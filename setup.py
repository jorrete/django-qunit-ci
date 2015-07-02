#!/usr/bin/env python

import codecs
import os
from pip.download import PipSession
from pip.index import PackageFinder
from pip.req import parse_requirements
from setuptools import setup, find_packages

install_requires = [
    'django-nose',
    'sbo-selenium>=0.4.0',
]

version = '1.6.0'  # Update docs/CHANGELOG.rst if you increment the version

on_rtd = os.environ.get('READTHEDOCS', None) == 'True'
if on_rtd:
    root_dir = os.path.abspath(os.path.dirname(__file__))
    session = PipSession()
    requirements_path = os.path.join(root_dir, 'requirements', 'documentation.txt')
    finder = PackageFinder([], [], session=session)
    requirements = parse_requirements(requirements_path, finder, session=session)
    install_requires.extend([str(r.req) for r in requirements])

with codecs.open('README.rst', 'r', 'utf-8') as f:
    long_description = f.read()

setup(
    name="django-nose-qunit",
    version=version,
    author="Jeremy Bowman",
    author_email="jbowman@safaribooksonline.com",
    description="Integrate QUnit JavaScript tests into a Django test suite via nose",
    long_description=long_description,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Software Development :: Testing',
    ],  # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    url='https://github.com/safarijv/django-qunit-ci',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    include_package_data=True,
    zip_safe=False,
    install_requires=install_requires,
    entry_points={
        'nose.plugins.0.10': [
            'django-qunit = django_nose_qunit.nose_plugin:QUnitPlugin',
            'django-qunit-index = django_nose_qunit.nose_plugin:QUnitIndexPlugin'
        ]
    },
)
