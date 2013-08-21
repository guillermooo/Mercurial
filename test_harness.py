from AAAPT.runner import register_tests


TESTS_CLIENT = 'Mercurial.tests.shglib.test_client'
TESTS_PARSING = 'Mercurial.tests.shglib.test_parsing'
TESTS_LOG_SUPPORT = 'Mercurial.tests.shglib.test_log_support'

TESTS_ALL_CLIENT = [TESTS_CLIENT]
TESTS_ALL_PARSING = [TESTS_PARSING]
TESTS_ALL_SUPPORT = [TESTS_LOG_SUPPORT]

test_suites = {
        'client': TESTS_ALL_CLIENT,
        'parsing': TESTS_ALL_PARSING,
        'support': TESTS_ALL_SUPPORT,
}

register_tests(test_suites)
