import json
import logging
import os
import requests
import urllib

from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.test import LiveServerTestCase
from django.test.testcases import QuietWSGIRequestHandler, StoppableWSGIServer

from django_nose_qunit.conf import settings

PHANTOMJS_URL = 'http://127.0.0.1:%s/' % settings.QUNIT_PHANTOMJS_PORT
PHANTOMJS_TIMEOUT = 10

logger = logging.getLogger('django.request')
registry = {}

# First, we need to make some improvements to Django's LiveServerTestCase and
# the associated code:
#   1. Log messages from the WSGI request handler instead of ignoring them (the
#      logger output can be tweaked or suppressed as necessary).
#   2. Log errors from the WSGI request handler instead of dumping them to
#      stderr (where they get mixed in with the test results).
#   3. Don't dump "[Errno 32] Broken pipe" and similar harmless errors from
#      the WSGI server to the console.
# I'll try to get some code accepted into Django which does this automatically
# and/or makes it easier to override.


def qwrh_log_exception(self, exc_info):
    """Implementation of log_exception() for QuietWSGIRequestHandler which logs
    errors instead of dumping them to stderr (where they get mixed up with the
    test output).
    """
    logger.error('QuietWSGIRequestHandler exception:', exc_info=exc_info)


def qwrh_log_message(self, format_string, *args):
    """ Replacement for QuietWSGIRequestHandler.log_message() to log to file
    rather than ignore the messages """
    # Don't bother logging requests for admin images or the favicon.
    if hasattr(self, 'admin_media_prefix'):
        # Django 1.4.x
        admin_prefix = self.admin_media_prefix
    else:
        # Django 1.5+
        admin_prefix = self.admin_static_prefix
    if (self.path.startswith(admin_prefix) or self.path == '/favicon.ico'):
        return
    logger.info(format_string % args)


def qwrh_get_stderr(self):
    """ Anything other than an actual exception trying to write to stderr
    is probably a captured broken pipe exception or such that can be safely
    ignored. """
    return open(os.devnull, 'w')

QuietWSGIRequestHandler.log_exception = qwrh_log_exception
QuietWSGIRequestHandler.log_message = qwrh_log_message
QuietWSGIRequestHandler.get_stderr = qwrh_get_stderr


def sws_handle_error(self, request, client_address):
    """ Errors from the WSGI server itself tend to be harmless ones like
    "[Errno 32] Broken pipe" (which happens when a browser cancels a request
    before it finishes because it realizes it already has the asset).  By
    default these get dumped to stderr where they get confused with the test
    results, but aren't actually treated as test errors.  We'll just ignore
    them for now.
    """
    pass

StoppableWSGIServer.handle_error = sws_handle_error


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

    test_file and dependencies paths should be relative to STATIC_URL,
    entries in html_fixtures are looked up as templates. html_strings are
    injected directly. raw_script_urls are referenced directly (no STATIC_URL
    processing."""

    phantomjs = None

    test_file = ''
    dependencies = ()
    raw_script_urls = ()
    html_fixtures = ()
    html_strings = ()

    @classmethod
    def setUpClass(cls):
        super(QUnitTestCase, cls).setUpClass()
        registry[qualified_class_name(cls)] = cls

    def __init__(self, methodName='runTest', request=None, autostart=False):
        """
        Allow the class to be instantiated without a specified test method so
        the generator function can be run by the nose plugin.
        """
        # These attributes get used when serving pages interactively
        self.request = request
        self.autostart = autostart
        self.response = None
        if methodName == 'runTest':
            super(QUnitTestCase, self).__init__('generator')
        else:
            super(QUnitTestCase, self).__init__(methodName)

    def _case_url(self):
        """
        Get the live test server URL for this test case's QUnit test file.
        """
        address = self.live_server_url
        className = urllib.quote(qualified_class_name(self.__class__), safe='')
        url = reverse('django-nose-qunit-test')
        return '%s%s?class=%s' % (address, url, className)

    def generator(self):
        """
        Load each file in PhantomJS without actually running the tests in order
        to generate a list of all the test cases.  qunit_case() will be called
        for each test case in the list.
        """
        # Need to start and stop server, since tests aren't running yet
        self.__class__.setUpClass()
        try:
            url = self._case_url()
            post_data = json.dumps({'action': 'list', 'url': url})
            r = requests.post(PHANTOMJS_URL, data=post_data)
            if r.status_code != 200:
                className = qualified_class_name(self.__class__)
                msg = 'PhantomJS error in %s: %s' % (className, r.text)
                raise self.failureException(msg)
            modules = r.json()
        finally:
            self.__class__.tearDownClass()
        for module_name in modules:
            for test_name in modules[module_name]:
                yield self.qunit_case, module_name, test_name

    def qunit_case(self, module_name, test_name):
        """
        Run the tests in the file if that hasn't been done yet, then get the
        result for the specific test case described.
        """
        if not hasattr(self.__class__, 'results'):
            url = self._case_url()
            params = {'action': 'test', 'url': url}
            post_data = json.dumps(params)
            r = requests.post(PHANTOMJS_URL, data=post_data)
            if r.status_code != 200:
                raise self.failureException('PhantomJS error: %s' % r.text)
            self.__class__.results = r.json()
        modules = self.results['modules']
        if not module_name in modules:
            msg = 'Unable to find results for module "%s".  All results: %s'
            msg = msg % (module_name, json.dumps(self.results))
            raise self.failureException(msg)
        tests = modules[module_name]['tests']
        if not test_name in tests:
            msg = 'Unable to find results for test "%s" in module "%s". '
            msg += 'Results for that module: %s'
            msg = msg % (test_name, module_name, json.dumps(self.results))
            raise self.failureException(msg)
        test = tests[test_name]
        if test['failed'] > 0:
            message = ', '.join(test['failedAssertions'])
            raise self.failureException(message)

    def serve_page(self):
        """
        Serve the page with all tests for use in an interactive session.  Runs
        setUp and tearDown once at appropriate times, so test cases can prepare
        templates and database fixtures for use by the page as a whole.
        """
        class_name = qualified_class_name(self.__class__)
        context = {
            'test_file': self.test_file,
            'title': '%s (%s)' % (class_name, self.test_file),
            'dependencies': self.dependencies,
            'raw_script_urls': self.raw_script_urls,
            'fixtures': self.html_fixtures,
            'html_strings': self.html_strings,
            # Can't assume django.core.context_processors.debug is in use
            'autostart': self.autostart,
        }
        self.response = render(self.request, 'django_nose_qunit/template.html',
                               context)
