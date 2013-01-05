from django.conf import settings as django_settings


class LazySettings(object):

    @property
    def QUNIT_PHANTOMJS_PATH(self):
        return getattr(django_settings, "QUNIT_PHANTOMJS_PATH", "phantomjs")

    @property
    def QUNIT_PHANTOMJS_PORT(self):
        return getattr(django_settings, "QUNIT_PHANTOMJS_PORT", 9081)

    @property
    def QUNIT_SCREENSHOT_DIR(self):
        return getattr(django_settings, "QUNIT_SCREENSHOT_DIR", '')

settings = LazySettings()
