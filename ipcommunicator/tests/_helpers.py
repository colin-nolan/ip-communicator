from ipaddress import IPv4Address

import requests

TEST_IPV4_ADDRESS_1 = IPv4Address("192.168.168.192")
TEST_IPV4_ADDRESS_2 = IPv4Address("192.168.192.168")

DEFAULT_CONNECTION_TEST_URL = "https://www.google.com"
DEFAULT_CONNECTION_TEST_TIMEOUT = 10


def is_internet_connection(test_url: str=DEFAULT_CONNECTION_TEST_URL, timeout: str=DEFAULT_CONNECTION_TEST_TIMEOUT) \
        -> bool:
    """
    TODO
    :param test_url:
    :param timeout:
    :return:
    """
    try:
        requests.get(test_url, timeout=timeout)
        return True
    except requests.ConnectionError:
        return False
