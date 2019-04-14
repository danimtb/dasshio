#! /usr/bin/env python
import os


def run(cmd, message=None):
    msg = message or cmd
    print("\n%s\n" % msg)
    ret = os.system(cmd)
    if ret != 0:
        raise Exception("Error running: %s" % msg)


DOCKER_BUILD = "docker run --rm --privileged -v ~/.docker:/root/.docker -v $(pwd)/{addon}:/data homeassistant/{arch}-builder -t /data --no-cache"

addon = os.getenv("ADDON")


for arch in ["armhf", "amd64", "aarch64", "i386"]:
    run(DOCKER_BUILD.format(addon=addon, arch=arch))
