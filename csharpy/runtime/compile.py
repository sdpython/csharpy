"""
@file
@brief Dynamically compile a C# function.
"""
import warnings
from ..binaries import AddReference


def create_cs_function(name, code, usings=None, dependencies=None,
                       redirect=False, use_clr=False, verbose=False):
    """
    Compiles a :epkg:`C#` function.
    Relies on @see fn run_cs_function.

    @param      name            function name
    @param      code            :epkg:`C#` code
    @param      usings          *using* to add, such as *System*, *System.Linq*, ...
    @param      dependencies    dependencies, can be absolute path file
    @param      redirect        redirect standard output and error
    @param      has_clr         use :epkg:`pythonnet` or not
    @param      verbose         verbose
    @return                     :epkg:`Python` wrapper on the compiled :epkg:`C#`

    Assemblies are expected to be filename with extension.
    If this one is missing, it will be automatically added.
    If *redirect* is True, the results is a tuple
    ``(return of :epkg:`C#` function, standard output, standard error)``.
    The function use dotnet if *use_clr* is False and not :epkg:`pythonnet`.
    Many assemblies can be found in path returned by @see fn get_clr_path.
    """
    if use_clr:
        AddReference("System", use_clr, verbose=verbose)
        AddReference("System.Collections", use_clr, verbose=verbose)
        AddReference("System.Collections.Immutable", use_clr, verbose=verbose)
        AddReference("System.Linq", use_clr, verbose=verbose)
        AddReference("System.Runtime", use_clr, verbose=verbose)
        res = AddReference("DynamicCS", use_clr, verbose=verbose)
        from System import String
        try:
            from DynamicCS import DynamicFunction
        except ModuleNotFoundError as e:
            raise ImportError(
                "Unable to find 'DynamicFunction' in 'DynamicCS' (imported [{}])"
                ".".format(res)) from e

        with warnings.catch_warnings():
            warnings.simplefilter("ignore", DeprecationWarning)
            from System.Collections.Generic import List, __file__ as f_col  # pylint: disable=W0611
            from System.Linq import __file__ as f_linq  # pylint: disable=W0611,E0401

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
        obj = DynamicFunction.CreateFunction(
            name, code, usings, myarray, None)
        return lambda *params: run_cs_function_clr(
            obj, params, redirect=redirect)
    else:
        if usings is None:
            usings = []
        if dependencies is None:
            dependencies = []
        from ..csnative.csmain import CsCreateFunction  # pylint: disable=E0611,E0401
        res = CsCreateFunction(name, code, usings, dependencies)
        from ..csnative.csmain import CallArrayInt32String  # pylint: disable=E0611,E0401
        from ..csnative.csmain import CallDoubleDouble  # pylint: disable=E0611,E0401
        from ..csnative.csmain import CallArrayDoubleArrayDouble  # pylint: disable=E0611,E0401
        from ..csnative.csmain import CallVoid  # pylint: disable=E0611,E0401
        sigs = {
            'Double->Double': CallDoubleDouble,
            'Double[]->Double[]': CallArrayDoubleArrayDouble,
            'String->Int32[]': CallArrayInt32String,
            '->Void': CallVoid,
        }

        fct = res[0]
        fctpy = sigs[res[1]]
        return lambda *args: fctpy(fct, redirect, *args)


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
    return DynamicFunction.RunFunction(func, par.ToArray())
