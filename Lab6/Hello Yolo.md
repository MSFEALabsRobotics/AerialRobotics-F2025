# 🧠 Hello World YOLO (Ultralytics YOLO11)

This short guide will help you get started with **YOLO** (You Only Look Once) — one of the fastest and most accurate object detection models.

---

## ⚙️ 1. Install YOLO

Install the official Ultralytics package using `pip`:

```bash
pip install ultralytics
```

---

## 📦 2. Explore Available Models

You can find all supported YOLO11 models (Nano, Small, Medium, etc.) at:

🔗 [https://docs.ultralytics.com/models/yolo11/#supported-tasks-and-modes](https://docs.ultralytics.com/models/yolo11/#supported-tasks-and-modes)

---

## 💻 3. Hello World Example (Windows or WSL)

Create a Python file `hello_yolo.py`:

```python
from ultralytics import YOLO

# Load a pretrained YOLO model (recommended for inference or training)
model = YOLO("yolo11n.pt")

# Print the class names
print(model.names)

# Perform object detection on an image
results = model("bus.jpg")

# Display the detection results
results[0].show()
```

### 🐍 Run the script:
```bash
python hello_yolo.py
```

If everything is installed correctly, a window will open showing detections (bounding boxes and class labels).

---

## 🍓 . YOLO on Raspberry Pi (Optional)

To deploy YOLO efficiently on a Raspberry Pi, you can **convert the model to NCNN** format for edge inference.

Guide:  
🔗 [https://docs.ultralytics.com/guides/raspberry-pi/#convert-model-to-ncnn-and-run-inference](https://docs.ultralytics.com/guides/raspberry-pi/#convert-model-to-ncnn-and-run-inference)

---

