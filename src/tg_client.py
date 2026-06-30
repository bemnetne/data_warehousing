import sys
import os
sys.path.insert(0, os.path.abspath('..'))
from telethon import TelegramClient
from src.config import TG_API_HASH,TG_API_ID,PHONE_NUMBER

api_id = os.getenv("TG_API_ID")
api_hash = os.getenv("TG_API_HASH")

client = TelegramClient(
    "medical_session",
    api_id,
    api_hash
)