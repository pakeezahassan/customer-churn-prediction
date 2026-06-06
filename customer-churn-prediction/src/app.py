"""
Customer Churn Prediction - Flask API
Production-ready REST API for making predictions
"""

from flask import Flask, request, jsonify
import joblib
import numpy as np
import pandas as pd
from datetime import datetime
import logging
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)

# Load pre-trained model
try:
    model_data = joblib.load('models/churn_model.pkl')
    model = model_data['model']
    scaler = model_data['scaler']
    feature_names = model_data['feature_names']
    logger.info("✓ Model loaded successfully")
except Exception as e:
    logger.error(f"Error loading model: {e}")
    model = None

# ==============================================================================
# ROUTES
# ==============================================================================

@app.route('/', methods=['GET'])
def home():
    """Home page with API documentation"""
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>📱 Customer Churn Prediction API</title>
        <style>
            body { 
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
                margin: 0; 
                padding: 20px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
            }
            .container { 
                max-width: 1000px; 
                margin: 0 auto; 
                background: white; 
                padding: 40px; 
                border-radius: 10px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.3);
            }
            h1 { 
                color: #333; 
                text-align: center;
                margin-bottom: 30px;
            }
            .status { 
                padding: 15px; 
                margin: 20px 0; 
                border-radius: 8px; 
                text-align: center;
                font-weight: bold;
            }
            .status.healthy { 
                background: #d4edda; 
                color: #155724; 
                border: 2px solid #28a745;
            }
            .endpoint { 
                background: #f8f9fa; 
                padding: 20px; 
                margin: 20px 0; 
                border-radius: 8px; 
                border-left: 5px solid #667eea;
            }
            .method { 
                color: #667eea; 
                font-weight: bold; 
                font-size: 14px;
            }
            code { 
                background: #2c3e50; 
                color: #ecf0f1; 
                padding: 10px; 
                border-radius: 5px;
                display: block;
                overflow-x: auto;
                margin: 10px 0;
                font-size: 12px;
            }
            .example { 
                background: #f0f0f0; 
                padding: 15px; 
                border-radius: 5px;
                margin: 10px 0;
            }
            h2 { color: #333; margin-top: 30px; }
            h3 { color: #667eea; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>📱 Customer Churn Prediction API</h1>
            <p style="text-align: center; color: #666;">Production-ready ML API for predicting customer churn</p>
            
            <div class="status healthy">✓ API is HEALTHY and ready to use</div>
            
            <h2>📚 API Endpoints</h2>
            
            <div class="endpoint">
                <div class="method">GET /health</div>
                <h3>Health Check</h3>
                <p>Check if API is running</p>
                <code>curl http://localhost:5000/health</code>
            </div>
            
            <div class="endpoint">
                <div class="method">GET /info</div>
                <h3>Model Information</h3>
                <p>Get model details and feature names</p>
                <code>curl http://localhost:5000/info</code>
            </div>
            
            <div class="endpoint">
                <div class="method">POST /predict</div>
                <h3>Single Prediction</h3>
                <p>Predict churn for one customer</p>
                <code>curl -X POST http://localhost:5000/predict \\
  -H "Content-Type: application/json" \\
  -d '{"features": [65, 2, 34.65, 45, 0, 0, 1, 1, ...]}'</code>
                <p><strong>Parameters:</strong> features array with 35+ values</p>
            </div>
            
            <div class="endpoint">
                <div class="method">POST /batch-predict</div>
                <h3>Batch Predictions</h3>
                <p>Predict churn for multiple customers</p>
                <code>curl -X POST http://localhost:5000/batch-predict \\
  -H "Content-Type: application/json" \\
  -d '{"data": [[65, 2, 34.65, ...], [45, 1, 55.20, ...]]}'</code>
            </div>
            
            <h2>💡 Example Usage</h2>
            
            <div class="example">
                <h3>Python</h3>
                <code>import requests

url = "http://localhost:5000/predict"
data = {"features": [65, 2, 34.65, 45, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0]}
response = requests.post(url, json=data)
print(response.json())</code>
            </div>
            
            <div class="example">
                <h3>JavaScript</h3>
                <code>fetch('http://localhost:5000/predict', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({features: [65, 2, 34.65, ...]})
})
.then(r => r.json())
.then(data => console.log(data))</code>
            </div>
            
            <h2>📊 Response Format</h2>
            
            <div class="example">
                <code>{
  "prediction": 1,
  "prediction_label": "Will Churn",
  "probability_stay": 0.35,
  "probability_churn": 0.65,
  "confidence": 0.65,
  "timestamp": "2024-12-10T15:30:00",
  "success": true
}</code>
            </div>
            
            <h2>🔧 Features Required</h2>
            <p>Model expects 35+ features (all encoded as numbers). Features include:</p>
            <ul>
                <li>age, tenure, monthlyCharges, totalCharges</li>
                <li>One-hot encoded categorical variables</li>
                <li>Contract type, internet service, payment method, etc.</li>
            </ul>
            
            <p style="text-align: center; color: #999; margin-top: 40px;">
                Built with ❤️ | Flask + scikit-learn | Deployed successfully
            </p>
        </div>
    </body>
    </html>
    '''

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy' if model else 'error',
        'timestamp': datetime.now().isoformat(),
        'message': 'Model is running' if model else 'Model failed to load'
    }), 200 if model else 500

@app.route('/info', methods=['GET'])
def info():
    """Get model information"""
    return jsonify({
        'model_type': str(type(model).__name__),
        'n_features': len(feature_names) if feature_names is not None else 0,
        'features': list(feature_names) if feature_names is not None else [],
        'scaler': str(type(scaler).__name__)
    })

@app.route('/predict', methods=['POST'])
def predict():
    """
    Make prediction for single customer
    
    Expected JSON:
    {"features": [value1, value2, ...]}
    """
    
    if model is None:
        return jsonify({'error': 'Model not loaded'}), 500
    
    try:
        data = request.get_json()
        
        if 'features' not in data:
            return jsonify({'error': 'Missing "features" in request'}), 400
        
        features = np.array(data['features']).reshape(1, -1)
        
        # Validate input
        if features.shape[1] != len(feature_names):
            return jsonify({
                'error': f'Expected {len(feature_names)} features, got {features.shape[1]}'
            }), 400
        
        # Scale and predict
        features_scaled = scaler.transform(features)
        prediction = model.predict(features_scaled)[0]
        prediction_proba = model.predict_proba(features_scaled)[0]
        
        return jsonify({
            'prediction': int(prediction),
            'prediction_label': 'Will Churn' if prediction == 1 else 'Will Stay',
            'probability_stay': float(prediction_proba[0]),
            'probability_churn': float(prediction_proba[1]),
            'confidence': float(max(prediction_proba)),
            'timestamp': datetime.now().isoformat(),
            'success': True
        }), 200
    
    except Exception as e:
        logger.error(f"Prediction error: {str(e)}")
        return jsonify({
            'error': str(e),
            'success': False
        }), 400

@app.route('/batch-predict', methods=['POST'])
def batch_predict():
    """
    Predict on multiple customers
    
    Expected JSON:
    {"data": [[val1, val2, ...], [val1, val2, ...]]}
    """
    
    if model is None:
        return jsonify({'error': 'Model not loaded'}), 500
    
    try:
        data = request.get_json()
        samples = data.get('data', [])
        
        if not samples:
            return jsonify({'error': 'No data provided'}), 400
        
        # Convert to array
        features = np.array(samples)
        
        # Validate
        if features.shape[1] != len(feature_names):
            return jsonify({
                'error': f'Expected {len(feature_names)} features, got {features.shape[1]}'
            }), 400
        
        # Scale and predict
        features_scaled = scaler.transform(features)
        predictions = model.predict(features_scaled)
        predictions_proba = model.predict_proba(features_scaled)
        
        results = []
        for i, (pred, proba) in enumerate(zip(predictions, predictions_proba)):
            results.append({
                'customer_id': i,
                'prediction': int(pred),
                'prediction_label': 'Will Churn' if pred == 1 else 'Will Stay',
                'probability_stay': float(proba[0]),
                'probability_churn': float(proba[1]),
                'confidence': float(max(proba))
            })
        
        return jsonify({
            'predictions': results,
            'n_samples': len(predictions),
            'churn_rate': float(predictions.mean()),
            'timestamp': datetime.now().isoformat(),
            'success': True
        }), 200
    
    except Exception as e:
        logger.error(f"Batch prediction error: {str(e)}")
        return jsonify({
            'error': str(e),
            'success': False
        }), 400

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({'error': 'Endpoint not found', 'status': 404}), 404

@app.errorhandler(500)
def server_error(error):
    """Handle 500 errors"""
    return jsonify({'error': 'Server error', 'status': 500}), 500

# ==============================================================================
# MAIN
# ==============================================================================

if __name__ == '__main__':
    print("""
    ╔════════════════════════════════════════╗
    ║  📱 CHURN PREDICTION API               ║
    ║  Starting Flask Server...              ║
    ║  http://localhost:5000                 ║
    ╚════════════════════════════════════════╝
    """)
    
    # Create directories if they don't exist
    os.makedirs('models', exist_ok=True)
    os.makedirs('outputs', exist_ok=True)
    
    # Run Flask app
    app.run(debug=True, host='0.0.0.0', port=5000)
