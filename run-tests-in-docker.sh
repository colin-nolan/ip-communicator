#!/usr/bin/env bash

set -euf -o pipefail

scriptDirectory="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

## Note: `mktemp` creates temps in directory that cannot be mounted by default on Mac
#tempDirectory="/tmp/patchwork-docker-${RANDOM}"
#trap "echo ${tempDirectory} && rm -rf ${tempDirectory}" INT TERM HUP EXIT
#mkdir "${tempDirectory}"

docker build -t ipcommunicator -f Dockerfile .
docker build -t ipcommunicator-tests -f Dockerfile.test .
docker run --rm -it -v "${scriptDirectory}":/ipcommunicator \
    --entrypoint=bash \
    ipcommunicator-tests run-tests.sh
