# Copyright (c) 2023 Dmitry Rogozhkin
# SPDX-License-Identifier: Apache-2.0

ARG IMAGE=ubuntu:22.04
FROM $IMAGE

RUN apt-get update && \
  DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
    ca-certificates \
    clang \
    cmake \
    git \
    lld \
    ninja-build \
    python3 \
    python3-dev \
    python3-pip \
  && rm -rf /var/lib/apt/lists/*

ARG IREE_VER=20e2112cf149bb342e1d9bfe8f01229a674de1ab
RUN cd /opt && \
  git clone https://github.com/openxla/iree.git && cd iree && \
  git checkout $IREE_VER && \
  git submodule update --init

RUN cd /opt/iree && \
  python3 -m pip install --upgrade pip && \
  python3 -m pip install -r runtime/bindings/python/iree/runtime/build_requirements.txt

RUN cd /opt/iree && \
  cmake -G Ninja -B _build \
    -DCMAKE_BUILD_TYPE=RelWithDebInfo \
    -DCMAKE_C_COMPILER=clang \
    -DCMAKE_CXX_COMPILER=clang++ \
    -DIREE_ENABLE_ASSERTIONS=ON \
    -DIREE_ENABLE_SPLIT_DWARF=ON \
    -DIREE_ENABLE_THIN_ARCHIVES=ON \
    -DIREE_ENABLE_LLD=ON \
    -DIREE_BUILD_PYTHON_BINDINGS=ON  \
    -DPython3_EXECUTABLE="$(which python3)" \
  && cmake --build _build

ENV PATH=/opt/iree/_build/tools/:$PATH

# Not using integrations/tensorflow/test/requirements.txt to make sure
# we install released version of TF to avoid possible regressions.
# python3 -m pip install tensorflow
# python3 -m pip install -r integrations/tensorflow/test/requirements.txt 
RUN cd /opt/iree && \
  python3 -m pip install tensorflow && \
  python3 -m pip install integrations/tensorflow/python_projects/iree_tf && \
  python3 -m pip install integrations/tensorflow/python_projects/iree_tflite

RUN sed -i 's/experimental_convert_saved_model_v1/experimental_convert_saved_model_v1_to_mlir/' \
  /usr/local/lib/python3.10/dist-packages/tensorflow/python/compiler/mlir/mlir.py

# Per IREE requirement we need to have saved model with the serving signature.
# The following helper script resaves given model with it.
# See: https://www.iree.dev/guides/ml-frameworks/tensorflow/#missing-serving-signature-in-savedmodel
COPY images/iree/tf/resave_1x224x224x3_f32.py /opt/

# This script just prints out model serving signature.
COPY images/iree/tf/print_signature.py /opt/

# vulkan arch to compile models for
ARG VULKAN_ARCH=arc-any-unknown

RUN apt-get update && \
  DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
    wget \
  && rm -rf /var/lib/apt/lists/*

#
# MOBILENET V2
#

RUN mkdir -p /opt/models/tf/mobilenet_v2 && cd /opt/models/tf/mobilenet_v2 && \
  wget -O - https://tfhub.dev/google/tf2-preview/mobilenet_v2/classification/4?tf-hub-format=compressed | tar xz

RUN python3 /opt/resave_1x224x224x3_f32.py \
  -i /opt/models/tf/mobilenet_v2 \
  -o /opt/models/iree/mobilenet_v2

RUN python3 /opt/print_signature.py -i /opt/models/iree/mobilenet_v2

RUN cd /opt/models/iree/mobilenet_v2 && iree-import-tf \
  --tf-import-type=savedmodel_v1 \
  --tf-savedmodel-exported-names=predict \
  ./ -o mobilenet_v2.mlir

RUN cd /opt/models/iree/mobilenet_v2 && iree-compile \
    --iree-hal-target-backends=vulkan-spirv \
    --iree-vulkan-target-triple=$VULKAN_ARCH \
    mobilenet_v2.mlir -o mobilenet_v2_vulkan_$VULKAN_ARCH.vmfb

#
# RESNET50
#

RUN mkdir /opt/models/tf/resnet50 && cd /opt/models/tf/resnet50 && \
  wget -O - https://tfhub.dev/tensorflow/resnet_50/classification/1?tf-hub-format=compressed | tar xz

RUN python3 /opt/resave_1x224x224x3_f32.py \
  -i /opt/models/tf/resnet50 \
  -o /opt/models/iree/resnet50

RUN python3 /opt/print_signature.py -i /opt/models/iree/resnet50

RUN cd /opt/models/iree/resnet50 && iree-import-tf \
  --tf-import-type=savedmodel_v1 \
  --tf-savedmodel-exported-names=predict \
  ./ -o resnet50.mlir

RUN cd /opt/models/iree/resnet50 && iree-compile \
  --iree-hal-target-backends=vulkan-spirv \
  --iree-vulkan-target-triple=arc-any-unknown \
  resnet50.mlir -o resnet50_vulkan_$VULKAN_ARCH.vmfb

#
# Vulkan runtime environment to be able to run under this docker
#
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

#
# Just useful stuff for development
#
RUN apt-get update && \
  DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
    binutils \
    less \
    openssh-client \
    vim \
  && rm -rf /var/lib/apt/lists/*

