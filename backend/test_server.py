#!/usr/bin/env python3
"""Simple test server to verify basic functionality."""

from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/health")
async def health():
    return {"status": "ok"}

if __name__ == "__main__":
    print("🚀 Starting Test Server...")
    print("📡 Server running on: http://127.0.0.1:8000")
    uvicorn.run(app, host="127.0.0.1", port=8000)
