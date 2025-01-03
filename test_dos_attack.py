import unittest
from utils import InputValidator, Logger

class TestInputValidator(unittest.TestCase):
    """Unit tests for the InputValidator class."""
    def test_validate_ip(self):
        self.assertTrue(InputValidator.validate_ip("192.168.1.1"))
        self.assertFalse(InputValidator.validate_ip("999.999.999.999"))

    def test_validate_port(self):
        self.assertTrue(InputValidator.validate_port(80))
        self.assertFalse(InputValidator.validate_port(70000))

class TestLogger(unittest.TestCase):
    def setUp(self):
        self.logger = Logger("test_log.log")

    def test_log_attack_start(self):
        self.logger.log_attack_start(("192.168.1.1", 80), "syn")
        # Check if the log file contains the expected log entry
        with open("test_log.log", "r") as f:
            logs = f.readlines()
            self.assertIn("Attack started - Target: 192.168.1.1:80 - Method: syn", logs[-1])

    def test_log_error(self):
        self.logger.log_error("Test error")
        # Check if the log file contains the expected error log entry
        with open("test_log.log", "r") as f:
            logs = f.readlines()
            self.assertIn("Error occurred: Test error", logs[-1])

if __name__ == "__main__":
    unittest.main()
