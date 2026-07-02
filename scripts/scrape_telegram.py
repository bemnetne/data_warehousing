import asyncio
import json
import logging
from pathlib import Path
from collections import defaultdict
from src.tg_client import client
from src.channels import CHANNELS


PROJECT_ROOT = Path(__file__).resolve().parent.parent
LOG_DIR = PROJECT_ROOT / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)
IMAGES_DIR = PROJECT_ROOT / "data" / "raw" / "images"

IMAGES_DIR.mkdir(parents=True, exist_ok=True)
RAW_DIR = Path("data/raw")
RAW_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_DIR / "scraper.log"),
        logging.StreamHandler()  # Also show logs in the terminal
    ]
)

logger = logging.getLogger(__name__)
async def scrape_channel(channel_name):
    logger.info(f"Starting scrape for channel: {channel_name}")
    channel_image_dir = IMAGES_DIR / channel_name

    channel_image_dir.mkdir(
        parents=True,
        exist_ok=True
    )
    messages_by_date = defaultdict(list)
    # messages = []

    async for message in client.iter_messages(channel_name):

        image_path = None

        if message.photo:

            image_path = (
                channel_image_dir /
                f"{message.id}.jpg"
            )

            await message.download_media(
                file=str(image_path)
            )

        partition_date = message.date.strftime("%Y-%m-%d")

        messages_by_date[partition_date].append({
            "message_id": message.id,
            "channel_name": channel_name,
            "message_date": (
                message.date.isoformat()
                if message.date else None
            ),
            "message_text": message.message,
            "views": getattr(message, "views", None),
            "forwards": getattr(message, "forwards", None),
            "has_media": bool(message.media),
            "image_path": (
                str(image_path)
                if image_path else None
            )
        })

    
    for date_partition, messages in messages_by_date.items():

        partition_dir = (
            PROJECT_ROOT /
            "data" /
            "raw" /
            "telegram_messages" /
            date_partition
        )

        partition_dir.mkdir(
            parents=True,
            exist_ok=True
        )

        output_file = (
            partition_dir /
            f"{channel_name}.json"
        )

        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(
                messages,
                f,
                ensure_ascii=False,
                indent=2,
                default=str
            )
        logger.info(
            f"Saved {len(messages)} messages "
            f"for channel '{channel_name}' "
            f"on {date_partition}"
        )
    total_messages = sum(
        len(messages)
        for messages in messages_by_date.values()
    )
    logger.info(
    f"Finished scraping '{channel_name}'. "
    f"Total messages: {total_messages} "
    f"across: {len(messages_by_date)} dates"
)


async def main():

    await client.start()

    for channel in CHANNELS:
        try:
            await scrape_channel(channel)
        except Exception as e:
            logger.exception(
            f"Failed to scrape channel '{channel}'"
        )

    await client.disconnect()


if __name__ == "__main__":
    asyncio.run(main())