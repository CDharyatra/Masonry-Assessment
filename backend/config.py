import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration settings
class Config:
    # API keys
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', 'your-openai-api-key')
    SERPAPI_KEY = os.getenv('SERPAPI_KEY', 'your-serpapi-key')
    
    # Search engine settings
    SEARCH_RESULT_COUNT = 10
    
    # Web scraping settings
    REQUEST_TIMEOUT = 10
    USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    
    # Content analysis settings
    MAX_CONTENT_LENGTH = 10000
    
    # API settings
    API_HOST = '0.0.0.0'
    API_PORT = 5000
    
    # For development purposes, we'll use mock API keys if not provided
    if not OPENAI_API_KEY or OPENAI_API_KEY == 'your-openai-api-key':
        OPENAI_API_KEY = 'sk-mock-api-key-for-development'
