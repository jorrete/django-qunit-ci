from django.conf import settings
from django.conf.urls import url, patterns
from django.conf.urls.static import static

from django_nose_qunit.urls import urlpatterns


urlpatterns += patterns(
    '',
    url(r'^raw-script/$', 'django_nose_qunit.views.fake_raw_script'),
) + static(settings.STATIC_URL, settings.STATIC_ROOT)
