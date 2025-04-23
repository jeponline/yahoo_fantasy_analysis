from flask import Flask
from flask_apscheduler import APScheduler
from config.config import Config
import os
from datetime import datetime

scheduler = APScheduler()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize scheduler
    scheduler.init_app(app)
    scheduler.start()
    
    # Create data directory if it doesn't exist
    os.makedirs(app.config['DATA_DIR'], exist_ok=True)
    
    # Register blueprints
    from app.routes import main
    app.register_blueprint(main)
    
    # Add global template variables
    @app.context_processor
    def inject_now():
        return {'now': datetime.now()}
    
    return app