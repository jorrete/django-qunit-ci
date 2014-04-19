import os

# Django settings for django_nose_qunit tests

DEBUG = False
TEMPLATE_DEBUG = DEBUG
ALLOWED_HOSTS = ['localhost']

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
NOSE_PLUGINS = [
    'django_nose_qunit.QUnitPlugin'
]
QUNIT_DYNAMIC_REGISTRY = True

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'UTC'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

ROOT_PATH = os.path.abspath(os.path.dirname(__file__))

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.join(ROOT_PATH, 'dist', 'static')

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'f9f22f75-56c9-11e2-9217-20c9d0480163'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'test_urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_nose',
    'django_nose_qunit',
    'sbo_selenium',
    # Uncomment the next line to enable the admin:
    # 'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
)

LOG_DIR = os.path.join(ROOT_PATH, 'log')
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)
SELENIUM_SCREENSHOT_DIR = os.path.join(LOG_DIR, 'screenshots')

# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'simple': {
            'format': '[%(levelname)s] [%(asctime)s] [%(name)s]: %(message)s'
        },
    },
    'handlers': {
        # nose installs handlers that only show output for failed tests, but they
        # can omit errors in setup and teardown; log everything to file also
        'file': {
            'class': 'logging.FileHandler',
            'filename': os.path.join(LOG_DIR, 'tests.log'),
            'formatter': 'simple',
            'level': 'DEBUG',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'propagate': True,
            'level': 'DEBUG',
        },
        'django.request': {
            'handlers': ['file'],
            'propagate': True,
            'level': 'INFO',
        },
        'django_nose_qunit': {
            'handlers': ['file'],
            'propagate': True,
            'level': 'DEBUG',
        },
        # Silence "Starting new HTTP connection" messages
        'requests': {
            'handlers': ['file'],
            'propagate': True,
            'level': 'WARNING',
        },
        'sbo_selenium': {
            'handlers': ['file'],
            'propagate': True,
            'level': 'DEBUG',
        },
        'selenium': {
            'handlers': ['file'],
            'propagate': True,
            'level': 'DEBUG',
        },
    }
}


NOSE_ARGS = [
    '--nocapture',
    '--failure-detail',
    '--verbosity=3',
]
