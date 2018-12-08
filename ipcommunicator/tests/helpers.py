import requests

DEFAULT_TEST_URL = "https://www.google.com"
DEFAULT_TIMEOUT = 10


def is_internet_connection(test_url: str=DEFAULT_TEST_URL, timeout: str=DEFAULT_TIMEOUT) -> bool:
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
