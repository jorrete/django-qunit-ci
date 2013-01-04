import os
import time
from subprocess import Popen
from unittest import TestSuite

from django.test import LiveServerTestCase

import requests

from django_qunit_ci.conf import settings

PHANTOMJS_URL = 'http://127.0.0.1:%s/' % settings.QUNIT_PHANTOMJS_PORT
PHANTOMJS_TIMEOUT = 10

# Reference to the PhantomJS subprocess
phantomjs = None


def start_phantomjs():
    """ Start PhantomJS if it isn't already running """
    if phantomjs:
        return
    phantomjs = Popen([
        settings.QUNIT_PHANTOMJS_PATH,
        os.path.join(os.path.dirname(__file__), 'run-qunit.js'),
        settings.QUNIT_PHANTOMJS_PORT
    ])
    # Now wait for it to finish initializing
    start = time.time()
    while True:
        try:
            r = requests.get(PHANTOMJS_URL)
            if r.status_code == 200:
                break
        except:
            if time.time() > start + PHANTOMJS_TIMEOUT:
                raise requests.exceptions.Timeout()


def stop_phantomjs():
    """ Stop PhantomJS if it's running """
    if not phantomjs:
        return
    phantomjs.terminate()
    phantomjs = None


class QUnitTestCase(LiveServerTestCase):
    """
    A test case which processes the result of a single QUnit test in the
    specifed JavaScript file.  Executes the file and caches the results if this
    is the first test from it, otherwise pulls the result from the already
    executed run.
    """

    executed_tests = {}

    def __init__(self, test_file, test_name, dependencies=(), html_fixtures=(),
                 module=None):
        self.test_file = test_file
        self.test_name = test_name
        self.dependencies = dependencies
        self.html_fixtures = html_fixtures
        self.module = module

    @classmethod
    def setUpClass(cls):
        super(LiveServerTestCase, cls).setUpClass()
        start_phantomjs()

    @classmethod
    def tearDownClass(cls):
        super(LiveServerTestCase, cls).tearDownClass()
        stop_phantomjs()

    def runTest(self):
        if not self.test_file in self.executed_tests.keys():
            path = os.path.abspath(self.test_file)
            params = {'file': path, 'test': self.test_name}
            if self.module:
                params['module'] = self.module
            self.wait_for_phantomjs()
            r = requests.get(PHANTOMJS_URL + '/test', params=params)
            self.executed_tests[self.test_file] = r.json()

    def wait_for_phantomjs(self):
        """ Wait for PhantomJS to finish initializing, if necessary """
        start = time.time()
        while True:
            try:
                r = requests.get(PHANTOMJS_URL)
                if r.status_code == 200:
                    break
            except:
                if time.time() > start + PHANTOMJS_TIMEOUT:
                    raise requests.exceptions.Timeout()


class QUnitTestSuite(TestSuite):
    """
    A test suite representing all the individual tests in a JavaScript file of
    QUnit tests.  QUnit doesn't provide an actual introspection mechanism for
    modules and tests, so we have to rely on regular expressions; this could
    break down in the case of commented-out tests, we'll try to treat those as
    skipped tests.  If a module name is specified, only tests in that module
    will be run.  (Again, QUnit doesn't allow finer-grained control like
    running a single test.)
    """

    def __init__(self, test_file, module=None, dependencies=(), fixtures=()):
        start_phantomjs()
        r = requests.post(PHANTOMJS_URL, data={'action': 'list'})
        modules = r.json()
        for module in modules:
            for test in module['tests']:
                self.addTest(QUnitTestCase(test_file, test, dependencies,
                                           fixtures, module['name']))
