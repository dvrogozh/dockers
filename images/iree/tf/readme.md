# IREE Tensorflow Docker

Build with:
```
docker build -f images/iree/tf/Dockerfile -t iree-tf .
```

This docker builds IREE with Tensorflow support and compiles Mobilenet V2 and
Resnet50 models for Vulkan targeting Intel Arc.

To execute models start docker as follows:
```
DEVICE=${DEVICE:-/dev/dri/renderD128}
DEVICE_GRP=$(stat --format %g $DEVICE)
docker run --rm -it \
  --device $DEVICE --group-add $DEVICE_GRP \
  iree-tf
```

Run examples:

```
iree-run-module \
  --device=vulkan \
  --module=/opt/models/iree/mobilenet_v2/mobilenet_v2_vulkan_arc-any-unknown.vmfb \
  --function=predict \
  --input="1x224x224x3xf32=0"

iree-run-module \
  --device=vulkan \
  --module=/opt/models/iree/resnet50/resnet50_vulkan_arc-any-unknown.vmfb \
  --function=predict \
  --input="1x224x224x3xf32=0"
```

