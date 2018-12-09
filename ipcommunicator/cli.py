import logging
import sys
from dataclasses import dataclass
from enum import Enum, unique
from typing import List, Dict, Callable

import logzero
from argparse import ArgumentParser
from logzero import logger

from ipcommunicator._external.verbosity_argument_parser import verbosity_parser_configuration, VERBOSE_PARAMETER_KEY, \
    DEFAULT_LOG_VERBOSITY_KEY, get_verbosity
from ipcommunicator.communicator import Communicator
from ipcommunicator.communicators.slack import SlackCommunicator
from ipcommunicator.control import Controller
from ipcommunicator.meta import EXECUTABLE_NAME, VERSION, DESCRIPTION

COMMUNICATOR_PARAMETER = "communicator"
CHECK_PERIOD_SHORT_PARAMETER = "p"
CHECK_PERIOD_LONG_PARAMETER = "check-period"
VERBOSITY_SHORT_PARAMETER = verbosity_parser_configuration[VERBOSE_PARAMETER_KEY]

DEFAULT_CHECK_PERIOD = Controller.DEFAULT_PERIOD_IN_SECONDS
DEFAULT_VERBOSITY = verbosity_parser_configuration[DEFAULT_LOG_VERBOSITY_KEY]


@unique
class CommunicatorName(Enum):
    """
    Names of supported communicators.
    """
    SLACK = "slack"


COMMUNICATOR_FACTORY_MAP: Dict[CommunicatorName, Callable[[], Communicator]] = {
    CommunicatorName.SLACK: lambda: SlackCommunicator()
}


@dataclass
class CliConfiguration:
    """
    Base CLI configuration.
    """
    log_verbosity: int
    communicator_name: CommunicatorName
    check_period: float


def _create_parser() -> ArgumentParser:
    """
    Creates an argument parser.
    :return: the created parser
    """
    parser = ArgumentParser(prog=EXECUTABLE_NAME, description=f"{DESCRIPTION} (v{VERSION})")

    parser.add_argument(f"-{CHECK_PERIOD_SHORT_PARAMETER}", f"--{CHECK_PERIOD_LONG_PARAMETER}",
                        default=DEFAULT_CHECK_PERIOD, type=float,
                        help="number of seconds between checking if the host's public IP address has changed")
    parser.add_argument(f"-{VERBOSITY_SHORT_PARAMETER}", action="count", default=0,
                        help="increase the level of log verbosity (add multiple increase further)")
    parser.add_argument(f"{COMMUNICATOR_PARAMETER}", type=str, choices=[e.value for e in CommunicatorName],
                        help="communicator to use to send notifications of updates on the host's public IP address")
    return parser


def parse_cli_configuration(arguments: List[str]) -> CliConfiguration:
    """
    Parses the given CLI arguments.
    :param arguments: the arguments from the CLI
    :return: parsed configuration
    """
    parsed_arguments = _create_parser().parse_args(arguments)
    parsed_arguments = {x.replace("_", "-"): y for x, y in vars(parsed_arguments).items()}

    cli_configuration = CliConfiguration(
        log_verbosity=get_verbosity(parsed_arguments),
        communicator_name=CommunicatorName(parsed_arguments[COMMUNICATOR_PARAMETER]),
        check_period=parsed_arguments[CHECK_PERIOD_LONG_PARAMETER]
    )

    return cli_configuration


def _set_log_level(level: int):
    """
    Sets the log level to that given.
    :param level: log level to set
    """
    logzero.loglevel(level)
    if level == logging.WARNING:
        logger.warning("There are not likely to be many WARN level logs: consider increasing the verbosity by adding"
                       f"more -{VERBOSITY_SHORT_PARAMETER}")


def main(cli_arguments: List[str], blocking: bool=True):
    """
    Entrypoint.
    :param cli_arguments: arguments passed in via the CLI
    :param blocking: whether the controller should block
    :return: the controller
    """
    cli_configuration = parse_cli_configuration(cli_arguments)

    if cli_configuration.log_verbosity:
        _set_log_level(cli_configuration.log_verbosity)

    communicator = COMMUNICATOR_FACTORY_MAP[cli_configuration.communicator_name]()
    controller = Controller(communicator, period_in_seconds=cli_configuration.check_period, changes_only=True)
    controller.start(blocking=blocking)
    return controller


def entrypoint():
    """
    Entry-point to be used by CLI.
    """
    logger.setLevel(DEFAULT_VERBOSITY)
    main(sys.argv[1:])


if __name__ == "__main__":
    entrypoint()
