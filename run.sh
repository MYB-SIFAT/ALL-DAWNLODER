#!/bin/bash
echo "======================================"
echo "  StreamVault - Starting Server"
echo "======================================"
mkdir -p downloads temp
pip3 install -r requirements.txt --break-system-packages 2>/dev/null || pip3 install -r requirements.txt
echo ""
echo "Server starting..."
echo "Open: http://localhost:5000"
echo ""
python3 main.py
