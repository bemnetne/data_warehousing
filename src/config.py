from dotenv import load_dotenv
import os

load_dotenv()

TG_API_ID = os.getenv("TG_API_ID")
TG_API_HASH = os.getenv("TG_API_HASH")
PHONE_NUMBER = os.getenv("PHONE_NUMBER")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
if TG_API_ID is None:
    raise ValueError(
        "TG_API_ID not found. "
        "Please add it to your .env file."
    )

if TG_API_HASH is None:
    raise ValueError(
        "TG_API_HASH not found. "
        "Please add it to your .env file."
    )
if PHONE_NUMBER is None:
    raise ValueError(
        "PHONE_NUMBER not found. "
        "Please add it to your .env file."
    )
if DB_HOST is None:
    raise ValueError(
        "DB_HOST not found. "
        "Please add it to your .env file."
    )
if DB_PORT is None:
    raise ValueError(
        "DB_PORT not found. "
        "Please add it to your .env file."
    )
if DB_NAME is None:
    raise ValueError(
        "DB_NAME not found. "
        "Please add it to your .env file."
    )
if DB_PASSWORD is None:
    raise ValueError(
        "DB_PASSWORD not found. "
        "Please add it to your .env file."
    )
