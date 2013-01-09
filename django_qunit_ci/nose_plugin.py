import logging
import os
import requests
import sys
import time
from subprocess import Popen

from nose.case import MethodTestCase
from nose.failure import Failure
from nose.plugins import Plugin
from nose.util import test_address

from django_qunit_ci import QUnitTestCase
from django_qunit_ci.conf import settings

PHANTOMJS_URL = 'http://127.0.0.1:%s/' % settings.QUNIT_PHANTOMJS_PORT
log = logging.getLogger('nose.plugins.django_nose_qunit')


class QUnitMethodTestCase(MethodTestCase):
    """
    Subclass of nose's test case class for test methods which produces better
    descriptions for QUnit tests.  Other types of tests continue to use the
    original class.
    """

    def __init__(self, method, test=None, arg=tuple(), descriptor=None):
        super(QUnitMethodTestCase, self).__init__(method, test, arg,
                                                  descriptor)
        module_name = arg[1]
        test_name = arg[2]
        if module_name:
            self.description = '%s:%s' % (module_name, test_name)
        else:
            self.description = test_name

    def shortDescription(self):
        return self.description


class QUnitPlugin(Plugin):
    """
    Nose plugin which allows for test generator methods in subclasses of
    django_qunit_ci.QUnitTestCase.  (Nose normally allows this for most classes
    except subclasses of unittest.TestCase, but we need to subclass Django's
    LiveServerTestCase which inherits from that.)
    """

    name = 'django-qunit'

    def options(self, parser, env=os.environ):
        super(QUnitPlugin, self).options(parser, env=env)

    def configure(self, options, conf):
        super(QUnitPlugin, self).configure(options, conf)

    def loadTestsFromTestCase(self, testCaseClass):
        if not issubclass(testCaseClass, QUnitTestCase):
            return None
        if len(testCaseClass.test_files) < 1:
            return None
        log.debug('Loading tests from %s' % testCaseClass.__name__)
        inst = testCaseClass()
        generator = getattr(inst, 'generator')

        def generate(g=generator, c=testCaseClass):
            try:
                for test in g():
                    test_func, arg = (test[0], test[1:])
                    yield QUnitMethodTestCase(test_func, arg=arg, descriptor=g)
            except KeyboardInterrupt:
                raise
            except:
                exc = sys.exc_info()
                yield Failure(exc[0], exc[1], exc[2],
                              address=test_address(generator))
        return self.loader.suiteClass(generate, context=generator,
                                      can_split=False)

    def prepareTestLoader(self, loader):
        self.loader = loader
        return None

    def begin(self):
        """ Start PhantomJS and clear the log file (if there is one) """
        if settings.QUNIT_PHANTOMJS_LOG:
            self.log_file = open(settings.QUNIT_PHANTOMJS_LOG, 'w')
        else:
            self.log_file = open(os.devnull, 'w')
        self.phantomjs = Popen([
            settings.QUNIT_PHANTOMJS_PATH,
            os.path.join(os.path.dirname(__file__), 'run-qunit.js'),
            str(settings.QUNIT_PHANTOMJS_PORT),
            settings.QUNIT_SCREENSHOT_DIR
        ], stdout=self.log_file)
        # Now wait for it to finish initializing
        start = time.time()
        while True:
            try:
                r = requests.get(PHANTOMJS_URL)
                if r.status_code == 200:
                    break
            except:
                if time.time() > start + 10:
                    raise requests.exceptions.Timeout()

    def finalize(self, result):
        """ Stop PhantomJS """
        self.phantomjs.terminate()
        self.log_file.close()
        return None
