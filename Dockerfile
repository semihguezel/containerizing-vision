# Use the official NVIDIA CUDA image as the base image with version 12.3.1 for development on Ubuntu 22.04
FROM nvidia/cuda:12.3.1-devel-ubuntu22.04

# Set non-interactive mode for Debian package installations
ARG DEBIAN_FRONTEND=noninteractive

# Set the environment variable TERM to xterm
ENV TERM=xterm

# Add /usr/local/cuda-12.3/lib64 to the LD_LIBRARY_PATH environment variable and print the PATH
RUN export LD_LIBRARY_PATH=/usr/local/cuda-12.3/lib64${LD_LIBRARY_PATH:+:${LD_LIBRARY_PATH}}; echo $PATH

# Set NVIDIA_VISIBLE_DEVICES, NVIDIA_DRIVER_CAPABILITIES for GPU visibility and capabilities
ENV NVIDIA_VISIBLE_DEVICES ${NVIDIA_VISIBLE_DEVICES:-all}
ENV NVIDIA_DRIVER_CAPABILITIES ${NVIDIA_DRIVER_CAPABILITIES:+$NVIDIA_DRIVER_CAPABILITIES,}graphics
ENV NVIDIA_DRIVER_CAPABILITIES=compute,utility

# Install the Ultralytics library using pip
RUN pip install ultralytics

# Create a directory /src in the container
RUN mkdir -p /src

# Copy the entrypoint.sh script to /src in the container
COPY entrypoint.sh /src

# Copy the /vision_app directory from the build context to /src/vision_app in the container
COPY /vision_app /src/vision_app

# Set the working directory to /src/vision_app/
WORKDIR /src/vision_app/

# Set the entry point for the container to /src/entrypoint.sh
ENTRYPOINT ["/src/entrypoint.sh"]

# Set the default shell for the Docker container to /bin/bash
SHELL ["/bin/bash"]
