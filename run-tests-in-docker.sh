#!/usr/bin/env bash

set -euf -o pipefail

scriptDirectory="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "${scriptDirectory}"

docker build -t ipcommunicator -f Dockerfile .
docker build -t ipcommunicator-tests -f Dockerfile.test .
docker run  --rm -it -v "${scriptDirectory}":/ip-communicator \
    -e SLACK_TOKEN -e SLACK_CHANNEL -e SLACK_USERNAME \
    --entrypoint=bash \
    ipcommunicator-tests run-tests.sh

# Hack the paths in the coverage report (unfortunately they are absolute)
docker run --rm -it -v $PWD/:/data alpine sed -i -e "s|\"/ip-communicator|\"${scriptDirectory}|g" /data/.coverage
