import torch
import cv2
import os

# ---------------- PATH CONFIG ----------------
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
YOLOV5_DIR = os.path.join(ROOT_DIR, "yolov5")
MODEL_PATH = os.path.join(ROOT_DIR, "artifacts", "best.pt")
IMAGE_PATH = os.path.join(ROOT_DIR, "test2.jpg")  # 👈 put your test image here

# ---------------- SANITY CHECK ----------------
if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(f"Model not found: {MODEL_PATH}")

if not os.path.exists(IMAGE_PATH):
    raise FileNotFoundError(f"Image not found: {IMAGE_PATH}")

print("📁 Model Path:", MODEL_PATH)
print("🖼 Image Path:", IMAGE_PATH)

# ---------------- LOAD MODEL ----------------
print("⏳ Loading YOLOv5 model...")

model = torch.hub.load(
    YOLOV5_DIR,
    "custom",
    path=MODEL_PATH,
    source="local"
)

model.conf = 0.05   # VERY LOW threshold for debugging
model.iou = 0.3

print("✅ Model loaded successfully")

# ---------------- LOAD IMAGE ----------------
image = cv2.imread(IMAGE_PATH)
if image is None:
    raise ValueError("Failed to load image")

print("🧠 Running inference...")

# ---------------- RUN INFERENCE ----------------
results = model(image)

# ---------------- PRINT RAW OUTPUT ----------------
df = results.pandas().xyxy[0]
print("\n🔎 RAW DETECTIONS:")
print(df)

# ---------------- VISUAL OUTPUT ----------------
annotated_image = results.render()[0]

cv2.imshow("Sign Language Detection - Image Test", annotated_image)
cv2.waitKey(0)
cv2.destroyAllWindows()

print("👋 Done")
