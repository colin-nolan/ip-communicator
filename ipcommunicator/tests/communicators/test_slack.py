from typing import Dict, Optional

from uuid import uuid4
import os
import unittest

from slackclient import SlackClient

from ipcommunicator.communicator import CommunicationError
from ipcommunicator.communicators.slack import SlackCommunicator, SLACK_TOKEN_ENVIRONMENT_PARAMETER_NAME, \
    SLACK_CHANNEL_ENVIRONMENT_PARAMETER_NAME, SLACK_USERNAME_ENVIRONMENT_PARAMETER_NAME
from ipcommunicator.tests._helpers import is_internet_connection, TEST_IPV4_ADDRESS_1


class SlackBasedTest(unittest.TestCase):
    """
    TODO
    """
    @property
    def slack_channel_id(self):
        if self._slack_channel_id is None:
            matching_channels = list(filter(lambda channel: channel["name"] == self.slack_channel_name,
                                            self.slack_client.api_call("channels.list")["channels"]))
            assert len(matching_channels) <= 1
            if len(matching_channels) == 0:
                raise ValueError(f"Slack channel \"{self.slack_channel_name}\" not found")
            self._slack_channel_id = matching_channels[0]["id"]
        return self._slack_channel_id

    def setUp(self):
        if not is_internet_connection("https://slack.com"):
            self.skipTest("Cannot connect to Slack")

        self.slack_token = os.environ.get(SLACK_TOKEN_ENVIRONMENT_PARAMETER_NAME)
        self.slack_channel_name = os.environ.get(SLACK_CHANNEL_ENVIRONMENT_PARAMETER_NAME)
        self.slack_username = os.environ.get(SLACK_USERNAME_ENVIRONMENT_PARAMETER_NAME)
        self._slack_channel_id = None

        if self.slack_token is None:
            self.skipTest(f"{SLACK_TOKEN_ENVIRONMENT_PARAMETER_NAME} is not set")
        if self.slack_channel_name is None:
            self.skipTest(f"{SLACK_CHANNEL_ENVIRONMENT_PARAMETER_NAME} is not set")
        self.slack_client = SlackClient(self.slack_token)

    def delete_message(self, message_timestamp: str):
        """
        Deletes Slack message in the working channel with the given (assumed unique!) timestamp.
        :param message_timestamp: timestamp of message to delete
        """
        self.slack_client.api_call("chat.delete", channel=self.slack_channel_id, ts=message_timestamp)

    def find_message_with_uuid(self, uuid: str) -> Optional[Dict[str, str]]:
        """
        Finds the message in the working channel containing the given UUID.
        :param uuid: unique substring of message text
        :return: the message if matched, else `None`
        """
        return self.find_message_with_property("text", uuid)

    def find_message_from_user(self, username: str) -> Optional[Dict[str, str]]:
        """
        TODO
        :param username:
        :return:
        """
        return self.find_message_with_property("username", username)

    def find_message_with_property(self, property: str, value: str) -> Optional[Dict[str, str]]:
        """
        TODO
        :param property:
        :param value:
        :return:
        """
        history = self.slack_client.api_call("channels.history", channel=self.slack_channel_id)
        for message in history["messages"]:
            if value in message.get(property, ""):
                return message
        return None


class TestSlackCommunicator(SlackBasedTest):
    """
    Tests for `SlackCommunicator`.
    """
    def test_send_with_invalid_slack_token(self):
        communicator = SlackCommunicator("invalid-token", self.slack_channel_name, self.slack_username)
        self.assertRaises(CommunicationError, self._test_send_ipv4, communicator)

    def test_send_ipv4(self):
        communicator = SlackCommunicator(self.slack_token, self.slack_channel_name, self.slack_username)
        self._test_send_ipv4(communicator)

    def test_send_ipv4_using_environment_variables(self):
        communicator = SlackCommunicator()
        self._test_send_ipv4(communicator)

    @unittest.skip("IPv6 support not implemented")
    def test_send_ipv6(self):
        raise NotImplementedError()

    def _test_send_ipv4(self, communicator: SlackCommunicator):
        unique_message = f"{self.__class__.__name__} - {uuid4()}"
        communicator.ipv4_message_generator = lambda _: unique_message
        try:
            communicator.send_ipv4(TEST_IPV4_ADDRESS_1)
            self.assertIsNotNone(self.find_message_with_uuid(unique_message))
        finally:
            message = self.find_message_with_uuid(unique_message)
            if message is not None:
                self.delete_message(message["ts"])

