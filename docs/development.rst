Development Utilities
=====================

Running tests
-------------

1. Install the prerequisites::

    $ pip install -r requirements/tests.txt

2. Run the tests::

    $ tox

The first run may take a while as it builds a virtualenv and installs everything in it, subsequent ones will be much faster.  To rebuild the virtualenv later with updated dependencies::

    $ tox -r

JavaScript sanity checks
------------------------

When changing the JavaScript, it's a good idea to run JSHint to look for likely
problems.  First install Grunt::

    $ sudo npm install -g grunt-cli
    $ npm install

If you installed node via brew, make sure that "/usr/local/share/npm/bin" is
in your PATH.  You can then run JSHint on all the JS files in nest with one
command::

    $ grunt

To run JShint on a single file::

    $ jshint path/to/file.js

The JSHint options are configured in django_nose_qunit/static/django_nose_qunit/test/.jshintrc
(for test files) and .jshintrc (for all other JavaScript files); the same
configuration is used both when runing jshint directly and when running grunt.
In cases where you need to knowingly break the usual style rules in special
cases, you can do so via ``/*jshint ...*/`` directives; do this sparingly, if
at all.

Generating Documentation
------------------------

Documentation for this package is generated using
`sbo-sphinx <https://github.com/safarijv/sbo-sphinx>`_.  To generate the docs
locally with any changes you may have made::

    $ pip install -r requirements/development.txt
    $ cd docs
    $ DJANGO_SETTINGS_MODULE=test_settings sphinx-build -b html . _build
