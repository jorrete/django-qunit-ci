from django.conf.urls import url
from .views import test_index, run_qunit_tests

# This should be safe to leave in the URL configuration even in production;
# the view always returns a 404 if the test classes haven't been loaded


urlpatterns = [
    url(r'qunit/$', test_index, name='django-nose-qunit-list'),
    url(r'^qunit/test/$', run_qunit_tests,name='django-nose-qunit-test')
]
