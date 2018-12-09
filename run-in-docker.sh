#!/usr/bin/env bash
set -euf -o pipefail

scriptDirectory="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "${scriptDirectory}"

docker build -q -t ipcommunicator . > /dev/null

docker run --rm -it \
    -e SLACK_TOKEN -e SLACK_CHANNEL -e SLACK_USERNAME \
    ipcommunicator "$@"
