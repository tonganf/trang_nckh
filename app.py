from flask import Flask, request, jsonify, render_template_string, send_from_directory
from flask_cors import CORS
import joblib
import numpy as np
import pandas as pd
import os
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Global variables
model = None
feature_columns = [
    'TBLANG', 'TBMATH', 'TBCT', 'TMKNM', 'TBLT',
    'M17', 'M19', 'M22', 'M30', 'M32', 'M33',
    'M34', 'M35', 'M36', 'M38', 'M41', 'M43',
    'M44', 'M45', 'M47'
]

def load_model():
    """Load the machine learning model"""
    global model
    model_path = 'rf_model.pkl'
    
    try:
        if os.path.exists(model_path):
            model = joblib.load(model_path)
            logger.info(f"✅ Model loaded successfully from {model_path}")
            return True
        else:
            logger.warning(f"⚠️ Model file not found at {model_path}")
            return False
    except Exception as e:
        logger.error(f"❌ Error loading model: {str(e)}")
        return False

def create_dummy_model():
    """Create a dummy model for testing when no real model is available"""
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.model_selection import train_test_split
    
    # Generate dummy data
    np.random.seed(42)
    n_samples = 1000
    X = np.random.uniform(0, 10, (n_samples, len(feature_columns)))  # Sử dụng 20 features
    
    # Create dummy target based on average score (0: Cảnh báo, 1: An toàn)
    avg_scores = X.mean(axis=1)
    y = np.where(avg_scores >= 6.0, 1, 0)  # 1 = An toàn, 0 = Cảnh báo
    
    # Train dummy model
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    dummy_model = RandomForestClassifier(n_estimators=100, random_state=42)
    dummy_model.fit(X_train, y_train)
    
    # Save dummy model
    joblib.dump(dummy_model, 'model.pkl')
    logger.info("✅ Created and saved dummy model for testing")
    
    return dummy_model

@app.route('/')
def index():
    """Serve the main HTML page"""
    try:
        with open('index.html', 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return """
        <h1>❌ Lỗi: Không tìm thấy file index.html</h1>
        <p>Vui lòng đảm bảo file index.html tồn tại trong thư mục gốc.</p>
        <p>Hoặc truy cập trực tiếp API tại <a href="/predict">/predict</a></p>
        """, 404

@app.route('/style.css')
def css():
    """Serve CSS file"""
    try:
        with open('style.css', 'r', encoding='utf-8') as f:
            response = app.response_class(
                response=f.read(),
                status=200,
                mimetype='text/css'
            )
            return response
    except FileNotFoundError:
        return "/* CSS file not found */", 404

@app.route('/script.js')
def js():
    """Serve JavaScript file"""
    try:
        with open('script.js', 'r', encoding='utf-8') as f:
            response = app.response_class(
                response=f.read(),
                status=200,
                mimetype='application/javascript'
            )
            return response
    except FileNotFoundError:
        return "// JavaScript file not found", 404

@app.route('/predict', methods=['POST', 'GET'])
def predict():
    """Handle prediction requests"""
    if request.method == 'GET':
        return jsonify({
            'message': 'Prediction API endpoint',
            'method': 'POST',
            'required_fields': feature_columns,
            'example': {field: 8.0 for field in feature_columns}
        })
    
    try:
        # Get JSON data from request
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'Không có dữ liệu được gửi'}), 400
        
        # Validate required fields
        missing_fields = [field for field in feature_columns if field not in data]
        if missing_fields:
            return jsonify({
                'error': f'Thiếu các trường bắt buộc: {", ".join(missing_fields)}'
            }), 400
        
        # Extract features in correct order
        features = []
        for field in feature_columns:
            try:
                value = float(data[field])
                if not (0 <= value <= 10):
                    return jsonify({
                        'error': f'Điểm {field} phải từ 0 đến 10 (nhận được: {value})'
                    }), 400
                features.append(value)
            except (ValueError, TypeError):
                return jsonify({
                    'error': f'Giá trị không hợp lệ cho trường {field}: {data[field]}'
                }), 400
        
        # Check if model is loaded
        if model is None:
            return jsonify({
                'error': 'Model chưa được tải. Vui lòng kiểm tra file model.pkl'
            }), 500
        
        # Make prediction
        features_array = np.array([features])
        prediction_raw = model.predict(features_array)[0]
        logger.info(f"Input features: {features}")
        logger.info(f"Prediction (raw): {prediction_raw}")
        # Convert prediction to meaningful labels
        if prediction_raw == 0:
            prediction_label = "⚠️ Cảnh báo"
        elif prediction_raw == 1:
            prediction_label = "✅ An toàn"
        else:
            prediction_label = str(prediction_raw)  # Fallback for other values
        
        # Get prediction probability if available
        prediction_proba = None
        if hasattr(model, 'predict_proba'):
            try:
                proba = model.predict_proba(features_array)[0]
                classes = model.classes_
                prediction_proba = {}
                for i, class_val in enumerate(classes):
                    if class_val == 0:
                        prediction_proba["Cảnh báo"] = float(proba[i])
                    elif class_val == 1:
                        prediction_proba["An toàn"] = float(proba[i])
                    else:
                        prediction_proba[str(class_val)] = float(proba[i])
            except Exception as e:
                logger.warning(f"Could not get prediction probabilities: {e}")
        
        # Log prediction
        logger.info(f"Prediction made: {prediction_raw} -> {prediction_label} for features: {dict(zip(feature_columns, features))}")
        
        response = {
            'prediction': prediction_label,
            'raw_prediction': int(prediction_raw),
            'confidence': prediction_proba,
            'timestamp': datetime.now().isoformat(),
            'input_data': dict(zip(feature_columns, features))
        }
        
        return jsonify(response)
        
    except Exception as e:
        logger.error(f"Prediction error: {str(e)}")
        return jsonify({
            'error': f'Lỗi xử lý dự đoán: {str(e)}'
        }), 500

@app.route('/health')
def health():
    """Health check endpoint"""
    model_status = "loaded" if model is not None else "not loaded"
    return jsonify({
        'status': 'healthy',
        'model_status': model_status,
        'timestamp': datetime.now().isoformat()
    })

@app.route('/model-info')
def model_info():
    """Get model information"""
    if model is None:
        return jsonify({'error': 'Model not loaded'}), 500
    
    info = {
        'model_type': type(model).__name__,
        'feature_columns': feature_columns,
        'n_features': len(feature_columns)
    }
    
    # Add additional info if available
    if hasattr(model, 'classes_'):
        info['classes'] = model.classes_.tolist()
    if hasattr(model, 'n_estimators'):
        info['n_estimators'] = model.n_estimators
    if hasattr(model, 'feature_importances_'):
        info['feature_importance'] = dict(zip(
            feature_columns, 
            model.feature_importances_.tolist()
        ))
    
    return jsonify(info)

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint không tồn tại'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Lỗi server nội bộ'}), 500

if __name__ == '__main__':
    print("🚀 Starting Flask application...")
    print("📁 Current directory:", os.getcwd())
    print("📂 Files in directory:", os.listdir('.'))
    
    # Try to load the model
    if not load_model():
        print("⚠️ No model found, creating dummy model for testing...")
        model = create_dummy_model()
    
    print(f"🤖 Model status: {'✅ Loaded' if model else '❌ Not loaded'}")
    print("🌐 Starting server...")
    print("📍 Access the application at: http://localhost:5000")
    print("🔗 API endpoint: http://localhost:5000/predict")
    print("💊 Health check: http://localhost:5000/health")
    
    app.run(debug=True, host='0.0.0.0', port=5000) 