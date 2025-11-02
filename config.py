import os
from datetime import timedelta

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-here-change-in-production'
    
    # Updated MongoDB Atlas URI
    MONGODB_URI = os.environ.get('MONGODB_URI') or 'mongodb+srv://krishnak040897_db_user:GllvLBL9pzGJJlkz@cluster0.0rjcyjt.mongodb.net/taskdb?retryWrites=true&w=majority'
    
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'jwt-secret-key-change-in-production'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)
    
    # Arduino CLI configuration
    ARDUINO_CLI_PATH = 'arduino-cli'
    DEFAULT_FQBN = 'arduino:avr:uno'
    
    # OpenRouter AI configuration for code validation
    OPENROUTER_API_KEY = os.environ.get('OPENROUTER_API_KEY') or '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'
    OPENROUTER_MODEL = os.environ.get('OPENROUTER_MODEL') or 'openai/gpt-4o'
    OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"