# 🪙 CoinCD - TH Coin Detection App

AI-powered coin detection application using YOLOv8 and FastAPI.

## Features

- **AI Detection**: Detect coins in images using YOLOv8
- **Value Calculation**: Automatically calculate total coin value
- **History Tracking**: Track and manage detection history
- **Report Generation**: Generate reports from selected history
- **Authentication**: Email/password and GitHub OAuth login
- **Delete History**: Remove unwanted detection records

## Architecture

- **Frontend**: Nuxt 3 (Vue 3) - Deployed on Vercel
- **Backend**: FastAPI + YOLOv8 - Deployed on Hugging Face Spaces
- **Database**: MongoDB Atlas
- **AI Model**: Custom YOLOv8 trained on coin images

## Setup

### Prerequisites
- Node.js 18+
- MongoDB Atlas account
- Hugging Face account (for backend deployment)

### 1. Clone and Install
```bash
git clone https://github.com/Kyst78/CountCoin.git
cd CountCoin
pnpm install
```

### 2. Environment Variables
Copy `.env.example` to `.env` and configure:

```bash
# Database
DATABASE_URL="mongodb+srv://..."

# AI Service (HF Spaces)
NUXT_AI_SERVICE_URL="https://your-space.hf.space"

# Authentication
NUXT_SESSION_PASSWORD="random_32_char_string"
NUXT_OAUTH_GITHUB_CLIENT_ID="github_client_id"
NUXT_OAUTH_GITHUB_CLIENT_SECRET="github_client_secret"

# Cloudinary (optional)
NUXT_PUBLIC_CLOUDINARY_CLOUD_NAME="..."
NUXT_PUBLIC_UPLOAD_PRESET="..."
NUXT_CLOUDINARY_API_KEY="..."
NUXT_CLOUDINARY_API_SECRET="..."
```

### 3. Database Setup
```bash
npx prisma db push
npx prisma generate
```

### 4. Development
```bash
pnpm dev
```

## Deployment

### Frontend (Vercel)
1. Connect GitHub repo to Vercel
2. Set environment variables in Vercel dashboard
3. Deploy automatically

### Backend (Hugging Face Spaces)
1. Create new Space: https://huggingface.co/spaces
2. Upload files from `/python` folder:
   - `simple_app.py`
   - `requirements.txt`
   - `best.pt`
   - `README.md`
3. Set HF Spaces configuration to use Gradio SDK
4. Deploy and copy the URL

## API Endpoints

### Backend (FastAPI)
- `POST /api/process-image` - Upload image for coin detection

### Frontend (Nuxt)
- `GET /api/history` - Get user history
- `POST /api/history` - Save detection result
- `DELETE /api/history/[id]` - Delete history item

## Supported Coins

- 0.25, 0.5, 1, 2, 5, 10 units

## Tech Stack

- **Frontend**: Nuxt 3, Vue 3, TailwindCSS, Nuxt UI
- **Backend**: FastAPI, Uvicorn, OpenCV, Ultralytics
- **Database**: MongoDB, Prisma
- **Deployment**: Vercel, Hugging Face Spaces
- **Authentication**: Nuxt Auth Utils

## Contributing

1. Fork the repository
2. Create feature branch
3. Commit changes
4. Push to branch
5. Create Pull Request

## License

MIT License
