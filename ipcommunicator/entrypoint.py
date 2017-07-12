import logging
from typing import Dict
from uuid import uuid4

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.base import BaseScheduler
from apscheduler.schedulers.blocking import BlockingScheduler

from ipcommunicator.communicator import Communicator
import ipgetter

_logger = logging.getLogger(__name__)

SECOND = 1 * 1000
MINUTE = 60 * SECOND
HOUR = 60 * MINUTE

SchedulerReference = str

_schedulers: Dict[SchedulerReference: BaseScheduler] = {}


def start(communicator: Communicator, period: int=1 * HOUR, blocking: bool=True) -> SchedulerReference:
    """
    Starts periodically communicating the IP address.
    :param communicator: the communicator of the address
    :param period: the number of milliseconds between each communication
    :param blocking: whether a call to this method should block
    :return: reference to the scheduler (will not get to the return if blocking!)
    """
    scheduler = BlockingScheduler() if blocking else BackgroundScheduler()
    scheduler_reference = uuid4()
    _schedulers[scheduler_reference] = scheduler
    scheduler.add_job(run, args=[communicator], trigger="interval", seconds=period)
    scheduler.start()
    return scheduler_reference


def stop(scheduler_reference: SchedulerReference):
    """
    Stops the scheduler with the given reference.
    :param scheduler_reference: the scheduler's reference
    """
    scheduler = _schedulers.pop(scheduler_reference)
    scheduler.stop()


def run(communicator: Communicator):
    """
    Communicate the IP address.
    :param communicator: the IP address communicator.
    """
    ip = ipgetter.myip()
    _logger.info(f"IPv4 address found to be: {ip}")
    communicator.send_ipv4(ip)
    # TODO: IPv6