#!/usr/bin/env python3
"""
Start both backend and frontend with dynamic port assignment
"""

import os
import sys
import subprocess
import time
import signal
import threading
from pathlib import Path

class AppStarter:
    def __init__(self):
        self.backend_process = None
        self.frontend_process = None
        self.backend_port = None
        self.frontend_port = None
        
    def find_free_port(self):
        """Find a free port automatically."""
        import socket
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('', 0))
            s.listen(1)
            port = s.getsockname()[1]
        return port
    
    def start_backend(self):
        """Start the backend server."""
        backend_dir = Path(__file__).parent / 'backend'
        os.chdir(backend_dir)
        
        # Set PYTHONPATH
        env = os.environ.copy()
        env['PYTHONPATH'] = '.'
        
        print("🚀 Starting Habit Loop Backend...")
        
        # Start backend with dynamic port
        self.backend_process = subprocess.Popen([
            sys.executable, 'app/main.py'
        ], env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        
        # Read output to get port
        for line in iter(self.backend_process.stdout.readline, ''):
            print(f"[Backend] {line.strip()}")
            if 'Server running on:' in line:
                # Extract port from line
                import re
                match = re.search(r':(\d+)', line)
                if match:
                    self.backend_port = match.group(1)
                    print(f"✅ Backend started on port {self.backend_port}")
                    break
    
    def start_frontend(self):
        """Start the frontend server."""
        frontend_dir = Path(__file__).parent / 'frontend'
        os.chdir(frontend_dir)
        
        print("🎨 Starting Habit Loop Frontend...")
        
        # Start frontend with dynamic port
        self.frontend_process = subprocess.Popen([
            'npm', 'run', 'dev:dynamic'
        ], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        
        # Read output to get port
        for line in iter(self.frontend_process.stdout.readline, ''):
            print(f"[Frontend] {line.strip()}")
            if 'Frontend running on:' in line:
                # Extract port from line
                import re
                match = re.search(r':(\d+)', line)
                if match:
                    self.frontend_port = match.group(1)
                    print(f"✅ Frontend started on port {self.frontend_port}")
                    break
    
    def start(self):
        """Start both backend and frontend."""
        try:
            print("🚀 Starting Habit Loop Application...")
            print("=" * 60)
            
            # Start backend in a separate thread
            backend_thread = threading.Thread(target=self.start_backend)
            backend_thread.daemon = True
            backend_thread.start()
            
            # Wait a bit for backend to start
            time.sleep(3)
            
            # Start frontend in a separate thread
            frontend_thread = threading.Thread(target=self.start_frontend)
            frontend_thread.daemon = True
            frontend_thread.start()
            
            # Wait a bit for frontend to start
            time.sleep(3)
            
            # Print summary
            print("\n" + "=" * 60)
            print("🎉 Habit Loop Application Started Successfully!")
            print("=" * 60)
            if self.backend_port:
                print(f"📡 Backend API: http://localhost:{self.backend_port}")
                print(f"📚 API Docs: http://localhost:{self.backend_port}/docs")
            if self.frontend_port:
                print(f"🎨 Frontend: http://localhost:{self.frontend_port}")
            print("=" * 60)
            print("Press Ctrl+C to stop both servers")
            
            # Keep the main thread alive
            while True:
                time.sleep(1)
                
        except KeyboardInterrupt:
            print("\n🛑 Shutting down servers...")
            self.stop()
    
    def stop(self):
        """Stop both servers."""
        if self.backend_process:
            self.backend_process.terminate()
        if self.frontend_process:
            self.frontend_process.terminate()
        print("✅ Servers stopped")

def main():
    starter = AppStarter()
    
    # Handle Ctrl+C gracefully
    def signal_handler(sig, frame):
        starter.stop()
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    
    starter.start()

if __name__ == "__main__":
    main()
