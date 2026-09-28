import os
from dotenv import load_dotenv

load_dotenv()

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY", "").strip()
FLASK_SECRET_KEY = os.getenv("FLASK_SECRET_KEY", "change-this-secret-key")
