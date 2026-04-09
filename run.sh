#!/bin/bash

# FoodHub - Online Food Ordering System
# Setup and run script for Linux/Mac

echo ""
echo "============================================"
echo "   FoodHub - Online Food Ordering System"
echo "============================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python3 is not installed"
    echo "Please install Python 3.7+ using:"
    echo "  Ubuntu/Debian: sudo apt-get install python3 python3-pip"
    echo "  macOS: brew install python3"
    exit 1
fi

echo "[1/3] Installing dependencies..."
python3 -m pip install --user -r requirements.txt
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install dependencies"
    exit 1
fi

echo ""
echo "[2/3] Database will be initialized on first run..."
echo ""
echo "[3/3] Starting FoodHub server..."
echo ""
echo "============================================"
echo "   Server is running at http://localhost:5000"
echo "   Open your browser and navigate to the URL above"
echo "============================================"
echo ""

python3 app.py
