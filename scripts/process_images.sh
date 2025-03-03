#!/bin/bash

echo "🖼️ Running AI processing pipeline..."
cd ai-processing || exit
source venv/bin/activate
python pipeline.py
