# IREE Runtime Docker

Build with:
```
docker build -f images/iree/runtime/Dockerfile -t iree-runtime .
```

This docker builds IREE runtime and installs Vulkan backend environment.

To execute models start docker as follows:
```
DEVICE=${DEVICE:-/dev/dri/renderD128}
DEVICE_GRP=$(stat --format %g $DEVICE)
docker run --rm -it \
  --device $DEVICE --group-add $DEVICE_GRP \
  iree-tf
```

You need to copy models into the running docker container. For example, you can
build and copy models from [iree-tf](../tf/).

