# intel-gpu-tools docker

Build with:
```
docker build -f images/intel-gpu-tools/Dockerfile -t igt .
```

Run as follows:
```
DEVICE=${DEVICE:-/dev/dri/renderD128}
DEVICE_GRP=$(stat --format %g $DEVICE)
docker run --rm -it \
  --device $DEVICE --group-add $DEVICE_GRP --cap-add SYS_ADMIN \
  igt
```

After that, assuming you have Intel GPU on the system, you should be able to
execute `intel_gpu_top` and see Intel GPU device utilization.

