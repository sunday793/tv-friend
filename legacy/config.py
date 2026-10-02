# config.py
import os
from dotenv import load_dotenv

load_dotenv()

KINO_API_KEY = os.getenv("KINO_API_KEY")

if not KINO_API_KEY:
    raise ValueError(
        "KINO_API_KEY not found! Please create a .env file with:\n"
        "KINO_API_KEY=your_api_key_here"
    )