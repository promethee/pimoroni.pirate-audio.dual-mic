#!/bin/sh
docker run -d --privileged --device /dev/spidev0.0:/dev/spidev0.0 --restart always --name $(basename "$PWD") $USER/$(basename "$PWD"):latest
