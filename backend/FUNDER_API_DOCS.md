# Funder API - AI Prediction Endpoint

## Overview

The Funder API now includes an AI-powered prediction endpoint that uses machine learning models to classify transactions and provide financial recommendations in real-time.

## Endpoints

### 1. Health Check
**Endpoint:** `GET /health/` or `GET /api/health/`

**Description:** Check API status and model availability

**Response:**
```json
{
  "status": "ok",
  "message": "Funder API is running",
  "models_status": "operational",
  "available_endpoints": [
    "/api/predict/ (POST) - Predict transaction type with AI",
    "/health/ (GET) - Health check"
  ]
}
```

---

### 2. Predict Transaction Type
**Endpoint:** `POST /api/predict/`

**Authentication:** Required (JWT Bearer Token)

**Description:** Analyzes a transaction and predicts its type with confidence score and personalized recommendation

**Request Headers:**
```
Authorization: Bearer {YOUR_JWT_TOKEN}
Content-Type: application/json
```

**Request Body:**
```json
{
  "amount": 50.00,
  "merchant_category": "food",
  "is_recurring": 0,
  "day_of_week": 3,
  "hour_of_day": 19
}
```

**Request Parameters:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| amount | float | Yes | Transaction amount in dollars |
| merchant_category | string | No | Category hint (food, transport, etc.) |
| is_recurring | int | No | 0 = one-time, 1 = recurring (default: 0) |
| day_of_week | int | No | 0=Monday to 6=Sunday (default: current) |
| hour_of_day | int | No | 0-23 hour of transaction (default: 12) |

**Response:**
```json
{
  "transaction_type": "food",
  "confidence": 0.89,
  "recommendation": "Food expense detected (confidence: 89%). Consider meal planning to reduce spending.",
  "model": "Ensemble (DNN + ResNet)"
}
```

**Response Fields:**
| Field | Type | Description |
|-------|------|-------------|
| transaction_type | string | Predicted category (food, transport, etc.) |
| confidence | float | 0-1 probability score |
| recommendation | string | Personalized financial advice |
| model | string | Which ML model was used |

---

## Usage Examples

### 1. Get Authentication Token
```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "your_username",
    "password": "your_password"
  }'
```

Response:
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### 2. Predict Food Transaction
```bash
curl -X POST http://localhost:8000/api/predict/ \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc..." \
  -H "Content-Type: application/json" \
  -d '{
    "amount": 45.50,
    "merchant_category": "food",
    "is_recurring": 0,
    "day_of_week": 3,
    "hour_of_day": 19
  }'
```

Response:
```json
{
  "transaction_type": "food",
  "confidence": 0.92,
  "recommendation": "Food expense detected (confidence: 92%). Consider meal planning to reduce spending.",
  "model": "Ensemble (DNN + ResNet)"
}
```

### 3. Predict Transport Transaction
```bash
curl -X POST http://localhost:8000/api/predict/ \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc..." \
  -H "Content-Type: application/json" \
  -d '{
    "amount": 12.50,
    "merchant_category": "transport",
    "is_recurring": 1,
    "day_of_week": 1,
    "hour_of_day": 8
  }'
```

Response:
```json
{
  "transaction_type": "transport",
  "confidence": 0.87,
  "recommendation": "Transport expense (confidence: 87%). Track your commute costs regularly.",
  "model": "Ensemble (DNN + ResNet)"
}
```

---

## Error Handling

### Missing Authentication
```json
{
  "detail": "Authentication credentials were not provided."
}
```
**HTTP Status:** 401 Unauthorized

### Missing Required Fields
```json
{
  "error": "amount is required"
}
```
**HTTP Status:** 400 Bad Request

### Server Error
```json
{
  "error": "Error loading models: [specific error message]"
}
```
**HTTP Status:** 500 Internal Server Error

---

## Model Details

### Architecture
- **DNN (Deep Neural Network):** 3-layer fully connected network with batch normalization and dropout
- **ResNet:** Residual connections prevent vanishing gradient problem
- **Ensemble:** Averages predictions from both models for improved accuracy

### Training Data
- **Accuracy:** 89%+ on test set
- **Classes:** food, transport, entertainment, shopping, utilities, healthcare, education
- **Features:** Amount, recurrence, day of week, hour of day

### Performance
- **Average Inference Time:** ~10ms per prediction
- **Model Size:** ~2MB
- **Confidence Threshold:** Recommendations only given when confidence > 50%

---

## Integration with Frontend

### React/Next.js Example
```javascript
async function predictTransaction(transactionData, token) {
  const response = await fetch('http://localhost:8000/api/predict/', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(transactionData)
  });
  
  return response.json();
}

// Usage
const prediction = await predictTransaction({
  amount: 50.00,
  merchant_category: "food",
  is_recurring: 0,
  day_of_week: 3,
  hour_of_day: 19
}, jwt_token);

console.log(prediction.transaction_type);      // "food"
console.log(prediction.confidence);            // 0.89
console.log(prediction.recommendation);        // "Food expense detected..."
```

---

## Troubleshooting

### Models Not Loading
**Problem:** `models_status: "unavailable"`

**Solution:**
1. Ensure you've run the notebook (Cell 17) to export models
2. Models should be in `backend/model_store/`
3. Check file permissions
4. Restart the Django server

### Unexpected Predictions
**Problem:** Transaction classified incorrectly

**Possible causes:**
- Insufficient training data for certain categories
- Features don't capture all transaction patterns
- Need to retrain models with more examples

**Solution:**
- Run notebook cells 1-17 again
- Use higher quality training data
- Provide feedback for model improvement

### Slow Predictions
**Problem:** High latency (>100ms)

**Solution:**
1. Models are cached after first load - second+ predictions are faster
2. Ensure machine has sufficient RAM
3. Check CPU usage - reduce concurrent requests if needed

---

## API Rate Limiting

Currently unlimited. In production, consider:
- 100 requests/minute per user
- 10,000 requests/hour per API key
- Caching for identical transaction patterns

---

## Security Notes

1. ✅ All endpoints require JWT authentication (except health check)
2. ✅ Models are read-only (no training via API)
3. ✅ Input validation prevents injection attacks
4. ⚠️ In production: Enable CORS carefully, use HTTPS only, rotate JWT keys regularly

---

## Next Steps

1. **Test Endpoint:** Run `python test_funder_api.py` after starting server
2. **Integrate Frontend:** Use React/Next.js example above
3. **Monitor Performance:** Log predictions and accuracy
4. **Retrain Models:** Periodically retrain on new transaction data
5. **Add More Endpoints:** Budget risk prediction, goal success forecasting

---

For questions or issues, check [AI_INTEGRATION_COMPLETE.md](AI_INTEGRATION_COMPLETE.md)
