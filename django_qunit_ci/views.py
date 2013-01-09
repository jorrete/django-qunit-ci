import urllib

from django.http import Http404
from django.shortcuts import render

from django_qunit_ci.testcases import registry


def run_qunit_tests(request):
    """
    Serve a page for running the specified QUnit test file, with JavaScript
    dependencies and HTML fixtures as given in the named test class.  Returns
    a 404 whenever an unknown test class or file is requested; should only
    happen if somebody is trying to guess URLs.
    """
    test_class_name = urllib.unquote(request.GET.get('class', ''))
    test_file = urllib.unquote(request.GET.get('file', ''))
    if not test_class_name in registry:
        raise Http404('No such QUnit test case: ' + test_class_name)
    cls = registry[test_class_name]
    if not test_file in cls.test_files:
        raise Http404('Unknown QUnit test script: ' + test_file)
    context = {
        'test_file': test_file,
        'title': '%s: %s' % (test_class_name, test_file),
        'dependencies': cls.dependencies,
        'fixtures': cls.html_fixtures
    }
    return render(request, 'qunit/template.html', context)
