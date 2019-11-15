#! /usr/bin/env python
import os


def run(cmd, message=None):
    msg = message or cmd
    print("\n%s\n" % msg)
    ret = os.system(cmd)
    if ret != 0:
        raise Exception("Error running: %s" % msg)

travis_tag = os.getenv("TRAVIS_TAG")
travis_commmit = os.getenv("TRAVIS_COMMIT")
github_url = os.getenv("GITHUB_URL")
addon = os.getenv("ADDON")

docker_build = "docker run -it --rm --privileged --name {addon} " \
               "-v ~/.docker:/root/.docker " \
               "-v $(pwd)/{addon}:/data " \
               "homeassistant/build-env:latest " \
               "--target {addon} " \
               "--tag-latest " \
               "--all -t /data --no-cache " \
               "--author 'Daniel Manzaneque <danimanzaneque@gmail.com>' " \
               " --doc-url {github_url} " \
               "--parallel " \
               "--arg COMMIT {travis_commmit}"
if not travis_tag:
    docker_build = docker_build + " --test"
run(docker_build.format(addon=addon, travis_commmit=travis_commmit, github_url=github_url))
