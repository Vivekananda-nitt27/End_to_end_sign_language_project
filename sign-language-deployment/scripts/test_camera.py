import cv2
import torch
import os

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
YOLOV5_DIR = os.path.join(ROOT_DIR, "yolov5")

model = torch.hub.load(
    YOLOV5_DIR,
    "custom",
    path="artifacts/best.pt",
    source="local"
)

model.conf = 0.005
model.iou = 0.45

cap = cv2.VideoCapture(0)

print("📷 Press Q to quit camera")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    results = model(frame)
    df = results.pandas().xyxy[0]

    if not df.empty:
        best = df.sort_values("confidence", ascending=False).iloc[0]

        label = best["name"]
        conf = round(float(best["confidence"]), 2)

        x1, y1, x2, y2 = map(int, [best["xmin"], best["ymin"], best["xmax"], best["ymax"]])

        cv2.rectangle(frame, (x1, y1), (x2, y2), (0,255,0), 2)
        cv2.putText(frame, f"{label} {conf}", (x1, y1-10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,0), 2)

    cv2.imshow("Sign Language Detector", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
