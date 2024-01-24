#!/bin/bash
# Set the '-e' option to exit immediately if any command exits with a non-zero status.
set -e

# Add the '/src/vision_app/' directory to the Python module search path.
export PYTHONPATH=$PYTHONPATH:'/src/vision_app/'

# Run the Python script 'yolo_detector.py' using Python 3.
python3 yolo_detector.py

# Execute any additional commands or scripts passed as arguments to this bash script.
exec "$@"
