"""
@file
@brief Dynamically compile a C# function.
"""
import clr


def create_cs_function(name, code, dependencies = None):
    """
    Compiles a :epkg:`C#` function.
    Relies on @see fn run_cs_function.
    
    @param      name            function name
    @param      code            :epkg:`C#` code
    @param      dependencies    dependencies (*System*, ...)
    @return                     :epkg:`Python` wrapper on the compiled :epkg:`C#`
    """
    clr.AddReference("DynamicCS")
    from DynamicCS import DynamicFunction
    from System import String
    from System.Collections.Generic import List
 
    if dependencies is not None and len(dependencies) > 0 :
        myarray = List[String]()
        for i,d in enumerate(dependencies):
            myarray.Add( d )
        myarray = myarray.ToArray()
    else:
        myarray = List[String]().ToArray()
     
    obj = DynamicFunction.CreateFunction(name, code, myarray)
    return lambda *params: run_cs_function(obj, params)
 
 
def run_cs_function(func, params):
    """
    Runs a :epkg:`C#` function.
    
    @param      func            :epkg:`C#` in memory object
    @param      params          parameters
    @return                     results of the :epkg:`C#` function
    """
    clr.AddReference("DynamicCS")
    from DynamicCS import DynamicFunction
    from System.Collections.Generic import List
    from System import Object
 
    par = List[Object]()
    for p in params :
        par.Add ( p )
    return DynamicFunction.RunFunction(func, par.ToArray())
