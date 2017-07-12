import logging

from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.base import BaseScheduler
from apscheduler.schedulers.blocking import BlockingScheduler

from ipcommunicator.communicator import Communicator
import ipgetter

_logger = logging.getLogger(__name__)

SECOND = 1
MINUTE = 60 * SECOND
HOUR = 60 * MINUTE


class Controller:
    """
    IP address communication controller.
    """
    def __init__(self, communicator: Communicator, period: int=1 * HOUR, changes_only: bool=True):
        """
        Constructor.
        :param communicator: the communicator of the address
        :param period: the number of milliseconds between each communication
        :param changes_only: whether to only communicate the IP address if it has changed
        """
        self.communicator = communicator
        self.period = period
        self.changes_only = changes_only
        self._scheduler: BaseScheduler = None
        self.previous_ipv4_address = None
        self.previous_ipv6_address = None

    def start(self, blocking: bool=True):
        """
        Starts periodically communicating the IP address.

        Not thread safe.
        :param blocking: whether a call to this method should block
        """
        scheduler = BlockingScheduler() if blocking else BackgroundScheduler()
        self._scheduler = scheduler
        scheduler.add_job(self.run, trigger="interval", seconds=self.period, next_run_time=datetime.now())
        scheduler.start()

    def stop(self):
        """
        Stops the scheduler (if running).

        Not thread safe.
        """
        if self._scheduler:
            self._scheduler.shutdown()
            self._scheduler = None

    def run(self):
        """
        Communicate the IP address.
        """
        # TODO: IPv6
        ipv4 = ipgetter.myip()
        _logger.info(f"IPv4 address found to be: {ipv4}")
        try:
            if not self.changes_only or ipv4 != self.previous_ipv4_address:
                self.communicator.send_ipv4(ipv4)
        finally:
            self.previous_ipv4_address = ipv4
