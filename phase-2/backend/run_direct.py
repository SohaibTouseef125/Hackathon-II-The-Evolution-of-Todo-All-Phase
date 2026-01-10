#!/usr/bin/env python3
"""
Run the application directly without uvicorn
"""

import os
from dotenv import load_dotenv
load_dotenv()

# Import the main app
from main import app

# Run using uvicorn programmatically without multiprocessing
import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "run_direct:app",
        host="127.0.0.1",
        port=8000,
        reload=False  # Disable reload to avoid multiprocessing issues
    )