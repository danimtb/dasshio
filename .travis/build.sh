#!/bin/bash

set -e
set -x

archs="${ARCHS}"
for addon in "$@"; do
    if [ -z ${TRAVIS_COMMIT_RANGE} ] || git diff --name-only ${TRAVIS_COMMIT_RANGE} | grep -v README.md | grep -q ${addon}; then
  if [ -z "$archs" ]; then
        archs=$(jq -r '.arch // ["armhf", "amd64", "aarch64", "i386"] | [.[] | "--" + .] | join(" ")' ${addon}/config.json)
  fi
        docker run --rm --privileged -v ~/.docker:/root/.docker -v $(pwd)/${addon}:/data homeassistant/amd64-builder ${archs} -t /data --no-cache
    else
    echo "No change in commit range ${TRAVIS_COMMIT_RANGE}"
    fi
done