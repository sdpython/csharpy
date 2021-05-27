
.. image:: https://travis-ci.com/sdpython/csharpy.svg?branch=master
    :target: https://travis-ci.com/sdpython/csharpy
    :alt: Build status

.. image:: https://ci.appveyor.com/api/projects/status/ldrgt6sxeyfwtoo2?svg=true
    :target: https://ci.appveyor.com/project/sdpython/csharpy
    :alt: Build Status Windows

.. image:: https://circleci.com/gh/sdpython/csharpy/tree/master.svg?style=svg
    :target: https://circleci.com/gh/sdpython/csharpy/tree/master

.. image:: https://badge.fury.io/py/csharpy.svg
    :target: http://badge.fury.io/py/csharpy

.. image:: http://img.shields.io/github/issues/sdpython/csharpy.png
    :alt: GitHub Issues
    :target: https://github.com/sdpython/csharpy/issues

.. image:: https://img.shields.io/badge/license-MIT-blue.svg
    :alt: MIT License
    :target: http://opensource.org/licenses/MIT

.. image:: https://requires.io/github/sdpython/csharpy/requirements.svg?branch=master
     :target: https://requires.io/github/sdpython/csharpy/requirements/?branch=master
     :alt: Requirements Status

.. image:: https://codecov.io/github/sdpython/csharpy/coverage.svg?branch=master
    :target: https://codecov.io/github/sdpython/csharpy?branch=master

.. image:: http://www.xavierdupre.fr/app/csharpy/helpsphinx/_images/nbcov.png
    :target: http://www.xavierdupre.fr/app/csharpy/helpsphinx/all_notebooks_coverage.html
    :alt: Notebook Coverage

.. image:: https://img.shields.io/github/repo-size/sdpython/csharpy
    :target: https://github.com/sdpython/csharpy/
    :alt: size

.. _l-README:

csharpy
=======

Helpers to play with *C#* and *Python*.
It can easily compile and wrap a C# function
into *Python*:

::

    from csharpy.runtime import create_cs_function
    code = "public static double SquareX(double x) {return x*x ; }"
    SquareX = create_cs_function("SquareX", code)
    print(SquareX(4))

It also implements *sphinx* extension to dynamically run *C#* when
the documentation is built.

**Installation**

*Windows*

::

    pip install csharpy

*Linux*

Follow the instructions described in
`config.yml <https://github.com/sdpython/csharpy/blob/master/.circleci/config.yml>`_.

**Links**

* `GitHub/csharpy <https://github.com/sdpython/csharpy/>`_
* `documentation <http://www.xavierdupre.fr/app/csharpy/helpsphinx2/index.html>`_
* `Blog <http://www.xavierdupre.fr/app/csharpy/helpsphinx/blog/main_0000.html#ap-main-0>`_
