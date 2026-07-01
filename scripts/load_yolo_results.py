from pathlib import Path
import pandas as pd

from sqlalchemy import create_engine
from src.database import DATABASE_URL

engine = create_engine(DATABASE_URL)

PROJECT_ROOT = Path(__file__).resolve().parent.parent

csv_file = (
    PROJECT_ROOT /
    "data" /
    "processed" /
    "detections.csv"
)

df = pd.read_csv(csv_file)

df.to_sql(
    "image_detections",
    engine,
    schema="raw",
    if_exists="replace",
    index=False
)

print(f"Loaded {len(df)} detections into raw.image_detections")