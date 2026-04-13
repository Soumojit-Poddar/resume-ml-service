from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os

def create_app():
    """Create and configure the Flask application"""
    
    # Load environment variables
    load_dotenv()
    
    # Create Flask app
    app = Flask(__name__)
    
    # Configuration
    app.config['UPLOAD_FOLDER'] = os.getenv('UPLOAD_FOLDER', 'uploads')
    app.config['MAX_CONTENT_LENGTH'] = int(os.getenv('MAX_CONTENT_LENGTH', 5242880))
    
    # Enable CORS for all routes
    CORS(app, resources={r"/*": {"origins": "*"}})
    
    # Create upload folder
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    # Root route
    @app.route('/')
    def index():
        return jsonify({
            'message': 'ML Service API',
            'status': 'running',
            'version': '1.0.0'
        })
    
    # Register blueprints
    try:
        from app.routes.ml_routes import ml_bp
        app.register_blueprint(ml_bp, url_prefix='/api')
        print("✅ Blueprint registered successfully")
    except Exception as e:
        print(f"❌ Error registering blueprint: {e}")
        import traceback
        traceback.print_exc()
    
    return app