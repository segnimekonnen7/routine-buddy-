#!/usr/bin/env python3
"""Start the backend with dynamic port assignment."""

import os
import sys
import subprocess
import time

def start_backend():
    """Start the backend server with dynamic port."""
    # Set the Python path
    backend_dir = os.path.join(os.path.dirname(__file__), 'backend')
    os.chdir(backend_dir)
    
    # Set PYTHONPATH
    env = os.environ.copy()
    env['PYTHONPATH'] = '.'
    
    print("🚀 Starting Habit Loop Backend with Dynamic Port...")
    
    # Start the server
    process = subprocess.Popen([
        sys.executable, 'app/main.py'
    ], env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    
    # Read the output to get the port
    port = None
    for line in iter(process.stdout.readline, ''):
        print(line.strip())
        if 'Server running on:' in line:
            # Extract port from line like "📡 Server running on: http://0.0.0.0:54785"
            import re
            match = re.search(r':(\d+)', line)
            if match:
                port = match.group(1)
                break
    
    if port:
        print(f"\n✅ Backend started successfully on port {port}")
        print(f"📚 API Docs: http://localhost:{port}/docs")
        return port
    else:
        print("❌ Failed to start backend")
        return None

if __name__ == "__main__":
    start_backend()
