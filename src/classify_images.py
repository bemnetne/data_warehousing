from ultralytics import YOLO
from pathlib import Path
import pandas as pd
PROJECT_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = (
    PROJECT_ROOT /
    "data" /
    "processed"
)
filepath = (
    PROJECT_ROOT /
    "data" /
    "processed" /
    "detections_raw.csv"
)
df = pd.read_csv(filepath)
PRODUCT_OBJECTS = {
    "bottle",
    "cup",
    "bowl",
    "box",
    "vase"
}

classified_images = []

for (message_id, channel_name, image_path), group in df.groupby(
    ["message_id", "channel_name", "image_path"]
):

    detected_objects = set(group["detected_object"])

    has_person = "person" in detected_objects

    has_product = any(
        obj in PRODUCT_OBJECTS
        for obj in detected_objects
    )

    if has_person and has_product:
        image_category = "promotional"

    elif has_product:
        image_category = "product_display"

    elif has_person:
        image_category = "lifestyle"

    else:
        image_category = "other"

    classified_images.append({

        "message_id": message_id,

        "channel_name": channel_name,

        "image_path": image_path,

        "detected_objects": ", ".join(
            sorted(detected_objects)
        ),

        "confidence_score": round(
            group["confidence_score"].max(),
            4
        ),

        "image_category": image_category

    })
classified_df = pd.DataFrame(classified_images)
OUTPUT_CSV = OUTPUT_DIR / "detections.csv"

classified_df.to_csv(
    OUTPUT_CSV,
    index=False
)

print(
    f"Saved {len(classified_df)} classified images."
)