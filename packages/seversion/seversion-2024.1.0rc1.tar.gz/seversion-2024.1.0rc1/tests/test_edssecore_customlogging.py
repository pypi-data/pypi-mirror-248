from unittest import TestCase, skipIf
from seCore.CustomLogging import logger


class EDSseTestCase(TestCase):

    def setUp(self) -> None:
        self.msg = "Test Message"

    def test_logger(self):
        logger.info(self.msg)


