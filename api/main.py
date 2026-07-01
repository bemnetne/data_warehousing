from fastapi import FastAPI
from api.routes import router
app = FastAPI(
    title="Medical Warehouse API",
    description="""
REST API for querying analytical insights from the Medical Warehouse data warehouse.

The API provides endpoints for:
- Product frequency analysis
- Channel activity and trends
- Message keyword search
- Visual content statistics generated using YOLOv8
""",
    version="1.0.0",
)


@app.get("/")
def home():
    return {
        "message": "Medical Warehouse API is running"
    }

app.include_router(router)