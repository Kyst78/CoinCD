from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from ultralytics import YOLO
from PIL import Image, ImageDraw, ImageFont
import io
import base64
import uvicorn
import random
import os

app = FastAPI()

# CORS for Vercel
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load model
model = YOLO("best.pt")

COIN_VALUES = {
    "025": 0.25,
    "050": 0.5,
    "1": 1,
    "2": 2,
    "5": 5,
    "10": 10,
}

CLASS_COLORS = {
    "025": (255, 99, 132),
    "050": (54, 162, 235),
    "1": (255, 205, 86),
    "2": (75, 192, 192),
    "5": (153, 102, 255),
    "10": (255, 159, 64),
}

def get_class_color(class_name):
    return CLASS_COLORS.get(class_name, (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))

def crop_and_encode(image: Image.Image, box: list):
    cropped = image.crop((box[0], box[1], box[2], box[3]))
    buffered = io.BytesIO()
    cropped.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    return f"data:image/jpeg;base64,{img_str}"

def draw_boxes(image: Image.Image, boxes: list, labels: list, confidences: list = None):
    draw = ImageDraw.Draw(image)
    try:
        font = ImageFont.truetype("arial.ttf", 20)
    except:
        font = ImageFont.load_default()

    for i, (box, label) in enumerate(zip(boxes, labels)):
        x1, y1, x2, y2 = map(int, box)
        color = get_class_color(label)
        draw.rectangle([x1, y1, x2, y2], outline=color, width=3)
        
        display_text = f"{label}"
        if confidences and i < len(confidences):
            display_text += f" ({confidences[i]:.2f})"

        bbox = draw.textbbox((0, 0), display_text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        text_bg_x1 = x1
        text_bg_y1 = y1 - text_height - 8
        text_bg_x2 = x1 + text_width + 8
        text_bg_y2 = y1

        if text_bg_y1 < 0:
            text_bg_y1 = y2
            text_bg_y2 = y2 + text_height + 8

        draw.rectangle([text_bg_x1, text_bg_y1, text_bg_x2, text_bg_y2], fill=color)
        draw.text((text_bg_x1 + 4, text_bg_y1 + 4), display_text, fill="white", font=font)

    return image

@app.get("/", response_class=HTMLResponse)
async def root():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Coin Detection AI</title>
        <style>
            body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
            .upload-area { border: 2px dashed #ccc; padding: 20px; text-align: center; margin: 20px 0; }
            .result { margin: 20px 0; }
            img { max-width: 100%; height: auto; }
        </style>
    </head>
    <body>
        <h1>🪙 Coin Detection AI</h1>
        <p>Upload an image to detect and count coins using YOLOv8</p>
        
        <div class="upload-area">
            <input type="file" id="fileInput" accept="image/*">
            <button onclick="detectCoins()">Detect Coins</button>
        </div>
        
        <div id="result" class="result"></div>
        
        <script>
            async function detectCoins() {
                const fileInput = document.getElementById('fileInput');
                const result = document.getElementById('result');
                
                if (!fileInput.files[0]) {
                    alert('Please select an image');
                    return;
                }
                
                const formData = new FormData();
                formData.append('file', fileInput.files[0]);
                
                result.innerHTML = '<p>Detecting coins...</p>';
                
                try {
                    const response = await fetch('/api/process-image', {
                        method: 'POST',
                        body: formData
                    });
                    
                    const data = await response.json();
                    
                    result.innerHTML = `
                        <h2>Results:</h2>
                        <p><strong>Coins found:</strong> ${data.count}</p>
                        <p><strong>Total value:</strong> $${data.totalValue}</p>
                        <h3>Annotated Image:</h3>
                        <img src="${data.labeledImage}" alt="Detected coins" />
                    `;
                } catch (error) {
                    result.innerHTML = '<p>Error: ' + error.message + '</p>';
                }
            }
        </script>
    </body>
    </html>
    """

@app.post("/api/process-image")
async def process_image(file: UploadFile = File(...)):
    contents = await file.read()
    image = Image.open(io.BytesIO(contents)).convert("RGB")
    
    results = model(image)
    
    counts = {}
    details = []
    total_count = 0
    total_value = 0.0
    coins_with_images = []
    
    all_boxes = []
    all_labels = []
    all_confidences = []
    
    for result in results:
        for box, cls, conf in zip(result.boxes.xyxy, result.boxes.cls, result.boxes.conf):
            class_id = int(cls.item())
            class_name = model.names[class_id]
            box_list = box.tolist()
            confidence = conf.item()
            
            counts[class_name] = counts.get(class_name, 0) + 1
            cropped_img_base64 = crop_and_encode(image, box_list)
            
            coins_with_images.append({
                "type": class_name,
                "bbox": box_list,
                "confidence": confidence,
                "image": cropped_img_base64
            })
            
            all_boxes.append(box_list)
            all_labels.append(class_name)
            all_confidences.append(confidence)
    
    labeled_image = draw_boxes(image.copy(), all_boxes, all_labels, all_confidences)
    
    buffered = io.BytesIO()
    labeled_image.save(buffered, format="JPEG", quality=95)
    labeled_base64 = base64.b64encode(buffered.getvalue()).decode()
    
    for coin_type, count in counts.items():
        value = COIN_VALUES.get(coin_type, 0) * count
        details.append({
            "type": coin_type,
            "count": count,
            "value": value,
            "color": CLASS_COLORS.get(coin_type, (128, 128, 128))
        })
        total_count += count
        total_value += value
    
    return {
        "count": total_count,
        "totalValue": total_value,
        "details": details,
        "coins": coins_with_images,
        "labeledImage": f"data:image/jpeg;base64,{labeled_base64}",
        "classColors": CLASS_COLORS
    }

if __name__ == "__main__":
    port = int(os.getenv("PORT", "7860"))
    uvicorn.run(app, host="0.0.0.0", port=port)
