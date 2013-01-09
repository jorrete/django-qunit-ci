from setuptools import setup, find_packages

version = '1.0'

setup(
    name="django-nose-qunit",
    version=version,
    author="Jeremy Bowman",
    author_email="jbowman@safaribooksonline.com",
    description="Integrate QUnit JavaScript tests into a Django test suite via nose",
    include_package_data=True,
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    zip_safe=False,
    install_requires=[
        'Django>=1.4',
        'django-nose',
        'requests',
    ],
    entry_points={
        'nose.plugins.0.10': [
            'django-qunit = django_nose_qunit.nose_plugin:QUnitPlugin'
        ]
    },
)
