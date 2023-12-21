# Copyright (c) 2023 Dmitry Rogozhkin
# SPDX-License-Identifier: Apache-2.0

ARG IMAGE=ubuntu:22.04
FROM $IMAGE

RUN apt-get update && \
  DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
    ca-certificates \
    gcc \
    g++ \
    cmake \
    git \
    libomp-dev \
    ninja-build \
    python3 \
    python3-dev \
    python3-pip \
  && rm -rf /var/lib/apt/lists/*

ARG PYTORCH_VER=v2.1.1
RUN cd /opt && \
  git clone -b $PYTORCH_VER --depth 1 https://github.com/pytorch/pytorch && cd pytorch && \
  git submodule update --init --recursive --depth 1

RUN cd /opt/pytorch && \
  python3 -m pip install --upgrade pip && \
  python3 -m pip install -r requirements.txt

ENV _GLIBCXX_USE_CXX11_ABI=1

RUN cd /opt/pytorch && \
  python3 setup.py develop

#ENV PATH=/opt/iree/_build/tools/:$PATH

