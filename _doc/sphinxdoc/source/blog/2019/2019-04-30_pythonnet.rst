
.. blogpost::
    :title: pythonnet with only netcore
    :keywords: C#, netcore, pythonnet
    :date: 2019-04-30
    :categories: C#

    :epkg:`pythonnet` does not work without  *.NetFramework*,
    there is an initiative to make it work with :epkg:`dotnet` only.
    I tried to do something about it but I lost patience in the process
    then I discovered this fork which does build only with :epkg:`dotnet`:
    `djoyce82/pythonnet <https://github.com/djoyce82/pythonnet>`_.
    To build it after it is cloned:

    ::

        python setup.py bdist_wheel --xplat
