import logging
import os
import requests
import time
from subprocess import Popen

from nose.plugins import Plugin

from django_qunit_ci import QUnitTestCase
from django_qunit_ci.conf import settings

PHANTOMJS_URL = 'http://127.0.0.1:%s/' % settings.QUNIT_PHANTOMJS_PORT
log = logging.getLogger('nose.plugins.django_qunit')


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
        generator = testCaseClass.generator
        return self.loader.loadTestsFromGeneratorMethod(generator,
                                                        testCaseClass)

    def prepareTestLoader(self, loader):
        self.loader = loader
        return None

    def begin(self):
        """ Start PhantomJS """
        self.phantomjs = Popen([
            settings.QUNIT_PHANTOMJS_PATH,
            os.path.join(os.path.dirname(__file__), 'run-qunit.js'),
            str(settings.QUNIT_PHANTOMJS_PORT),
            settings.QUNIT_SCREENSHOT_DIR
        ])
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
        return None
