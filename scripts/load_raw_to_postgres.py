import json
import pandas as pd
from pathlib import Path
from src.database import engine

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_DIR = (
    PROJECT_ROOT /
    "data" /
    "raw" /
    "telegram_messages"
)

json_files = []

for date_folder in DATA_DIR.iterdir():

    if date_folder.is_dir():

        json_files.extend(
            date_folder.glob("*.json")
        )

records = []

for file in json_files:

    with open(file, encoding="utf-8") as f:

        records.extend(
            json.load(f)
        )




df = pd.DataFrame(records)

#### Prepare the dataframe #####


df["message_date"] = pd.to_datetime(df["message_date"])

df["views"] = pd.to_numeric(df["views"], errors="coerce")
df["forwards"] = pd.to_numeric(df["forwards"], errors="coerce")

df["has_media"] = df["has_media"].astype(bool)

#### Load into PostgreSQL #####

# print(df.columns.tolist())
# print(df.head())
# print(df.shape)
# duplicates = df[df.duplicated(subset=["message_id"], keep=False)]

# print(duplicates[["message_id", "channel_name"]].sort_values("message_id"))
# print(f"Duplicate message IDs: {duplicates['message_id'].nunique()}")
df = df.drop_duplicates(
    subset=["message_id", "channel_name"]
)
df.to_sql(
    "telegram_messages",
    con=engine,
    schema="raw",
    if_exists="replace",
    index=False
)

print(f"{len(df)} rows loaded successfully.")