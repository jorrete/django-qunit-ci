import importlib
import urllib

from django.conf import settings
from django.http import Http404
from django.shortcuts import render

from django_nose_qunit.testcases import registry


def run_qunit_tests(request):
    """
    Serve a page for running the specified QUnit test file, with JavaScript
    dependencies and HTML fixtures as given in the named test class.  Returns
    a 404 whenever an unknown test class is requested; should only
    happen if somebody is trying to guess URLs.
    """
    test_class_name = urllib.unquote(request.GET.get('class', ''))
    if not settings.DEBUG and not test_class_name in registry:
        raise Http404('No such QUnit test case: ' + test_class_name)
    if test_class_name in registry:
        cls = registry[test_class_name]
    else:
        parts = test_class_name.rsplit('.', 1)
        module = importlib.import_module(parts[0])
        cls = getattr(module, parts[1])
    test_file = cls.test_file
    context = {
        'test_file': test_file,
        'title': '%s (%s)' % (test_class_name, test_file),
        'dependencies': cls.dependencies,
        'fixtures': cls.html_fixtures
    }
    return render(request, 'django_nose_qunit/template.html', context)
