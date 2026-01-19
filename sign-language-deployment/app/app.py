import torch
import tempfile
import sys
import os
from fastapi import FastAPI, UploadFile, File
from PIL import Image
import io
import numpy as np
import cv2

from app.s3_operations import S3Operation
from app.constant import MODEL_PUSHER_BUCKET_NAME, MODEL_PUSHER_S3_MODEL_KEY
from app.logger import logging

app = FastAPI(title="Sign Language Detection API")
model = None


@app.on_event("startup")
def load_model():
    global model

    try:
        logging.info("Starting model load from S3...")

        ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        YOLOV5_DIR = os.path.join(ROOT_DIR, "yolov5")
        sys.path.append(YOLOV5_DIR)

        s3 = S3Operation()
        model_bytes = s3.read_object(
            bucket_name=MODEL_PUSHER_BUCKET_NAME,
            object_name=MODEL_PUSHER_S3_MODEL_KEY,
            decode=False
        )

        with tempfile.NamedTemporaryFile(delete=False, suffix=".pt") as f:
            f.write(model_bytes)
            model_path = f.name

        model = torch.hub.load(
            YOLOV5_DIR,
            "custom",
            path=model_path,
            source="local",
            force_reload=False
        )

        # 🔥 IMPORTANT: override YOLO default filters
        model.conf = 0.005    # keep ultra-low confidence boxes
        model.iou = 0.45
        model.max_det = 10

        model.eval()
        print("✅ YOLOv5 model loaded successfully with low conf threshold")

    except Exception as e:
        logging.error(f"Model loading failed: {e}")
        model = None


# 🔥 HEALTH CHECK
@app.get("/")
def health():
    return {"status": "ok", "message": "Sign Language API is running"}


# 🔥 PREDICTION ENDPOINT
@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    global model

    if model is None:
        return {"error": "Model not loaded"}

    image_bytes = await file.read()
    np_img = np.frombuffer(image_bytes, np.uint8)
    image = cv2.imdecode(np_img, cv2.IMREAD_COLOR)

    results = model(image)
    df = results.pandas().xyxy[0]

    # Keep ultra-low confidence
    df = df[df["confidence"] >= 0.005]

    if df.empty:
        return {"label": "No sign detected", "confidence": 0}

    best = df.sort_values("confidence", ascending=False).iloc[0]

    return {
        "label": best["name"],
        "confidence": float(best["confidence"]),
        "bbox": {
            "xmin": float(best["xmin"]),
            "ymin": float(best["ymin"]),
            "xmax": float(best["xmax"]),
            "ymax": float(best["ymax"]),
        }
    }
