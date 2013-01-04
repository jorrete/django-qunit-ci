from setuptools import setup, find_packages

version = '1.0'

setup(
    name="django-qunit-ci",
    version=version,
    author="Jeremy Bowman",
    author_email="jbowman@safaribooksonline.com",
    description="QUnit testing framework for Django that works well with continuous integration software",
    include_package_data=True,
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    zip_safe=False,
    install_requires=[
        'Django>=1.4',
        'requests',
    ],
)
