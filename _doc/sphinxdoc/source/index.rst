
csharpy
=======

.. only:: html

    .. image:: https://travis-ci.org/sdpython/csharpy.svg?branch=master
        :target: https://travis-ci.org/sdpython/csharpy
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

.. image:: nbcov.png
    :target: http://www.xavierdupre.fr/app/csharpy/helpsphinx/all_notebooks_coverage.html
    :alt: Notebook Coverage

**Links:** `github <https://github.com/sdpython/csharpy/>`_,
`documentation <http://www.xavierdupre.fr/app/csharpy/helpsphinx2/index.html>`_
:ref:`l-README`,
:ref:`blog <ap-main-0>`

What is it?
-----------
Helpers to play with :epkg:`C#`, :epkg:`Python`.
The module also relies on
:epkg:`pythonnet` and :epkg:`csharpy`.

.. runpython::
    :showcode:

    from csharpy.runtime import create_cs_function
    code = "public static double SquareX(double x) {return x*x ; }"
    SquareX = create_cs_function("SquareX", code)
    print(SquareX(4))

Documentation
-------------

.. toctree::
    :maxdepth: 1

    api/index
    i_ex
    i_faq
    i_nb

Galleries
---------

.. toctree::
    :maxdepth: 2

    all_notebooks
    blog/blogindex

Installation
------------

*Windows*

::

    pip install csharpy

*Linux*

Follow the instructions described in
`config.yml <https://github.com/sdpython/csharpy/blob/master/.circleci/config.yml>`_.

Build
-----

The package contains :epkg:`C#` and :epkg:`C++` extensions
which can be built with the following instruction:

::

    python setup.py build_ext --inplace

Navigation
----------

.. toctree::
    :maxdepth: 1

    indexmenu
    HISTORY

.. toctree::
    :hidden:

    blog/index_blog

+----------------------+---------------------+---------------------+--------------------+------------------------+------------------------------------------------+
| :ref:`l-modules`     |  :ref:`l-functions` | :ref:`l-classes`    | :ref:`l-methods`   | :ref:`l-staticmethods` | :ref:`l-properties`                            |
+----------------------+---------------------+---------------------+--------------------+------------------------+------------------------------------------------+
| :ref:`modindex`      |  :ref:`l-EX2`       | :ref:`search`       | :ref:`l-license`   | :ref:`l-changes`       | :ref:`l-README`                                |
+----------------------+---------------------+---------------------+--------------------+------------------------+------------------------------------------------+
| :ref:`genindex`      |  :ref:`l-FAQ2`      | :ref:`l-notebooks`  |                    | :ref:`l-statcode`      | `Unit Test Coverage <coverage/index.html>`_    |
+----------------------+---------------------+---------------------+--------------------+------------------------+------------------------------------------------+
