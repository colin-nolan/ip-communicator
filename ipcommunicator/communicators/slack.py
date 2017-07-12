from slackclient import SlackClient

from ipcommunicator.communicator import Communicator

_SLACK_CLIENT_POST_MESSAGE = "chat.postMessage"


class SlackCommunicator(Communicator):
    """
    Communicator for Slack, using legacy tokens (i.e. not for use in production).
    """
    def __init__(self, token: str, channel: str=None, username: str=None, **kwargs):
        """
        Constructor.
        :param token: authentication token from BasicSlackClient
        :param channel: the channel to post to
        :param username: the username to post as
        """
        super().__init__(**kwargs)
        self.default_channel = channel
        self.default_username = username
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
        self._slack_client.api_call(
            _SLACK_CLIENT_POST_MESSAGE, channel=self.default_channel, text=message, username=self.default_username)
