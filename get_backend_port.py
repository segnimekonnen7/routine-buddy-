#!/usr/bin/env python3
"""Get the current backend port from running processes."""

import subprocess
import re
import sys

def get_backend_port():
    """Get the port of the running backend server."""
    try:
        # Get all uvicorn processes
        result = subprocess.run(['ps', 'aux'], capture_output=True, text=True)
        lines = result.stdout.split('\n')
        
        for line in lines:
            if 'uvicorn' in line and 'app.main:app' in line:
                # Extract port from the command line
                port_match = re.search(r'--port\s+(\d+)', line)
                if port_match:
                    return int(port_match.group(1))
        
        # If no port found, return default
        return 8000
    except Exception as e:
        print(f"Error getting backend port: {e}", file=sys.stderr)
        return 8000

if __name__ == "__main__":
    port = get_backend_port()
    print(port)
