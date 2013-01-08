from django_qunit_ci import QUnitTestCase


class QUnitIntroTestCase(QUnitTestCase):
    test_files = ('django_qunit_ci/test/qunit_intro.js',)
    html_fixtures = ('qunit/fixtures/qunit_intro.html',)
