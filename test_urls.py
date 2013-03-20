from django.conf.urls.defaults import url, patterns

from django_nose_qunit.urls import urlpatterns


urlpatterns += patterns('',
        url(r'^raw-script/$', 'django_nose_qunit.views.fake_raw_script'),
    )

