from collections import defaultdict
from threading import Event
from typing import Dict, Any, List
from ipcommunicator.communicator import Communicator


class DummyCommunicator(Communicator):
    """
    Dummy communicator.
    """
    @property
    def sent_ipv4_messages(self) -> List[str]:
        return list(self._sent_messages[self._send_ipv4_message])

    @property
    def sent_ipv6_messages(self) -> List[str]:
        return list(self._sent_messages[self._send_ipv6_message])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._sent_messages: Dict[Any, List[str]] = defaultdict(list)
        self.message_event = Event()

    def clear(self):
        """
        Clears record of sent messages.
        """
        self._sent_messages.clear()

    def _send_ipv4_message(self, message: str):
        self._send_message(self._send_ipv4_message, message)

    def _send_ipv6_message(self, message: str):
        self._send_message(self._send_ipv6_message, message)

    def _send_message(self, queue: Any, message: str):
        self._sent_messages[queue].append(message)
        self.message_event.set()
