from sqlalchemy import create_engine
from dotenv import load_dotenv
from src.config import DB_HOST,DB_NAME,DB_USER,DB_PASSWORD,DB_PORT
import os

load_dotenv()
print(f"DB_HOST = {DB_HOST}")
print(f"DB_PORT = {DB_PORT}")
print(f"DB_NAME = {DB_NAME}")
print(f"DB_USER = {DB_USER}")
DATABASE_URL = (
    f"postgresql+psycopg2://"
    f"{DB_USER}:"
    f"{DB_PASSWORD}@"
    f"{DB_HOST}:"
    f"{DB_PORT}/"
    f"{DB_NAME}"
)

engine = create_engine(DATABASE_URL)