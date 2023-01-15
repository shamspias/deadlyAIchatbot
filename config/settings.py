# DEV settings.py
import os
from dotenv import load_dotenv

load_dotenv()

# Flask Config
DEBUG = os.getenv("DEBUG")

# Secret key
SECRET_KEY = os.urandom(24)

# Open AI Key
OPEN_AI_KEY = os.getenv("OPEN_AI_KEY")

# Whatsapp API Config
WHATSAPP_HOOK_TOKEN = os.getenv('WHATSAPP_HOOK_TOKEN')
WHATSAPP_API_TOKEN = os.getenv("WHATSAPP_API_TOKEN")
WHATSAPP_NUMBER_ID = os.getenv("WHATSAPP_NUMBER_ID")
GRAPH_API_URL = "https://graph.facebook.com/v15.0/"

# Celery Config
CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL')
CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND')
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_REDIS_MAX_CONNECTIONS = 5
