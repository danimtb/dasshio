#! /usr/bin/env python
import os


def run(cmd, message=None):
    print("\n%s\n" % (cmd if not message else message)
    ret = os.system(cmd)
    if ret != 0:
        raise Exception("Error running: %s" % cmd)


DOCKER_LOGIN = "docker login -u {docker_user} -p {docker_pass}"
DOCKER_BUILD = "vocker run --rm --privileged -v ~/.docker:/root/.docker -v $(pwd)/{addon}:/data homeassistant/{arch}-builder -t /data --no-cache"

addon = os.getenv("ADDON")
docker_user = os.getenv("DOCKER_USER")
docker_pass = os.getenv("DOCKER_PASS")


run(DOCKER_LOGIN.format(docker_user=docker_user, docker_pass=docker_pass), "docker login")

for arch in ["armhf", "amd64", "aarch64", "i386"]:
    run(DOCKER_BUILD.format(addon=addon, arch=arch))
