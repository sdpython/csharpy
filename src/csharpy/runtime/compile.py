"""
@file
@brief Dynamically compile a C# function.
"""
# import os
import warnings
from ..binaries import AddReference
from ..csnative.csmain import CsCreateFunction  # pylint: disable=E0611
# from ..csnative import get_clr_path


def create_cs_function(name, code, usings=None, dependencies=None,
                       redirect=False, use_clr=False):
    """
    Compiles a :epkg:`C#` function.
    Relies on @see fn run_cs_function.

    @param      name            function name
    @param      code            :epkg:`C#` code
    @param      usings          *using* to add, such as *System*, *System.Linq*, ...
    @param      dependencies    dependencies, can be absolute path file
    @param      redirect        redirect standard output and error
    @param      has_clr         use :epkg:`pythonnet` or not
    @return                     :epkg:`Python` wrapper on the compiled :epkg:`C#`

    Assemblies are expected to be filename with extension.
    If this one is missing, it will be automatically added.
    If *redirect* is True, the results is a tuple
    ``(return of :epkg:`C#` function, standard output, standard error)``.

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

    The function use dotnet if *use_clr* is False and not :epkg:`pythonnet`.
    Many assemblies can be found in path returned by @see fn get_clr_path.
    """
    if use_clr:
        AddReference("System", use_clr)
        AddReference("System.Collections", use_clr)
        AddReference("System.Collections.Immutable", use_clr)
        AddReference("DynamicCS", use_clr)
        from DynamicCS import DynamicFunction
        from System import String

        with warnings.catch_warnings():
            warnings.simplefilter("ignore", DeprecationWarning)
            from System.Collections.Generic import List

        # dotnet extension is dll even on linux.
        ext = ".dll"
        myarray = List[String]()
        if dependencies:
            for d in dependencies:
                if d.endswith(ext):
                    myarray.Add(d)
                else:
                    myarray.Add(d + ".dll")
        myarray = myarray.ToArray()
        obj = DynamicFunction.CreateFunction(name, code, usings, myarray)
        return lambda *params: run_cs_function_clr(obj, params, redirect=redirect)
    else:
        if usings is None:
            usings = []
        if dependencies is None:
            dependencies = []
        res = CsCreateFunction(name, code, usings, dependencies)
        print(res)
        return res


def run_cs_function_clr(func, params, redirect=False):
    """
    Runs a :epkg:`C#` function with
    :epkg:`pythonnet`.

    @param      func            :epkg:`C#` in memory object
    @param      params          parameters
    @param      redirect        redirect standard output and error
    @return                     results of the :epkg:`C#` function

    If *redirect* is True, the results is a tuple
    ``(return of :epkg:`C#` function, standard output, standard error)``.
    """
    AddReference("DynamicCS", True)
    from DynamicCS import DynamicFunction
    from System.Collections.Generic import List
    from System import Object

    par = List[Object]()
    for p in params:
        par.Add(p)
    if redirect:
        res = DynamicFunction.RunFunctionRedirectOutput(func, par.ToArray())
        return (res.Item1, str(res.Item2).replace("\r", ""), str(res.Item3))
    else:
        return DynamicFunction.RunFunction(func, par.ToArray())
