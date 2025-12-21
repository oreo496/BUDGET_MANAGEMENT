from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.conf import settings
from .models import AIAlert
from .serializers import AIAlertSerializer
import torch
import torch.nn as nn
import numpy as np
import pandas as pd
import pickle
import os
from pathlib import Path


# ========== MODEL DEFINITIONS (Mirror from notebook) ==========

class DeepNeuralNetwork(nn.Module):
    """DNN architecture for transaction classification and flagged detection"""
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


class AttentionLayer(nn.Module):
    def __init__(self, hidden_dim):
        super(AttentionLayer, self).__init__()
        self.attention = nn.Linear(hidden_dim, 1)

    def forward(self, x):
        attention_weights = torch.softmax(self.attention(x), dim=1)
        return x * attention_weights


class AttentionNeuralNetwork(nn.Module):
    """Attention-based neural network for transaction classification"""
    def __init__(self, input_dim, num_classes):
        super(AttentionNeuralNetwork, self).__init__()
        self.fc1 = nn.Linear(input_dim, 256)
        self.bn1 = nn.BatchNorm1d(256)
        self.attention1 = AttentionLayer(256)
        self.fc2 = nn.Linear(256, 128)
        self.bn2 = nn.BatchNorm1d(128)
        self.attention2 = AttentionLayer(128)
        self.fc3 = nn.Linear(128, 64)
        self.bn3 = nn.BatchNorm1d(64)
        self.fc_out = nn.Linear(64, num_classes)
        self.relu = nn.ReLU()
        self.dropout = nn.Dropout(0.3)

    def forward(self, x):
        x = self.fc1(x)
        x = self.bn1(x)
        x = self.relu(x)
        x = self.attention1(x)
        x = self.dropout(x)
        x = self.fc2(x)
        x = self.bn2(x)
        x = self.relu(x)
        x = self.attention2(x)
        x = self.dropout(x)
        x = self.fc3(x)
        x = self.bn3(x)
        x = self.relu(x)
        x = self.dropout(x)
        x = self.fc_out(x)
        return x


# ========== MODEL LOADER UTILITIES ==========

MODEL_DIR = Path(settings.BASE_DIR) / "model_store"
_loaded_models = {}


def load_model_once(model_key, loader_func):
    """Cache loaded models to avoid reloading on every request"""
    if model_key not in _loaded_models:
        _loaded_models[model_key] = loader_func()
    return _loaded_models[model_key]


def load_transaction_models():
    """Load all transaction classification models and preprocessing objects"""
    try:
        device = torch.device('cpu')
        
        # Load preprocessing objects
        with open(MODEL_DIR / "transaction_preprocessing.pkl", 'rb') as f:
            preprocessing = pickle.load(f)
        
        # Load DNN model
        dnn_checkpoint = torch.load(MODEL_DIR / "transaction_dnn_model.pth", map_location=device)
        dnn_model = DeepNeuralNetwork(dnn_checkpoint['input_dim'], dnn_checkpoint['num_classes'])
        dnn_model.load_state_dict(dnn_checkpoint['model_state_dict'])
        dnn_model.eval()
        
        # Load ResNet model
        resnet_checkpoint = torch.load(MODEL_DIR / "transaction_resnet_model.pth", map_location=device)
        resnet_model = ResidualNeuralNetwork(resnet_checkpoint['input_dim'], resnet_checkpoint['num_classes'])
        resnet_model.load_state_dict(resnet_checkpoint['model_state_dict'])
        resnet_model.eval()
        
        # Load Attention model
        attention_checkpoint = torch.load(MODEL_DIR / "transaction_attention_model.pth", map_location=device)
        attention_model = AttentionNeuralNetwork(attention_checkpoint['input_dim'], attention_checkpoint['num_classes'])
        attention_model.load_state_dict(attention_checkpoint['model_state_dict'])
        attention_model.eval()
        
        # Try to load TabNet if available
        tabnet_model = None
        try:
            from pytorch_tabnet.tab_model import TabNetClassifier
            tabnet_model = TabNetClassifier()
            tabnet_model.load_model(str(MODEL_DIR / "transaction_tabnet_model.zip"))
        except:
            pass
        
        return {
            'dnn': dnn_model,
            'resnet': resnet_model,
            'attention': attention_model,
            'tabnet': tabnet_model,
            'preprocessing': preprocessing,
            'device': device
        }
    except Exception as e:
        raise Exception(f"Error loading transaction models: {str(e)}")


def load_budget_model():
    """Load budget overrun prediction model"""
    try:
        from pytorch_tabnet.tab_model import TabNetClassifier
        
        model = TabNetClassifier()
        model.load_model(str(MODEL_DIR / "budget_overrun_tabnet_model.zip"))
        
        with open(MODEL_DIR / "budget_overrun_metadata.pkl", 'rb') as f:
            metadata = pickle.load(f)
        
        return {'model': model, 'metadata': metadata}
    except Exception as e:
        raise Exception(f"Error loading budget model: {str(e)}")


def load_goal_model():
    """Load savings goal success prediction model"""
    try:
        from pytorch_tabnet.tab_model import TabNetClassifier
        
        model = TabNetClassifier()
        model.load_model(str(MODEL_DIR / "savings_goal_tabnet_model.zip"))
        
        with open(MODEL_DIR / "savings_goal_metadata.pkl", 'rb') as f:
            metadata = pickle.load(f)
        
        return {'model': model, 'metadata': metadata}
    except Exception as e:
        raise Exception(f"Error loading goal model: {str(e)}")


def load_flagged_model():
    """Load flagged transaction detection model"""
    try:
        device = torch.device('cpu')
        
        with open(MODEL_DIR / "flagged_transaction_preprocessing.pkl", 'rb') as f:
            preprocessing = pickle.load(f)
        
        checkpoint = torch.load(MODEL_DIR / "flagged_transaction_dnn_model.pth", map_location=device)
        model = DeepNeuralNetwork(checkpoint['input_dim'], checkpoint['num_classes'])
        model.load_state_dict(checkpoint['model_state_dict'])
        model.eval()
        
        return {'model': model, 'preprocessing': preprocessing, 'device': device}
    except Exception as e:
        raise Exception(f"Error loading flagged model: {str(e)}")


# ========== API ENDPOINTS ==========

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def predict_transaction_type(request):
    """
    Predict transaction type using ensemble of deep learning models
    
    Request body:
    {
        "amount": 150.00,
        "category": "Food",
        "payment_method": "Credit Card",
        "merchant_name": "Restaurant XYZ",
        ... (other transaction features)
    }
    """
    try:
        models = load_model_once('transaction', load_transaction_models)
        
        # Extract features from request
        data = request.data
        preprocessing = models['preprocessing']
        
        # Prepare feature vector
        numeric_features = [data.get(f, 0) for f in preprocessing['numeric_features']]
        
        # Scale numeric features
        X_numeric = np.array(numeric_features).reshape(1, -1)
        X_scaled = preprocessing['scaler'].transform(X_numeric)
        
        # Encode categorical features if present
        if preprocessing['cat_encoder'] is not None:
            categorical_features = [data.get(f, 'missing') for f in preprocessing['categorical_features']]
            X_cat = np.array(categorical_features).reshape(1, -1)
            X_cat_encoded = preprocessing['cat_encoder'].transform(X_cat)
            X_final = np.concatenate([X_scaled, X_cat_encoded], axis=1)
        else:
            X_final = X_scaled
        
        # Get predictions from all models
        X_tensor = torch.FloatTensor(X_final).to(models['device'])
        
        predictions = []
        with torch.no_grad():
            # DNN prediction
            dnn_output = models['dnn'](X_tensor)
            dnn_pred = torch.argmax(dnn_output, dim=1).cpu().numpy()[0]
            predictions.append(dnn_pred)
            
            # ResNet prediction
            resnet_output = models['resnet'](X_tensor)
            resnet_pred = torch.argmax(resnet_output, dim=1).cpu().numpy()[0]
            predictions.append(resnet_pred)
            
            # Attention prediction
            attention_output = models['attention'](X_tensor)
            attention_pred = torch.argmax(attention_output, dim=1).cpu().numpy()[0]
            predictions.append(attention_pred)
            
            # TabNet prediction if available
            if models['tabnet'] is not None:
                tabnet_pred = models['tabnet'].predict(X_final)[0]
                predictions.append(tabnet_pred)
        
        # Ensemble voting
        from collections import Counter
        ensemble_pred = Counter(predictions).most_common(1)[0][0]
        
        # Decode prediction
        predicted_type = preprocessing['label_encoder'].inverse_transform([ensemble_pred])[0]
        
        return Response({
            'success': True,
            'predicted_type': predicted_type,
            'confidence': float(len([p for p in predictions if p == ensemble_pred]) / len(predictions)),
            'model_votes': {
                'dnn': preprocessing['label_encoder'].inverse_transform([predictions[0]])[0],
                'resnet': preprocessing['label_encoder'].inverse_transform([predictions[1]])[0],
                'attention': preprocessing['label_encoder'].inverse_transform([predictions[2]])[0]
            }
        })
        
    except Exception as e:
        return Response({
            'success': False,
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def predict_budget_risk(request):
    """
    Predict budget overrun risk
    
    Request body:
    {
        "total_spent": 1200.00,
        "monthly_budget": 1500.00,
        "days_passed": 20,
        "transaction_count": 45,
        "avg_transaction_size": 26.67,
        "recent_trend": 50.00
    }
    """
    try:
        budget_data = load_model_once('budget', load_budget_model)
        model = budget_data['model']
        metadata = budget_data['metadata']
        
        # Extract features
        data = request.data
        features = []
        for feature_name in metadata['features']:
            if feature_name == 'days_remaining':
                features.append(30 - data.get('days_passed', 15))
            elif feature_name == 'budget_utilization':
                features.append(data.get('total_spent', 0) / max(data.get('monthly_budget', 1), 1))
            elif feature_name == 'daily_burn_rate':
                features.append(data.get('total_spent', 0) / max(data.get('days_passed', 1), 1))
            elif feature_name == 'projected_total':
                daily_rate = data.get('total_spent', 0) / max(data.get('days_passed', 1), 1)
                features.append(daily_rate * 30)
            else:
                features.append(data.get(feature_name, 0))
        
        X = np.array(features).reshape(1, -1)
        
        # Make prediction
        prediction = model.predict(X)[0]
        probability = model.predict_proba(X)[0][1]
        
        # Determine risk level
        if probability > metadata['risk_threshold_high']:
            risk_level = 'HIGH'
        elif probability > metadata['risk_threshold_medium']:
            risk_level = 'MEDIUM'
        else:
            risk_level = 'LOW'
        
        # Calculate recommendations
        current_budget = data.get('monthly_budget', 0)
        if probability > 0.75:
            recommended_budget = current_budget * 1.20
        elif probability > 0.5:
            recommended_budget = current_budget * 1.10
        else:
            recommended_budget = current_budget
        
        days_remaining = 30 - data.get('days_passed', 15)
        daily_cap = max((current_budget - data.get('total_spent', 0)) / max(days_remaining, 1), 0)
        
        return Response({
            'success': True,
            'overrun_risk': bool(prediction),
            'risk_probability': float(probability),
            'risk_level': risk_level,
            'recommended_budget': float(recommended_budget),
            'daily_spending_cap': float(daily_cap),
            'model_accuracy': float(metadata['accuracy'])
        })
        
    except Exception as e:
        return Response({
            'success': False,
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def predict_goal_success(request):
    """
    Predict savings goal success probability
    
    Request body:
    {
        "goal_amount": 10000.00,
        "current_savings": 3000.00,
        "months_remaining": 12,
        "monthly_income": 5000.00,
        "monthly_expenses": 3500.00,
        "past_contributions": 200.00,
        "contribution_consistency": 0.75,
        "income_stability": 0.80,
        "past_goal_success_rate": 0.65
    }
    """
    try:
        goal_data = load_model_once('goal', load_goal_model)
        model = goal_data['model']
        metadata = goal_data['metadata']
        
        # Extract and calculate features
        data = request.data
        goal_amount = data.get('goal_amount', 0)
        current_savings = data.get('current_savings', 0)
        months_remaining = data.get('months_remaining', 12)
        monthly_income = data.get('monthly_income', 0)
        monthly_expenses = data.get('monthly_expenses', 0)
        
        features = [
            goal_amount,
            current_savings,
            months_remaining,
            monthly_income,
            monthly_expenses,
            data.get('past_contributions', 0),
            data.get('contribution_consistency', 0.5),
            data.get('income_stability', 0.5),
            data.get('past_goal_success_rate', 0.5),
            (current_savings / max(goal_amount, 1)) * 100,  # progress_percentage
            monthly_income - monthly_expenses,  # monthly_surplus
            (goal_amount - current_savings) / max(months_remaining, 1),  # required_monthly_contribution
            (monthly_income - monthly_expenses) / max((goal_amount - current_savings) / max(months_remaining, 1), 1)  # surplus_to_required_ratio
        ]
        
        X = np.array(features).reshape(1, -1)
        
        # Make prediction
        prediction = model.predict(X)[0]
        probability = model.predict_proba(X)[0][1]
        
        # Determine confidence level
        if probability > metadata['success_threshold']:
            confidence = 'HIGH'
        elif probability > 0.5:
            confidence = 'MODERATE'
        else:
            confidence = 'LOW'
        
        # Calculate timeline probabilities
        timeline_probabilities = {}
        for month in range(0, months_remaining + 1, max(1, months_remaining // 4)):
            time_factor = (months_remaining - month) / max(months_remaining, 1)
            month_prob = probability * (1 - 0.3 * time_factor)
            timeline_probabilities[f'month_{month}'] = round(min(month_prob, 1.0), 3)
        
        required_contribution = (goal_amount - current_savings) / max(months_remaining, 1)
        
        return Response({
            'success': True,
            'goal_achievable': bool(prediction),
            'success_probability': float(probability),
            'confidence_level': confidence,
            'recommended_monthly_contribution': float(required_contribution),
            'timeline_probabilities': timeline_probabilities,
            'model_accuracy': float(metadata['accuracy'])
        })
        
    except Exception as e:
        return Response({
            'success': False,
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def predict_flagged_transaction(request):
    """
    Predict if a transaction should be flagged as suspicious
    
    Request body: Same as predict_transaction_type
    """
    try:
        flagged_data = load_model_once('flagged', load_flagged_model)
        model = flagged_data['model']
        preprocessing = flagged_data['preprocessing']
        device = flagged_data['device']
        
        # Extract features
        data = request.data
        numeric_features = [data.get(f, 0) for f in preprocessing['numeric_features']]
        
        # Scale numeric features
        X_numeric = np.array(numeric_features).reshape(1, -1)
        X_scaled = preprocessing['scaler'].transform(X_numeric)
        
        # Encode categorical features if present
        if preprocessing['cat_encoder'] is not None:
            categorical_features = [data.get(f, 'missing') for f in preprocessing['categorical_features']]
            X_cat = np.array(categorical_features).reshape(1, -1)
            X_cat_encoded = preprocessing['cat_encoder'].transform(X_cat)
            X_final = np.concatenate([X_scaled, X_cat_encoded], axis=1)
        else:
            X_final = X_scaled
        
        # Make prediction
        X_tensor = torch.FloatTensor(X_final).to(device)
        
        with torch.no_grad():
            output = model(X_tensor)
            probabilities = torch.softmax(output, dim=1)
            prediction = torch.argmax(output, dim=1).cpu().numpy()[0]
            confidence = probabilities[0][prediction].item()
        
        # Decode prediction
        is_flagged = bool(preprocessing['label_encoder'].inverse_transform([prediction])[0])
        
        return Response({
            'success': True,
            'is_flagged': is_flagged,
            'confidence': float(confidence),
            'risk_score': float(probabilities[0][1].item()) if len(probabilities[0]) > 1 else 0.0
        })
        
    except Exception as e:
        return Response({
            'success': False,
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# ========== ORIGINAL VIEWSET ==========

class AIAlertViewSet(viewsets.ModelViewSet):
    serializer_class = AIAlertSerializer

    def get_queryset(self):
        return AIAlert.objects.all()

