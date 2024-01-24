#!/usr/bin/env bash
# Use the 'env' command to locate bash in the system's PATH.

# Allow root access to the local X server.
xhost local:root
XAUTH=/tmp/.docker.xauth

# Set variables for container and image names, and the base folder.
CONTAINER_NAME=containerizing_vision_container
IMAGE_NAME=containerizing_vision:tutorial
BASE_FOLDER=$PWD

# Run the Docker container with GPU support, X11 display forwarding, and other configurations.
docker run --log-opt max-size=10m --log-opt max-file=10 --rm -it \
    --name=$CONTAINER_NAME \
    --gpus all \
    --env="DISPLAY=$DISPLAY" \
    --env="QT_X11_NO_MITSHM=1" \
    --env="XAUTHORITY=$XAUTH" \
    --volume="$XAUTH:$XAUTH" \
    --volume="/tmp/.X11-unix:/tmp/.X11-unix:rw" \
    --volume="$BASE_FOLDER/entrypoint.sh:/src/entrypoint.sh" \
    --volume="$BASE_FOLDER/vision_app:/src/vision_app" \
    --net=host \
    --privileged \
    --runtime=nvidia \
    $IMAGE_NAME \
    bash

# Print a message indicating that the script execution is complete.
echo "Done."
