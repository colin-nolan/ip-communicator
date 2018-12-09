import logging
from ipaddress import IPv4Address, ip_address, IPv6Address
from typing import Callable

from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.base import BaseScheduler
from apscheduler.schedulers.blocking import BlockingScheduler
from logzero import logger

from ipcommunicator.communicator import Communicator
import ipgetter

SECOND = 1
MINUTE = 60 * SECOND
HOUR = 60 * MINUTE


def ipv4_getter() -> IPv4Address:
    """
    Gets the host's IPv4 address.
    :return: the host's IPv4 address.
    """
    return ip_address(ipgetter.myip())


def ipv6_getter() -> IPv6Address:
    """
    Gets the host's IPv6 address.
    :return: the host's IPv6 address.
    """
    raise NotImplementedError()


class Controller:
    """
    IP address communication controller.
    """
    DEFAULT_PERIOD_IN_SECONDS = 0.25 * HOUR

    @property
    def started(self):
        return self._scheduler is not None

    def __init__(self, communicator: Communicator, period_in_seconds: float=DEFAULT_PERIOD_IN_SECONDS,
                 changes_only: bool=True, *, ipv4_getter: Callable[[], IPv4Address]=ipv4_getter,
                 ipv6_getter: Callable[[], IPv6Address]=ipv6_getter):
        """
        Constructor.
        :param communicator: the communicator of the address
        :param period_in_seconds: the number of seconds between each communication
        :param changes_only: whether to only communicate the IP address if it has changed
        """
        self.communicator = communicator
        self.period = period_in_seconds
        self.changes_only = changes_only
        self.previous_ipv4_address = None
        self.previous_ipv6_address = None
        self.ipv4_getter = ipv4_getter
        self.ipv6_getter = ipv6_getter
        self._scheduler: BaseScheduler = None

    def start(self, blocking: bool=True):
        """
        Starts periodically communicating the IP address.

        Not thread safe.
        :param blocking: whether a call to this method should block
        """
        if not self.started:
            scheduler = BlockingScheduler() if blocking else BackgroundScheduler()
            self._scheduler = scheduler
            scheduler.add_job(self.run, trigger="interval", seconds=self.period, next_run_time=datetime.now())
            scheduler.start()

    def stop(self):
        """
        Stops the scheduler (if running).

        Not thread safe.
        """
        if self.started:
            self._scheduler.shutdown()
            self._scheduler = None

    def run(self):
        """
        Communicate the IP address.
        """
        # TODO: IPv6
        ipv4 = self.ipv4_getter()
        logger.info(f"IPv4 address: {ipv4}")
        try:
            if not self.changes_only or ipv4 != self.previous_ipv4_address:
                logger.info(f"IPv4 address has changed")
                self.communicator.send_ipv4(ipv4)
        finally:
            self.previous_ipv4_address = ipv4
