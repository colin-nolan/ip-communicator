from abc import ABCMeta, abstractmethod
from ipaddress import IPv4Address, IPv6Address
from typing import Callable, Union


class CommunicationError(RuntimeError):
    """
    Raised if an error occurs when communicating.
    """


class Communicator(metaclass=ABCMeta):
    """
    Communicator of IP address.
    """
    @staticmethod
    def default_message_generator(ip_address: Union[IPv4Address, IPv6Address]) -> str:
        """
        Default generator for the IP messages.
        :param ip_address: the IP address
        :return: the message generated from the given IP address
        """
        return ip_address.exploded

    @abstractmethod
    def _send_ipv4_message(self, message: str):
        """
        Sends the IPv4 related message.
        :param message: the message to send
        :raises CommunicationException: if the IP address could not be sent
        """

    @abstractmethod
    def _send_ipv6_message(self, message: str):
        """
        Sends the IPv6 related message.
        :param message: the message to send
        :raises CommunicationException: if the IP address could not be sent
        """

    def __init__(self, ipv4_message_generator: Callable[[IPv4Address], str]=None,
                 ipv6_message_generator: Callable[[IPv6Address], str]=None):
        """
        Constructor.
        :param ipv4_message_generator: generator for messages to send relating the machines IPv4 address
        :param ipv6_message_generator: generator for messages to send relating the machines IPv6 address
        """
        self.ipv4_message_generator = ipv4_message_generator if ipv4_message_generator \
            else Communicator.default_message_generator
        self.ipv6_message_generator = ipv6_message_generator if ipv4_message_generator \
            else Communicator.default_message_generator

    def send_ipv4(self, ip_address: IPv4Address):
        """
        Sends the given IP address.
        :param ip_address: the IPv4 address to send
        :raises CommunicationException: if the IP address could not be sent
        """
        self._send_ipv4_message(self.ipv4_message_generator(ip_address))

    def send_ipv6(self, ip_address: IPv6Address):
        """
        Sends the given IP address.
        :param ip_address: the IPv6 address to send
        :raises CommunicationException: if the IP address could not be sent
        """
        self._send_ipv6_message(self.ipv6_message_generator(ip_address))
