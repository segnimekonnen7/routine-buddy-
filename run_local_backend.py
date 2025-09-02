#!/usr/bin/env python3
"""
Local Backend Runner for Habit Loop
Run this to get the full version working locally!
"""

import subprocess
import sys
import os

def main():
    print("🚀 Starting Habit Loop Backend Locally...")
    print("📡 This will give you the FULL version with live data!")
    print("🌐 Your app will connect to: http://localhost:8000")
    print("")
    
    # Check if uvicorn is installed
    try:
        import uvicorn
        print("✅ Uvicorn is available")
    except ImportError:
        print("❌ Uvicorn not found. Installing...")
        subprocess.run([sys.executable, "-m", "pip", "install", "uvicorn[standard]"])
        print("✅ Uvicorn installed!")
    
    # Check if fastapi is installed
    try:
        import fastapi
        print("✅ FastAPI is available")
    except ImportError:
        print("❌ FastAPI not found. Installing...")
        subprocess.run([sys.executable, "-m", "pip", "install", "fastapi"])
        print("✅ FastAPI installed!")
    
    print("")
    print("🔧 Starting backend server...")
    print("📱 Open your app and change the API URL to: http://localhost:8000")
    print("🔄 The app will automatically connect to your local backend!")
    print("")
    print("Press Ctrl+C to stop the server")
    print("=" * 50)
    
    # Start the backend
    try:
        from simple_backend import app
        import uvicorn
        uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
    except Exception as e:
        print(f"❌ Error starting backend: {e}")
        print("🔧 Trying alternative method...")
        
        # Alternative: run as module
        try:
            subprocess.run([
                sys.executable, "-m", "uvicorn", 
                "simple_backend:app", 
                "--host", "127.0.0.1", 
                "--port", "8000", 
                "--reload"
            ])
        except KeyboardInterrupt:
            print("\n🛑 Backend stopped by user")
        except Exception as e2:
            print(f"❌ Alternative method also failed: {e2}")
            print("🔧 Please check the error messages above")

if __name__ == "__main__":
    main()
