#! /usr/bin/env python
import os


def run(cmd, message=None):
    msg = message or cmd
    print("\n%s\n" % msg)
    ret = os.system(cmd)
    if ret != 0:
        raise Exception("Error running: %s" % msg)

travis_tag = os.getenv("TRAVIS_TAG")
addon = os.getenv("ADDON")

docker_build = "docker run --rm --privileged " \
               "-v /var/run/docker.sock:/var/run/docker.sock " \
               "-v ~/.docker:/root/.docker " \
               "-v $(pwd):/docker " \
               "hassioaddons/build-env:latest " \
               "--target {addon} " \
               "--login ${{DOCKER_USER}} " \
               "--password ${{DOCKER_PASS}} " \
               "--no-cache --all --tag-latest"
if travis_tag:
    docker_build = docker_build + " --push"
run(docker_build.format(addon=addon))
