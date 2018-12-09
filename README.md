[![Build Status](https://travis-ci.org/colin-nolan/ip-communicator.svg?branch=master)](https://travis-ci.org/colin-nolan/ip-communicator)
[![codecov](https://codecov.io/gh/colin-nolan/ip-communicator/branch/master/graph/badge.svg)](https://codecov.io/gh/colin-nolan/ip-communicator)

# IP Communicator
_Monitors and communicates changes of a machine's public IP address_


## Purpose
To monitor a machine's public IP address and to communicate changes to it using a communicator plugin. 

Similar to a DDNS client but not coupled to DDNS.



## How to
TODO


### Communicator Plugins
#### Slack
Communicates IP address changes to a slack channel. Gets configuration from the environment variables:
`SLACK_TOKEN` `SLACK_CHANNEL` `SLACK_USERNAME`.



## Installation
Prerequisites
- Python 3.6+ (can be run entirely from Docker if you don't have Python 3.6).

The tool can be installed directly from GitHub:
```bash
pip install git+https://github.com/wtsi-hgi/ip-communicator@master#egg=ipcommunicator
```
