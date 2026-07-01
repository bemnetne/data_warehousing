from ultralytics import YOLO
from pathlib import Path
import pandas as pd

# Load YOLO Model
# ----------------------------------------------------
model = YOLO("yolov8n.pt")

# Project Paths
# ----------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parent.parent

IMAGES_DIR = (
    PROJECT_ROOT /
    "data" /
    "raw" /
    "images"
)

OUTPUT_DIR = (
    PROJECT_ROOT /
    "data" /
    "processed"
)

OUTPUT_DIR.mkdir(exist_ok=True)
OUTPUT_CSV = OUTPUT_DIR / "detections_raw.csv"
# Detection Results
# ----------------------------------------------------

detections = []

# ----------------------------------------------------
# Scan Images
# ----------------------------------------------------

image_files = list(IMAGES_DIR.rglob("*.jpg"))

print(f"Found {len(image_files)} images")

# ----------------------------------------------------
# Run Detection
# ----------------------------------------------------

for image_path in image_files:

    print(f"Processing {image_path.name}")

    channel_name = image_path.parent.name

    message_id = image_path.stem

    results = model(image_path)

    for result in results:

        boxes = result.boxes

        for box in boxes:

            class_id = int(box.cls[0])

            confidence = float(box.conf[0])

            object_name = model.names[class_id]

            detections.append({

                "message_id": message_id,

                "channel_name": channel_name,

                "image_path": str(image_path),

                "detected_object": object_name,

                "confidence_score": round(confidence, 4)

            })

# ----------------------------------------------------
# Save CSV
# ----------------------------------------------------

df = pd.DataFrame(detections)
df.to_csv(
    OUTPUT_CSV,
    index=False
)


