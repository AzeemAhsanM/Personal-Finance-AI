#!/usr/bin/env bash
# Exit on error
set -o errexit  

# --- Build React frontend ---
cd frontend
npm install
npm run build

# --- Move build files to backend/static ---
mkdir -p ../backend/app/static
cp -r build/* ../backend/app/static/

# --- Back to backend ---
cd ../backend
pip install -r requirements.txt

# --- Start FastAPI app with Uvicorn ---
# uvicorn app.main:app --host 0.0.0.0 --port 8000
