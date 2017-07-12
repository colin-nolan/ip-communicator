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
    TODO
    :param communicator:
    :param period:
    :param blocking:
    :return:
    """
    scheduler = BlockingScheduler() if blocking else BackgroundScheduler()
    scheduler_reference = uuid4()
    _schedulers[scheduler_reference] = scheduler
    scheduler.add_job(run, args=[communicator], trigger="interval", seconds=period)
    scheduler.start()
    return scheduler_reference


def stop(scheduler_reference: SchedulerReference):
    """
    TODO
    :param scheduler_reference:
    :return:
    """
    scheduler = _schedulers.pop(scheduler_reference)
    scheduler.stop()


def run(communicator: Communicator):
    """
    TODO
    :param communicator:
    :return:
    """
    ip = ipgetter.myip()
    _logger.info(f"IP address found to be: {ip}")
    communicator.send_ipv4(ip)
