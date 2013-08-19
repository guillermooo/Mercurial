from Mercurial.test_runner import _pt_show_suites


TESTS_CLIENT = 'Mercurial.tests.shglib.test_client'
TESTS_PARSING = 'Mercurial.tests.shglib.test_parsing'
TESTS_LOG_SUPPORT = 'Mercurial.tests.shglib.test_log_support'

TESTS_ALL_CLIENT = [TESTS_CLIENT]
TESTS_ALL_PARSING = [TESTS_PARSING]
TESTS_ALL_SUPPORT = [TESTS_LOG_SUPPORT]

test_suites = {
        'client': ['_pt_run_tests', TESTS_ALL_CLIENT],
        'parsing': ['_pt_run_tests', TESTS_ALL_PARSING],
        'support': ['_pt_run_tests', TESTS_ALL_SUPPORT],
}

_pt_show_suites.register(test_suites)
