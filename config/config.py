import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    # Flask config
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard-to-guess-string'
    
    # Yahoo Fantasy API config
    CREDENTIALS_FILE = os.path.join(os.path.dirname(__file__), 'oauth2.json')
    
    # Data storage config
    DATA_DIR = os.environ.get('DATA_DIR') or os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
    
    # Scheduler config
    SCHEDULER_API_ENABLED = True
    JOBS = [
        {
            'id': 'refresh_data',
            'func': 'app.services.data_service:refresh_all_data',
            'trigger': 'interval',
            'hours': 6,  # Run every 6 hours by default
        }
    ]