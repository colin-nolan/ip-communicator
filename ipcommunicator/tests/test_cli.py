import os
import unittest
from time import sleep
from uuid import uuid4

from capturewrap import CaptureWrapBuilder

from ipcommunicator.cli import main
from ipcommunicator.communicators.slack import SLACK_USERNAME_ENVIRONMENT_PARAMETER_NAME
from ipcommunicator.meta import PACKAGE_NAME, VERSION, DESCRIPTION
from ipcommunicator.tests.communicators.test_slack import SlackBasedTest


class TestCli(SlackBasedTest):
    """
    Tests for `Controller`.
    """
    def test_main_help(self):
        builder = CaptureWrapBuilder(capture_stdout=True,
                                     capture_exceptions=lambda e: isinstance(e, SystemExit) and e.code == 0)
        wrapped = builder.build(main)
        result = wrapped(["-h"])
        self.assertIn(PACKAGE_NAME, result.stdout)
        self.assertIn(VERSION, result.stdout)
        self.assertIn(DESCRIPTION, result.stdout)

    def test_main(self):
        builder = CaptureWrapBuilder(capture_stdout=True,
                                     capture_exceptions=lambda e: isinstance(e, SystemExit) and e.code == 0)
        wrapped = builder.build(main)
        result = wrapped(["-h"])
        self.assertIn(PACKAGE_NAME, result.stdout)
        self.assertIn(VERSION, result.stdout)
        self.assertIn(DESCRIPTION, result.stdout)

    def test_main_slack(self):
        original_username = os.environ.get(SLACK_USERNAME_ENVIRONMENT_PARAMETER_NAME)
        username = str(uuid4())
        controller = None
        message = None
        try:
            os.environ[SLACK_USERNAME_ENVIRONMENT_PARAMETER_NAME] = username
            controller = main(["slack"], blocking=False)
            retries = 0
            while retries < 10:
                message = self.find_message_from_user(username)
                if message is not None:
                    break
                sleep(0.2 * retries)
                retries += 1
            self.assertNotEqual(10, retries)
        finally:
            if original_username is not None:
                os.environ[SLACK_USERNAME_ENVIRONMENT_PARAMETER_NAME] = original_username
            if controller is not None:
                controller.stop()
            if message is not None:
                self.delete_message(message["ts"])


if __name__ == "__main__":
    unittest.main()
