import json
import requests
import urllib

from django.core.urlresolvers import reverse
from django.test import LiveServerTestCase

from django_qunit_ci.conf import settings

PHANTOMJS_URL = 'http://127.0.0.1:%s/' % settings.QUNIT_PHANTOMJS_PORT
PHANTOMJS_TIMEOUT = 10

registry = {}


def qualified_class_name(cls):
    module = cls.__module__
    if module:
        return '%s.%s' % (module, cls.__name__)
    else:
        return cls.__name__


class QUnitTestCase(LiveServerTestCase):
    """
    A test case which runs the QUnit tests in the specified JavaScript files.
    Executes a whole file when the first test case in it is run and caches the
    results for the other test cases in it.  Each QUnit test case
    should have a module name + test name combination that is unique within
    that test file, otherwise the results from different tests will be
    confused.  Does not yet support running a single test or only the tests in
    a particular module, although QUnit supports this.

    Entries in test_files and dependencies should be relative to STATIC_ROOT,
    entries in html_fixtures are looked up as templates.
    """
    phantomjs = None

    test_files = ()
    dependencies = ()
    html_fixtures = ()

    @classmethod
    def setUpClass(cls):
        if hasattr(cls, 'results'):
            # Don't initialize twice (generator and tests)
            return
        super(QUnitTestCase, cls).setUpClass()
        registry[qualified_class_name(cls)] = cls
        cls.results = {}

    def __init__(self, methodName='runTest'):
        """
        Allow the class to be instantiated without a specified test method so
        the generator function can be run by the nose plugin.
        """
        if methodName == 'runTest':
            super(QUnitTestCase, self).__init__('generator')
        else:
            super(QUnitTestCase, self).__init__(methodName)

    def _case_url(self, test_file):
        """
        Get the live test server URL for a specific QUnit test file.
        """
        address = self.live_server_url
        className = urllib.quote(qualified_class_name(self.__class__), safe='')
        fileName = urllib.quote(test_file, safe='')
        url = reverse('django-qunit-ci-test')
        return '%s%s?class=%s&file=%s' % (address, url, className, fileName)

    def generator(self):
        """
        Load each file in PhantomJS without actually running the tests in order
        to generate a list of all the test cases.  qunit_case() will be called
        for each test case in the list.
        """
        # Need to start the server manually since we aren't running tests yet
        self.setUpClass()
        for test_file in self.test_files:
            url = self._case_url(test_file)
            post_data = json.dumps({'action': 'list', 'url': url})
            r = requests.post(PHANTOMJS_URL, data=post_data)
            r.raise_for_status()
            modules = r.json()
            for module_name in modules:
                for test_name in modules[module_name]:
                    yield self.qunit_case, test_file, module_name, test_name

    def qunit_case(self, test_file, module_name, test_name):
        """
        Run the tests in the file if that hasn't been done yet, then get the
        result for the specific test case described.
        """
        if not test_file in self.results:
            url = self._case_url(test_file)
            params = {'action': 'test', 'url': url}
            post_data = json.dumps(params)
            r = requests.post(PHANTOMJS_URL, data=post_data)
            if r.status_code != 200:
                raise self.failureException('PhantomJS error: %s' % r.text)
            self.results[test_file] = r.json()
        module = self.results[test_file]['modules'][module_name]
        test = module['tests'][test_name]
        if not test['passed']:
            message = ', '.join(test['failedAssertions'])
            raise self.failureException(message)
