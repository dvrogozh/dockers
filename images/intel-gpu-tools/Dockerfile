# Copyright (c) 2023 Dmitry Rogozhkin
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions
# and limitations under the License.
#
# SPDX-License-Identifier: Apache-2.0

ARG IMAGE=ubuntu:22.04
FROM $IMAGE as build

RUN apt-get update && \
  DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
    bison \
    ca-certificates \
    flex \
    gcc \
    git \
    libcairo-dev \
    libdrm-dev \
    libdw-dev \
    libkmod-dev \
    libpciaccess-dev \
    libpixman-1-dev \
    libprocps-dev \
    libudev-dev \
    meson \
    pkg-config && \
  rm -rf /var/lib/apt/lists/*

ARG IGT_REPO=https://gitlab.freedesktop.org/drm/igt-gpu-tools.git
ARG IGT_VER=v1.28

RUN git clone $IGT_REPO /opt/igt && cd /opt/igt \
  && git checkout $IGT_VER

RUN cd /opt/igt && meson setup _build \
    --buildtype=release \
    --prefix=/opt/intel/ \
    --libdir=/opt/intel/lib \
    -Ddocs=disabled \
    -Dlibdrm_drivers=intel \
    -Dman=disabled \
    -Doverlay=disabled \
    -Drunner=disabled \
    -Dtests=disabled \
  && meson compile -C _build \
  && meson install -C _build --destdir=/opt/dist \
  && cd /opt && rm -rf igt

FROM $IMAGE as runtime

RUN apt-get update && \
  DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
    libdrm2 \
    libglib2.0-0 \
  && rm -rf /var/lib/apt/lists/*

COPY --from=build /opt/dist /
ENV PATH=/opt/intel/bin:$PATH

