from ipaddress import ip_address
import unittest

from ipcommunicator.control import Controller, ipv4_getter, ipv6_getter
from ipcommunicator.tests._dummy_communicator import DummyCommunicator
from ipcommunicator.tests._helpers import is_internet_connection, TEST_IPV4_ADDRESS_1, TEST_IPV4_ADDRESS_2


class TestIpv4Getter(unittest.TestCase):
    """
    Tests for `ipv4_getter`.
    """
    def setUp(self):
        if not is_internet_connection():
            self.skipTest("No Internet connection")

    def test_getter(self):
        ipv4_getter()


@unittest.skip("IPv6 support not implemented")
class TestIpv6Getter(unittest.TestCase):
    """
    Tests for `ipv6_getter`.
    """
    def setUp(self):
        if not is_internet_connection():
            self.skipTest("No Internet connection")

    def test_getter(self):
        ipv6_getter()


class TestController(unittest.TestCase):
    """
    Tests for `Controller`.
    """
    def setUp(self):
        self.communicator = DummyCommunicator()
        self.controller = Controller(self.communicator, ipv4_getter=lambda: TEST_IPV4_ADDRESS_1)

    def test_run(self):
        self.controller.run()
        self.assertEqual(1, len(self.communicator.sent_ipv4_messages))
        self.assertEqual(TEST_IPV4_ADDRESS_1, ip_address(self.communicator.sent_ipv4_messages[0]))

    def test_run_when_no_change(self):
        self.controller.run()
        self.communicator.clear()
        self.controller.run()
        self.assertEqual(0, len(self.communicator.sent_ipv4_messages))

    def test_run_when_change_in_future(self):
        self.controller.run()
        self.communicator.clear()
        for i in range(10):
            self.controller.run()
        self.controller.ipv4_getter = lambda: TEST_IPV4_ADDRESS_2

        self.controller.run()
        self.assertEqual(1, len(self.communicator.sent_ipv4_messages))
        self.assertEqual(TEST_IPV4_ADDRESS_2, ip_address(self.communicator.sent_ipv4_messages[0]))


if __name__ == "__main__":
    unittest.main()
