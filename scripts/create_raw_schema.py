from sqlalchemy import text

from src.database import engine

with engine.begin() as conn:

    conn.execute(text(
        """
        CREATE SCHEMA IF NOT EXISTS raw;
        """
    ))

    conn.execute(text("""
CREATE TABLE IF NOT EXISTS raw.telegram_messages (
    message_id BIGINT NOT NULL,
    channel_name TEXT NOT NULL,
    message_date TIMESTAMP,
    message_text TEXT,
    views INTEGER,
    forwards INTEGER,
    has_media BOOLEAN,
    image_path TEXT,

    PRIMARY KEY (channel_name, message_id)
);
"""))

print("Raw schema created.")