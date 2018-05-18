"""
@file
@brief Dynamically compile a C# function.
"""
import sys
from ..binaries import AddReference


def create_cs_function(name, code, usings=None, dependencies=None):
    """
    Compiles a :epkg:`C#` function.
    Relies on @see fn run_cs_function.

    @param      name            function name
    @param      code            :epkg:`C#` code
    @param      usings          *using* to add, such as *System*, *System.Linq*, ...
    @param      dependencies    dependencies, can be absolute path file
    @return                     :epkg:`Python` wrapper on the compiled :epkg:`C#`

    Assemblies are expected to be filename with extension.
    If this one is missing, it will be automatically added.

    .. faqref::
        :title: Linq is missing

        No dependencies are added by default and many pieces of code
        relies on standard :epkg:`C#` implemented in ``System.Core``
        which must be added as a dependency. That's what the following
        error tells:

        ::

            System.InvalidOperationException: Error (CS0234): Missing 'Linq'

        Then ``'System.Core'`` must be added the *dependencies* in function
        @see fn create_cs_function or ``-d System.core`` in magic command
        @see me CS.
    """
    AddReference("System")
    # AddReference("System.Collections")
    AddReference("DynamicCS")
    from DynamicCS import DynamicFunction
    from System import String
    from System.Collections.Generic import List
    if sys.platform.startswith("win"):
        ext = ".dll"
    else:
        ext = ".so"

    myarray = List[String]()
    if dependencies:
        for d in dependencies:
            if d.endswith(ext):
                myarray.Add(d)
            else:
                myarray.Add(d + ".dll")
    myarray = myarray.ToArray()
    obj = DynamicFunction.CreateFunction(name, code, usings, myarray)
    return lambda *params: run_cs_function(obj, params)


def run_cs_function(func, params):
    """
    Runs a :epkg:`C#` function.

    @param      func            :epkg:`C#` in memory object
    @param      params          parameters
    @return                     results of the :epkg:`C#` function
    """
    AddReference("DynamicCS")
    from DynamicCS import DynamicFunction
    from System.Collections.Generic import List
    from System import Object

    par = List[Object]()
    for p in params:
        par.Add(p)
    return DynamicFunction.RunFunction(func, par.ToArray())
