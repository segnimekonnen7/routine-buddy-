#!/usr/bin/env python3
"""
Switch Frontend to Local Backend
This script updates the frontend to use your local backend for the FULL version!
"""

import os
import re

def update_frontend_api():
    """Update the frontend to use local backend."""
    
    # Path to the main index.html
    frontend_path = "../index.html"
    
    if not os.path.exists(frontend_path):
        print("❌ Frontend file not found. Make sure you're in the habit-loop directory.")
        return False
    
    print("🔧 Updating frontend to use local backend...")
    
    # Read the current frontend
    with open(frontend_path, 'r') as f:
        content = f.read()
    
    # Replace the API URL
    old_api = "https://routine-h9ig.onrender.com"
    new_api = "http://localhost:8000"
    
    if old_api in content:
        content = content.replace(old_api, new_api)
        
        # Write the updated content
        with open(frontend_path, 'w') as f:
            f.write(content)
        
        print("✅ Frontend updated successfully!")
        print(f"🔄 API URL changed from {old_api} to {new_api}")
        print("")
        print("📱 Now open your app and it will connect to your local backend!")
        print("🌐 Local backend should be running on: http://localhost:8000")
        return True
    else:
        print("❌ API URL not found in frontend. It might already be set to localhost.")
        return False

def main():
    print("🚀 Habit Loop - Switch to Local Backend")
    print("=" * 40)
    print("This will give you the FULL version with live data!")
    print("")
    
    # Check if we're in the right directory
    if not os.path.exists("simple_backend.py"):
        print("❌ simple_backend.py not found!")
        print("🔧 Please run this script from the habit-loop directory")
        return
    
    # Update the frontend
    if update_frontend_api():
        print("")
        print("🎯 Next steps:")
        print("1. Start your local backend: python run_local_backend.py")
        print("2. Open your app in the browser")
        print("3. The app will now connect to localhost:8000")
        print("4. You'll have the FULL version with live data!")
        print("")
        print("🔄 To switch back to deployed backend later:")
        print("   Change the API URL back to: https://routine-h9ig.onrender.com")
    else:
        print("❌ Failed to update frontend")

if __name__ == "__main__":
    main()
