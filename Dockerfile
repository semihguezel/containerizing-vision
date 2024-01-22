FROM nvidia/cuda:12.3.1-devel-ubuntu22.04

ARG DEBIAN_FRONTEND=noninteractive

ENV TERM=xterm

RUN echo $PATH
RUN export LD_LIBRARY_PATH=/usr/local/cuda-12.3/lib64${LD_LIBRARY_PATH:+:${LD_LIBRARY_PATH}}; echo $PATH
RUN echo $PATH

ENV NVIDIA_VISIBLE_DEVICES ${NVIDIA_VISIBLE_DEVICES:-all}
ENV NVIDIA_DRIVER_CAPABILITIES ${NVIDIA_DRIVER_CAPABILITIES:+$NVIDIA_DRIVER_CAPABILITIES,}graphics
ENV NVIDIA_DRIVER_CAPABILITIES=compute,utility

RUN pip install ultralytics

RUN mkdir -p /src

COPY entrypoint.sh /src

COPY /vision_app /src/vision_app

WORKDIR  /src/vision_app/

COPY ./entrypoint.sh /src
ENTRYPOINT ["/src/entrypoint.sh"]
SHELL ["/bin/bash"]
