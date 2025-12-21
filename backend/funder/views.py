"""
Funder API Views - Core endpoint for AI-powered financial recommendations
"""
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
import torch
import torch.nn as nn
import numpy as np
import pandas as pd
import pickle
import os
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

# ========== MODEL DEFINITIONS (Mirror from notebook) ==========

class DeepNeuralNetwork(nn.Module):
    """DNN architecture for transaction classification"""
    def __init__(self, input_dim, num_classes):
        super(DeepNeuralNetwork, self).__init__()
        self.network = nn.Sequential(
            nn.Linear(input_dim, 256), nn.BatchNorm1d(256), nn.ReLU(), nn.Dropout(0.4),
            nn.Linear(256, 128), nn.BatchNorm1d(128), nn.ReLU(), nn.Dropout(0.4),
            nn.Linear(128, 64), nn.BatchNorm1d(64), nn.ReLU(), nn.Dropout(0.3),
            nn.Linear(64, num_classes)
        )
    
    def forward(self, x):
        return self.network(x)


class ResidualBlock(nn.Module):
    def __init__(self, input_dim, hidden_dim):
        super(ResidualBlock, self).__init__()
        self.fc1 = nn.Linear(input_dim, hidden_dim)
        self.bn1 = nn.BatchNorm1d(hidden_dim)
        self.fc2 = nn.Linear(hidden_dim, input_dim)
        self.bn2 = nn.BatchNorm1d(input_dim)
        self.relu = nn.ReLU()
        self.dropout = nn.Dropout(0.2)

    def forward(self, x):
        residual = x
        out = self.fc1(x)
        out = self.bn1(out)
        out = self.relu(out)
        out = self.dropout(out)
        out = self.fc2(out)
        out = self.bn2(out)
        out += residual
        out = self.relu(out)
        return out


class ResidualNeuralNetwork(nn.Module):
    """ResNet architecture for transaction classification"""
    def __init__(self, input_dim, num_classes):
        super(ResidualNeuralNetwork, self).__init__()
        self.input_layer = nn.Linear(input_dim, 256)
        self.bn_input = nn.BatchNorm1d(256)
        self.res_block1 = ResidualBlock(256, 512)
        self.res_block2 = ResidualBlock(256, 512)
        self.res_block3 = ResidualBlock(256, 512)
        self.fc_out = nn.Sequential(
            nn.Linear(256, 128),
            nn.BatchNorm1d(128),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(128, num_classes)
        )
        self.relu = nn.ReLU()

    def forward(self, x):
        x = self.input_layer(x)
        x = self.bn_input(x)
        x = self.relu(x)
        x = self.res_block1(x)
        x = self.res_block2(x)
        x = self.res_block3(x)
        x = self.fc_out(x)
        return x


# ========== MODEL LOADER UTILITIES ==========

MODEL_DIR = Path(settings.BASE_DIR) / "model_store"
_loaded_models = {}
_preprocessors = {}


def load_model_once(model_key, loader_func):
    """Cache loaded models to avoid reloading on every request"""
    if model_key not in _loaded_models:
        _loaded_models[model_key] = loader_func()
    return _loaded_models[model_key]


def load_transaction_models():
    """Load all transaction classification models"""
    try:
        device = torch.device('cpu')
        
        # Load preprocessing objects
        with open(MODEL_DIR / "transaction_preprocessing.pkl", 'rb') as f:
            preprocessing = pickle.load(f)
        
        _preprocessors['transaction'] = preprocessing
        
        # Load DNN model
        dnn_checkpoint = torch.load(MODEL_DIR / "transaction_dnn_model.pth", map_location=device)
        input_dim = dnn_checkpoint['input_dim']
        num_classes = dnn_checkpoint['num_classes']
        
        dnn_model = DeepNeuralNetwork(input_dim, num_classes).to(device)
        dnn_model.load_state_dict(dnn_checkpoint['model_state_dict'])
        dnn_model.eval()
        
        # Load ResNet model
        resnet_checkpoint = torch.load(MODEL_DIR / "transaction_resnet_model.pth", map_location=device)
        resnet_model = ResidualNeuralNetwork(input_dim, num_classes).to(device)
        resnet_model.load_state_dict(resnet_checkpoint['model_state_dict'])
        resnet_model.eval()
        
        return {
            'dnn': dnn_model,
            'resnet': resnet_model,
            'input_dim': input_dim,
            'num_classes': num_classes,
            'device': device,
            'label_encoder': preprocessing['label_encoder']
        }
    except Exception as e:
        logger.error(f"Error loading transaction models: {e}")
        raise


def preprocess_transaction_data(data, preprocessing_objs):
    """Convert raw transaction data to model-ready features"""
    try:
        # Extract numeric features from transaction
        amount = float(data.get('amount', 0))
        is_flagged = int(data.get('is_flagged', 0))
        monthly_budget = float(data.get('monthly_budget', 1000))
        spent_in_category_month = float(data.get('spent_in_category_month', 0))
        
        # Calculate over_budget_percentage
        if monthly_budget > 0:
            over_budget_percentage = (spent_in_category_month / monthly_budget) * 100
        else:
            over_budget_percentage = 0
        
        # Create numeric feature array (5 features as per preprocessing)
        numeric_features = np.array([[
            amount,
            is_flagged,
            monthly_budget,
            spent_in_category_month,
            over_budget_percentage
        ]], dtype=np.float32)
        
        # Scale numeric features
        scaler = preprocessing_objs['scaler']
        features_scaled = scaler.transform(numeric_features)
        
        # Handle categorical features if encoder exists
        cat_encoder = preprocessing_objs.get('cat_encoder')
        if cat_encoder is not None:
            category = data.get('category', 'other')
            payment_method = data.get('payment_method', 'cash')
            
            cat_features = np.array([[category, payment_method]])
            cat_encoded = cat_encoder.transform(cat_features)
            
            # Concatenate numeric and categorical features
            all_features = np.concatenate([features_scaled, cat_encoded], axis=1)
        else:
            all_features = features_scaled
        
        return torch.FloatTensor(all_features)
    except Exception as e:
        logger.error(f"Error preprocessing transaction data: {e}")
        raise


def predict_transaction_type(transaction_data):
    """Predict transaction type using ensemble of models"""
    try:
        models = load_model_once('transaction_models', load_transaction_models)
        
        # Preprocess data
        X = preprocess_transaction_data(transaction_data, _preprocessors['transaction'])
        X = X.to(models['device'])
        
        # Get predictions from both models
        with torch.no_grad():
            dnn_output = models['dnn'](X)
            resnet_output = models['resnet'](X)
            
            # Average logits and get predictions
            ensemble_output = (dnn_output + resnet_output) / 2
            _, ensemble_pred = torch.max(ensemble_output, 1)
        
        # Decode prediction
        pred_idx = ensemble_pred.item()
        pred_label = models['label_encoder'].inverse_transform([pred_idx])[0]
        
        # Get confidence
        probabilities = torch.softmax(ensemble_output, dim=1)
        confidence = probabilities[0][pred_idx].item()
        
        return {
            'transaction_type': str(pred_label),
            'confidence': float(confidence),
            'model': 'Ensemble (DNN + ResNet)',
            'recommendation': get_recommendation_for_type(pred_label, confidence)
        }
    except Exception as e:
        logger.error(f"Error predicting transaction type: {e}")
        return {
            'error': str(e),
            'transaction_type': 'unknown',
            'confidence': 0.0
        }


def get_recommendation_for_type(transaction_type, confidence):
    """Generate financial recommendation based on transaction type"""
    recommendations = {
        'food': f"Food expense detected (confidence: {confidence:.1%}). Consider meal planning to reduce spending.",
        'transport': f"Transport expense (confidence: {confidence:.1%}). Track your commute costs regularly.",
        'entertainment': f"Entertainment expense (confidence: {confidence:.1%}). Budget-friendly alternatives available!",
        'shopping': f"Shopping transaction (confidence: {confidence:.1%}). Review if this is necessary.",
        'utilities': f"Utility payment (confidence: {confidence:.1%}). Essential expense.",
        'healthcare': f"Healthcare expense (confidence: {confidence:.1%}). Important for your well-being.",
        'education': f"Education investment (confidence: {confidence:.1%}). Great for skill development!",
    }
    return recommendations.get(str(transaction_type).lower(), 
                              f"Transaction categorized as {transaction_type} (confidence: {confidence:.1%})")


# ========== API ENDPOINTS ==========

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def predict_transaction(request):
    """
    POST /api/predict/
    
    Request body:
    {
        "amount": 50.00,
        "merchant_category": "food",
        "is_recurring": 0,
        "day_of_week": 3,
        "hour_of_day": 19
    }
    
    Returns:
    {
        "transaction_type": "food",
        "confidence": 0.89,
        "recommendation": "Food expense detected...",
        "model": "Ensemble (DNN + ResNet)"
    }
    """
    try:
        data = request.data
        
        # Validate required fields
        if 'amount' not in data:
            return Response(
                {'error': 'amount is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        result = predict_transaction_type(data)
        return Response(result, status=status.HTTP_200_OK)
    
    except Exception as e:
        logger.error(f"Error in predict_transaction: {e}")
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
def health_check(request):
    """Health check endpoint with model status - LIVE MODEL VERIFICATION"""
    try:
        # Attempt to load and verify models are operational
        models = load_model_once('transaction_models', load_transaction_models)
        
        # Test a simple prediction to ensure models work
        test_data = {
            'amount': 50.0,
            'is_flagged': 0,
            'monthly_budget': 1000,
            'spent_in_category_month': 200,
            'over_budget_percentage': 20,
            'category': 'food',
            'payment_method': 'card'
        }
        
        test_result = predict_transaction_type(test_data)
        
        if 'error' not in test_result:
            models_status = 'active'
            model_info = {
                'transaction_model': 'Ensemble (DNN + ResNet)',
                'dnn_accuracy': '98.10%',
                'resnet_accuracy': '98.10%',
                'test_prediction': test_result
            }
        else:
            models_status = 'error'
            model_info = {'error': test_result.get('error')}
    
    except Exception as e:
        logger.error(f"Model verification failed: {e}")
        models_status = 'unavailable'
        model_info = {'error': str(e)}
    
    return Response({
        'status': 'ok',
        'message': 'Funder API is running',
        'models_status': models_status,  # ✓ Changed from static to LIVE status
        'model_info': model_info,
        'available_endpoints': [
            '/api/predict/ (POST, requires auth) - Predict transaction type with LIVE AI',
            '/api/predict/test/ (POST, no auth) - Test endpoint for model verification',
            '/health/ (GET) - Health check with model verification'
        ]
    })


@api_view(['POST'])
def predict_transaction_test(request):
    """
    TEST endpoint WITHOUT authentication (for development/verification)
    
    Request body:
    {
        "amount": 50.00,
        "is_flagged": 0,
        "monthly_budget": 1000,
        "spent_in_category_month": 200,
        "over_budget_percentage": 20,
        "category": "food",
        "payment_method": "card"
    }
    """
    try:
        data = request.data
        
        if 'amount' not in data:
            return Response(
                {'error': 'amount is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        result = predict_transaction_type(data)
        return Response(result, status=status.HTTP_200_OK)
    
    except Exception as e:
        logger.error(f"Error in predict_transaction_test: {e}")
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
