import os

from logzero import logger
from slackclient import SlackClient
import logging

from ipcommunicator.communicator import Communicator, CommunicationError

SLACK_TOKEN_ENVIRONMENT_PARAMETER_NAME = "SLACK_TOKEN"
SLACK_CHANNEL_ENVIRONMENT_PARAMETER_NAME = "SLACK_CHANNEL"
SLACK_USERNAME_ENVIRONMENT_PARAMETER_NAME = "SLACK_USERNAME"

_SLACK_CLIENT_POST_MESSAGE = "chat.postMessage"


class SlackCommunicator(Communicator):
    """
    Communicator for Slack, using legacy tokens (i.e. not for use in production).
    """
    def __init__(self, token: str=None, channel: str=None, username: str=None, **kwargs):
        """
        Constructor.
        :param token: authentication token from BasicSlackClient
        :param channel: the channel to post to
        :param username: the username to post as
        """
        super().__init__(**kwargs)

        token = token if token is not None else os.environ.get(SLACK_TOKEN_ENVIRONMENT_PARAMETER_NAME)
        if token is None:
            raise ValueError(f"Slack token must either be given as argument or set using the environment variable "
                             f"{SLACK_TOKEN_ENVIRONMENT_PARAMETER_NAME}")

        self.channel = channel if channel is not None else os.environ.get(SLACK_CHANNEL_ENVIRONMENT_PARAMETER_NAME)
        if self.channel is None:
            raise ValueError(f"Slack channel must either be given as argument or set using the environment variable "
                             f"{SLACK_CHANNEL_ENVIRONMENT_PARAMETER_NAME}")

        self.username = username if username is not None else os.environ.get(SLACK_USERNAME_ENVIRONMENT_PARAMETER_NAME)
        if self.username is None:
            raise ValueError(f"Slack username must either be given as argument or set using the environment variable "
                             f"{SLACK_USERNAME_ENVIRONMENT_PARAMETER_NAME}")

        self._slack_client = SlackClient(token)

    def _send_ipv4_message(self, message: str):
        self._post(message)

    def _send_ipv6_message(self, message: str):
        self._post(message)

    def _post(self, message: str):
        """
        Post the given message to the given channel as the given username.
        :param message: the message to post
        """
        result = self._slack_client.api_call(
            _SLACK_CLIENT_POST_MESSAGE, channel=self.channel, text=message, username=self.username)
        if not result.get("ok"):
            raise CommunicationError(f"Error sending message to Slack: {result}")

        logger.info(f"Sent message to {self.channel} Slack channel as {self.username}")
        logger.debug(f"Message sent: {message}")
