# Copyright (c) 2023 Dmitry Rogozhkin
# SPDX-License-Identifier: Apache-2.0

ARG IMAGE=ubuntu:22.04
FROM $IMAGE

RUN apt-get update && \
  DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
    ca-certificates \
    cmake \
    g++ \
    cmake \
    gcc \
    git \
    libomp-dev \
    ninja-build \
    python3 \
    python3-dev \
    python3-pip \
    python-is-python3 \
  && rm -rf /var/lib/apt/lists/*

ARG SHADERC_VER=main
RUN cd /opt && \
  git clone -b $SHADERC_VER --depth 1 https://github.com/google/shaderc.git

WORKDIR /opt/shaderc

RUN ./utils/git-sync-deps

# Note: available in Ubuntu >=23.04
RUN cmake -B _build -G Ninja \
    -DCMAKE_BUILD_TYPE=Release \
    -DCMAKE_INSTALL_PREFIX=/opt/install \
    -DSHADERC_SKIP_COPYRIGHT_CHECK=ON \
  && ninja -C _build \
  && ninja -C _build install

ARG PYTORCH_VER=v2.1.1
RUN cd /opt && \
  git clone -b $PYTORCH_VER --depth 1 https://github.com/pytorch/pytorch && cd pytorch && \
  git submodule update --init --recursive --depth 1

RUN cd /opt/pytorch && \
  python3 -m pip install --upgrade pip && \
  python3 -m pip install -r requirements.txt

RUN apt-get update && \
  DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
    libvulkan-dev \
  && rm -rf /var/lib/apt/lists/*


ENV PATH=/opt/install/bin:$PATH
ENV _GLIBCXX_USE_CXX11_ABI=1
ENV USE_VULKAN=1

RUN cd /opt/pytorch && \
  python3 setup.py develop

