---
title: Coin Detection AI
emoji: 🪙
colorFrom: blue
colorTo: purple
sdk: fastapi
sdk_version: "0.110.0"
app_file: app.py
pinned: false
license: mit
---

# Coin Detection AI Service

FastAPI service for detecting coins in images using YOLOv8.

## Usage

```python
import requests

# Upload image for coin detection
with open("coin_image.jpg", "rb") as f:
    response = requests.post("https://your-space.hf.space/api/process-image", files={"file": f})
    result = response.json()
```

## Model

- Uses YOLOv8 custom model trained on coin images
- Detects coin types: 0.25, 0.5, 1, 2, 5, 10 units
- Returns bounding boxes, confidence scores, and total value

## API Endpoints

### POST /api/process-image
Upload an image file for coin detection.

**Response:**
```json
{
  "count": 5,
  "totalValue": 18.25,
  "details": [...],
  "coins": [...],
  "labeledImage": "data:image/jpeg;base64,..."
}
```
