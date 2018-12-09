import unittest

from ipcommunicator.tests._dummy_communicator import DummyCommunicator
from ipcommunicator.tests._helpers import TEST_IPV4_ADDRESS_1


class TestCommunicator(unittest.TestCase):
    """
    Tests for `Communicator`.
    """
    def setUp(self):
        self.communicator = DummyCommunicator()

    def test_default_message_generator(self):
        self.assertIn(str(TEST_IPV4_ADDRESS_1), self.communicator.default_message_generator(TEST_IPV4_ADDRESS_1))


if __name__ == "__main__":
    unittest.main()
