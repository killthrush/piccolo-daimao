import os, sys
import unittest
from datetime import datetime
from mock import patch, call, Mock


class IncrementorTests(unittest.TestCase):
    def setUp(self):
        log_patcher = patch('utilities.nest_event_publisher._logger')
        self._mock_logger = log_patcher.start()

    def test_can_increment_a_single_key_by_one(self):
        self.fail("Brillant!")

    def test_can_increment_a_single_key_by_more_than_one_with_successive_calls(self):
        self.fail("Brillant!")

    def test_ensure_that_missing_key_yields_400(self):
        self.fail("Brillant!")

    def test_ensure_that_missing_value_yields_400(self):
        self.fail("Brillant!")

    def test_ensure_that_non_integer_value_yields_400(self):
        self.fail("Brillant!")

    def test_ensure_that_flushes_happen_after_configured(self):
        self.fail("Brillant!")


if __name__ == '__main__':
    from pybald.core.logs import default_debug_log

    default_debug_log()
    loader = unittest.TestLoader()
    user_tests = loader.loadTestsFromTestCase(IncrementorTests)
    suite = unittest.TestSuite(user_tests)
    unittest.TextTestRunner(descriptions=True, verbosity=2).run(suite)