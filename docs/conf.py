#!/usr/bin/env python
# encoding: utf-8
"""
Sphinx configuration for documentation
"""

from sbo_sphinx.conf import *

project = 'django-nose-qunit'
apidoc_exclude = [
    os.path.join('docs', 'conf.py'),
    os.path.join('django_nose_qunit', 'tests'),
    'setup.py',
    'test_settings.py',
    'test_urls.py',
    've',
]
extensions.append('sbo_sphinx.jsdoc')
jsdoc_source_root = os.path.join('..', 'django_nose_qunit', 'static')
jsdoc_exclude = ['qunit.js']
