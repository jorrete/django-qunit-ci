from django_nose_qunit import QUnitTestCase


class QUnitIntroTestCase(QUnitTestCase):
    test_file = 'django_nose_qunit/test/qunit_intro.js'
    html_fixtures = ('django_nose_qunit/fixtures/qunit_intro.html',)
