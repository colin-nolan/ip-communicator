from abc import ABCMeta
from typing import Callable

MessageGenerator = Callable[[str], str]


class CommunicationException(Exception):
    """
    Raised if an exception occurs when communicating.
    """


class Communicator(metaclass=ABCMeta):
    """
    Communicator of IP address.
    """
    @staticmethod
    def default_message_generator(ip_address: str) -> str:
        """
        TODO
        :param ip_address:
        :return:
        """
        return ip_address

    def __init__(self, ipv4_message_generator: MessageGenerator=None, ipv6_message_generator: MessageGenerator=None):
        """
        TODO
        :param ipv4_message_generator:
        :param ipv6_message_generator:
        """
        self.ipv4_message_generator = ipv4_message_generator if ipv4_message_generator \
            else Communicator.default_message_generator
        self.ipv6_message_generator = ipv6_message_generator if ipv4_message_generator \
            else Communicator.default_message_generator

    def send_ipv4(self, ip_address: str):
        """
        Sends the given IP address.
        :param ip_address: the IPv4 address to send
        :raises CommunicationException: if the IP address could not be sent
        """
        self._send_ipv4_message(self.ipv4_message_generator(ip_address))

    def send_ipv6(self, ip_address: str):
        """
        Sends the given IP address.
        :param ip_address: the IPv6 address to send
        :raises CommunicationException: if the IP address could not be sent
        """
        self._send_ipv6_message(self.ipv6_message_generator(ip_address))

    def _send_ipv4_message(self, message: str):
        """
        TODO
        :param message:
        :return:
        """

    def _send_ipv6_message(self, message: str):
        """
        TODO
        :param message:
        :return:
        """
