Development Utilities
=====================

Running tests
-------------

1. Install the prerequisites::

    pip install -r requirements/tests.txt

2. Run the tests::

    tox

The first run may take a while as it builds a virtualenv and installs everything in it, subsequent ones will be much faster.  To rebuild the virtualenv later with updated dependencies::

    tox -r

JavaScript Sanity Checks
------------------------

When changing the JavaScript, it's a good idea to run JSHint to look for likely
problems.  First install Grunt::

    sudo npm install -g grunt-cli
    npm install

If you installed node via brew, make sure that "/usr/local/share/npm/bin" is
in your PATH.  You can then run JSHint on all the JS files in nest with one
command::

    grunt

To run JShint on a single file::

    jshint path/to/file.js

The JSHint options are configured in django_nose_qunit/static/django_nose_qunit/test/.jshintrc
(for test files) and .jshintrc (for all other JavaScript files); the same
configuration is used both when runing jshint directly and when running grunt.
In cases where you need to knowingly break the usual style rules in special
cases, you can do so via ``/*jshint ...*/`` directives; do this sparingly, if
at all.

Python Sanity Checks
--------------------

The Python code can also be easily checked for a variety of possible problems
and discouraged coding style elements.  To perform these checks, first install
the testing dependencies as described above and then run::

    tox -e flake8

This uses `flake8 <https://pypi.python.org/pypi/flake8>`_ to check for
`PEP 8 <http://legacy.python.org/dev/peps/pep-0008/>`_ compliance, some common
errors involving imports and variables, and code with unusually high
`cyclomatic complexity <https://en.wikipedia.org/wiki/Cyclomatic_complexity>`_.

Generating Documentation
------------------------

Documentation for this package is generated using `Sphinx <http://sphinx-doc.org/>`_
and some extensions for it from `sbo-sphinx <https://github.com/safarijv/sbo-sphinx>`_.
To generate the docs locally with any changes you may have made, first make
sure you've installed the testing prerequisites as described above.  Then run::

    tox -e docs

The ``README.rst`` file in the root directory also serves as the package
description on PyPI, so it needs to comply with a more limited range of reST
syntax than Sphinx allows.  Check the output of the "validate_readme.py"
command at the end of the above tox command to verify that PyPI should display
it formatted correctly instead of falling back to plain text.
