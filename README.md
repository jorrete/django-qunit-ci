django-qunit-ci
===============

Integrate QUnit JavaScript tests into a Django test suite via nose.

Installation
------------

1.  Checkout the latest django-qunit-ci release and copy or symlink the
`django_qunit_ci` directory into your `PYTHONPATH`.
2.  Add `'django_qunit_ci'` to your `INSTALLED_APPS` setting.
3.  Add some entries to your URL configuration:
```python
from django_qunit_ci.urls import urlpatterns as qunit_urlpatterns

# ... the rest of your URLconf here ...

urlpatterns += qunit_urlpatterns()
```
This only adds one URL (/django_qunit_ci/), and it returns a 404 unless QUnit
tests have been initialized as part of a test run.
3.  Install PhantomJS (http://phantomjs.org/), a headless web browser used to
run the tests.  Either make sure the "phantomjs" executable is in your PATH or
set the QUNIT_PHANTOMJS_PATH Django setting to be the full path to it.
4.  If you want screenshots taken when tests fail, set QUNIT_SCREENSHOT_DIR to
the directory you want them to be saved in.
5.  By default, PhantomJS listens for instructions from the nose test runner on
port 9081.  If you wish to use a different port, set QUNIT_PHANTOMJS_PORT to
the desired port number.
6.  By default, messages from the test server are silently ignored.  If you
want to preserve them to aid in debugging, set QUNIT_LOG_FILE to the path of
the log file to be used.

Creating Unit Tests
-------------------

Tests can be written in JavaScript using QUnit as normal; see the QUnit
documentation at http://qunitjs.com/ for details.  You need only create a
JavaScript file, not the HTML page that will load it (that is provided by the
template at qunit/template.html).  If your tests depend on HTML fixtures in the
qunit-fixture div, create those as HTML fragments in files which can be loaded
as templates.  External script dependencies should be files in the staticfiles
load path.

To make nose aware of your QUnit tests, create a subclass of
django_qunit_ci.QUnitTestCase in a file which would normally be searched by
nose, for example my_app/test/qunit/test_case.py.  It can contain as little as
just the "test_files" attribute (a list or tuple of one or more paths to QUnit
test scripts).  Any script dependencies for your test script(s) should be given
as paths relative to STATIC_ROOT in the "dependencies" attribute.  Paths to
HTML fixture templates are listed in the "html_fixtures" attribute.

Running Unit Tests
------------------
Add " --with-django-qunit" to your normal test execution command (using
django-admin.py or manage.py).  Execution can be restricted to one or more
specified packages and/or classes as normal.  There is currently no support for
running only a single module or test within a QUnit test script; QUnit module
and test names can be arbitrary strings, which makes it difficult for the nose
command parser to handle them.

How It Works
------------
QUnitTestCase is a subclass of Django's LiveServerTestCase, which starts a
Django test server in the background on setup of the test class and stops it on
teardown.  django_qunit_ci includes a nose plugin which starts PhantomJS via
a script which orders it to listen to further instructions via HTTP on a
specific port.  When nose searches for tests to run, the plugin tells it how
to ask PhantomJS to load each test script (without running the tests) in order
to get information about the modules and tests it contains.  Once these tests
are enumerated, they are run like any other test case.  The first execution of
a test from a QUnit test script runs all of the tests in the script, and the
results are stored.  Each test case then reports success or failure based on
the reported results, with failures including any messages provided by QUnit.
If a screenshot path was configured, a screenshot of the page is taken and
saved after each failure.  When the test run ends, PhantomJS is terminated.
