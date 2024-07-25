#!/bin/bash
# This script will start ttyd and then run the Python script

# Start ttyd to serve the Python script
ttyd -i 0.0.0.0 -p 80 /venv/bin/python3 /app/script.py
