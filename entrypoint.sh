#!/bin/bash
set -e
export PYTHONPATH=$PYTHONPATH:'/src/vision_app/'

python yolo_detector.py

exec "$@"
