import os
import sys
import uvicorn

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
YOLOV5_DIR = os.path.join(ROOT_DIR, "yolov5")

if YOLOV5_DIR not in sys.path:
    sys.path.append(YOLOV5_DIR)

APP_DIR = os.path.join(ROOT_DIR, "app")
if APP_DIR not in sys.path:
    sys.path.append(APP_DIR)

from app.model_validation import ModelValidation
from app.constant import LOCAL_MODEL_PATH
from app.logger import logging

def run():
    logging.info("Starting deployment pipeline")

    mv = ModelValidation(LOCAL_MODEL_PATH)
    if not mv.validate():
        raise Exception(" Model validation failed")

    logging.info("Model validation passed. Starting API server...")

    uvicorn.run(
        "app.app:app",
        host="0.0.0.0",
        port=8000,
        reload=False
    )

if __name__ == "__main__":
    run()
