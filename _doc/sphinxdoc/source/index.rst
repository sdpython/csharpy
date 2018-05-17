
python3_module_template
=======================

.. only:: html

    .. image:: https://travis-ci.org/sdpython/python3_module_template.svg?branch=master
        :target: https://travis-ci.org/sdpython/python3_module_template
        :alt: Build status

    .. image:: https://ci.appveyor.com/api/projects/status/ldrgt6sxeyfwtoo2?svg=true
        :target: https://ci.appveyor.com/project/sdpython/csharpy
        :alt: Build Status Windows

    .. image:: https://circleci.com/gh/sdpython/python3_module_template/tree/master.svg?style=svg
        :target: https://circleci.com/gh/sdpython/python3_module_template/tree/master

    .. image:: https://badge.fury.io/py/python3_module_template.svg
        :target: http://badge.fury.io/py/python3_module_template

    .. image:: http://img.shields.io/github/issues/sdpython/python3_module_template.png
        :alt: GitHub Issues
        :target: https://github.com/sdpython/python3_module_template/issues

    .. image:: https://img.shields.io/badge/license-MIT-blue.svg
        :alt: MIT License
        :target: http://opensource.org/licenses/MIT

    .. image:: https://coveralls.io/repos/sdpython/python3_module_template/badge.svg?branch=master&service=github
        :target: https://coveralls.io/github/sdpython/python3_module_template?branch=master

    .. image:: https://requires.io/github/sdpython/python3_module_template/requirements.svg?branch=master
         :target: https://requires.io/github/sdpython/python3_module_template/requirements/?branch=master
         :alt: Requirements Status

    .. image:: https://codecov.io/github/sdpython/python3_module_template/coverage.svg?branch=master
        :target: https://codecov.io/github/sdpython/python3_module_template?branch=master

.. image:: nbcov.png
    :target: http://www.xavierdupre.fr/app/python3_module_template/helpsphinx/all_notebooks_coverage.html
    :alt: Notebook Coverage

**Links:** `github <https://github.com/sdpython/python3_module_template/>`_,
`documentation <http://www.xavierdupre.fr/app/python3_module_template/helpsphinx2/index.html>`_,
`travis <https://travis-ci.org/sdpython/python3_module_template>`_,
:ref:`l-README`,
:ref:`blog <ap-main-0>`,
:ref:`l-issues-todolist`,
:ref:`l-completed-todolist`

What is it?
-----------

Helpers to play with C# and Python.
It can easily compile and wrap a C# function
into Python:

::

    from csharpy.runtime import create_cs_function
    code = "public static double SquareX(double x) {return x*x ; }"
    SquareX = create_cs_function("SquareX", code)
    print(SquareX(4))

The module relies in `pythonnet <https://github.com/pythonnet/pythonnet>`_.

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
| :ref:`genindex`      |  :ref:`l-FAQ2`      | :ref:`l-notebooks`  | :ref:`ext-tohelp`  | :ref:`l-statcode`      | `Unit Test Coverage <coverage/index.html>`_    |
+----------------------+---------------------+---------------------+--------------------+------------------------+------------------------------------------------+
