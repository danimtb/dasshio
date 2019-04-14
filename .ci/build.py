#! /usr/bin/env python
import os


def run(cmd, message=None):
    msg = message or cmd
    print("\n%s\n" % msg)
    ret = os.system(cmd)
    if ret != 0:
        raise Exception("Error running: %s" % msg)


addon = os.getenv("ADDON")
docker_build = "docker run --rm --privileged -v ~/.docker:/root/.docker -v $(pwd)/{addon}:/data homeassistant/amd64-builder -t /data --no-cache"
run(docker_build.format(addon=addon))
