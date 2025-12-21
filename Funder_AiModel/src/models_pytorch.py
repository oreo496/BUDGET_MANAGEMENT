"""
PyTorch neural network models for the FinanceAI system.
Defines architectures for DNN, ResNet, Attention networks and supporting loss functions.
"""

import torch
import torch.nn as nn
from torch.utils.data import Dataset


class TabularDataset(Dataset):
    """Custom PyTorch Dataset for tabular data with optional augmentation."""
    
    def __init__(self, X, y, augment=False, noise_std=0.02):
        """
        Args:
            X: Feature tensor
            y: Target tensor
            augment: Whether to apply random noise augmentation during training
            noise_std: Standard deviation of noise for augmentation
        """
        self.X = X
        self.y = y
        self.augment = augment
        self.noise_std = noise_std

    def __len__(self):
        return len(self.X)

    def __getitem__(self, idx):
        x = self.X[idx]
        y = self.y[idx]

        # Apply random noise during training for regularization
        if self.augment:
            noise = torch.randn_like(x) * self.noise_std
            x = x + noise

        return x, y


class DeepNeuralNetwork(nn.Module):
    """Deep Neural Network with batch normalization and dropout for classification."""
    
    def __init__(self, input_dim, num_classes):
        """
        Args:
            input_dim: Number of input features
            num_classes: Number of output classes
        """
        super(DeepNeuralNetwork, self).__init__()
        self.network = nn.Sequential(
            nn.Linear(input_dim, 256), 
            nn.BatchNorm1d(256), 
            nn.ReLU(), 
            nn.Dropout(0.4),
            
            nn.Linear(256, 128), 
            nn.BatchNorm1d(128), 
            nn.ReLU(), 
            nn.Dropout(0.4),
            
            nn.Linear(128, 64), 
            nn.BatchNorm1d(64), 
            nn.ReLU(), 
            nn.Dropout(0.3),
            
            nn.Linear(64, num_classes)
        )

    def forward(self, x):
        return self.network(x)


class LabelSmoothingLoss(nn.Module):
    """Cross-entropy loss with label smoothing for improved generalization."""
    
    def __init__(self, classes, smoothing=0.1):
        """
        Args:
            classes: Number of classes
            smoothing: Label smoothing factor (0-1)
        """
        super(LabelSmoothingLoss, self).__init__()
        self.confidence = 1.0 - smoothing
        self.smoothing = smoothing
        self.classes = classes

    def forward(self, pred, target):
        """
        Args:
            pred: Model predictions (logits)
            target: Ground truth labels
        
        Returns:
            Smoothed cross-entropy loss
        """
        pred = pred.log_softmax(dim=-1)
        with torch.no_grad():
            true_dist = torch.zeros_like(pred)
            true_dist.fill_(self.smoothing / (self.classes - 1))
            true_dist.scatter_(1, target.data.unsqueeze(1), self.confidence)
        return torch.mean(torch.sum(-true_dist * pred, dim=-1))


class ResidualBlock(nn.Module):
    """Residual block with skip connection for ResNet architecture."""
    
    def __init__(self, input_dim, hidden_dim):
        """
        Args:
            input_dim: Input dimension
            hidden_dim: Hidden layer dimension
        """
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
        out += residual  # Add skip connection
        out = self.relu(out)
        return out


class ResidualNeuralNetwork(nn.Module):
    """ResNet-style architecture with residual blocks for improved gradient flow."""
    
    def __init__(self, input_dim, num_classes):
        """
        Args:
            input_dim: Number of input features
            num_classes: Number of output classes
        """
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
    """Self-attention mechanism to weight important features."""
    
    def __init__(self, hidden_dim):
        """
        Args:
            hidden_dim: Hidden dimension for attention computation
        """
        super(AttentionLayer, self).__init__()
        self.attention = nn.Linear(hidden_dim, 1)

    def forward(self, x):
        """
        Args:
            x: Input tensor of shape (batch, seq_len, hidden_dim)
        
        Returns:
            Weighted tensor with attention applied
        """
        attention_weights = torch.softmax(self.attention(x), dim=1)
        return x * attention_weights


class AttentionNeuralNetwork(nn.Module):
    """Neural network with attention mechanisms to highlight important features."""
    
    def __init__(self, input_dim, num_classes):
        """
        Args:
            input_dim: Number of input features
            num_classes: Number of output classes
        """
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
