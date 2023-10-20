# Copyright (c) 2023 Dmitry Rogozhkin
# SPDX-License-Identifier: Apache-2.0

ARG IMAGE=ubuntu:22.04
FROM $IMAGE as build

RUN apt-get update && \
  DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
    ca-certificates \
    clang \
    cmake \
    git \
    lld \
    ninja-build \
    python3 \
  && rm -rf /var/lib/apt/lists/*

ARG IREE_VER=20e2112cf149bb342e1d9bfe8f01229a674de1ab
RUN cd /opt && \
  git clone https://github.com/openxla/iree.git && cd iree && \
  git checkout $IREE_VER && \
  git submodule update --init

RUN cd /opt/iree && \
  cmake -G Ninja -B _build \
    -DCMAKE_INSTALL_PREFIX=/opt/install \
    -DCMAKE_BUILD_TYPE=RelWithDebInfo \
    -DCMAKE_C_COMPILER=clang \
    -DCMAKE_CXX_COMPILER=clang++ \
    -DIREE_ENABLE_ASSERTIONS=ON \
    -DIREE_ENABLE_SPLIT_DWARF=ON \
    -DIREE_ENABLE_THIN_ARCHIVES=ON \
    -DIREE_ENABLE_LLD=ON \
  && cmake --build _build \
  && DESTDIR=/opt/dist ninja -C _build install \
  && cd /opt && rm -rf iree

FROM $IMAGE as runtime

COPY --from=build /opt/dist /

RUN apt-get update && \
  DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
    mesa-utils \
    vulkan-tools \
    mesa-va-drivers \
    mesa-vdpau-drivers \
    mesa-vulkan-drivers \
    libegl-mesa0 \
    libegl1-mesa \
    libgl1-mesa-dri \
    libglapi-mesa \
    libglx-mesa0 \
  && rm -rf /var/lib/apt/lists/*

