// Modified from https://github.com/Microsoft/NimbusML.
// See https://docs.microsoft.com/en-us/dotnet/core/tutorials/netcore-hosting.

#include <pybind11/pybind11.h>
#include <pybind11/operators.h>
#include <pybind11/numpy.h>
#include <pybind11/stl.h>
#include <pybind11/complex.h>
#include <sysmodule.h>
#include "stdafx.h"
#include <string>
#include <iostream>
#include "_filesystem.h"


void retrieve_dotnetcore_path(std::string &path_clr)
{
    // This function assumes dotnetcore2 is installed.
    //py::scoped_interpreter guard{};
    pybind11::module dnc = pybind11::module::import("dotnetcore2.runtime");
    auto fct = dnc.attr("_get_bin_folder");
    std::string value = fct().cast<std::string>();
    fs::path path = value;
    path /= std::string("shared");
    path /= std::string("Microsoft.NETCore.App");
    fs::path full_path;
    fs::path look;
    std::string dll("Microsoft.CSharp.dll");
    for (const auto & full_path : fs::directory_iterator(path)) {
        look = full_path / dll;
        if (fs::exists(look)) {
            fs::path fpath = full_path;
            auto native = fpath.native();
            path_clr = std::string(native.begin(), native.end());
            return;
        }
    }
    throw std::runtime_error("Unable to find dotnetcore2.");
}


#include "csmain.hpp"

/////////////////////////////////////////////////
// Declares functions with all the same signature
/////////////////////////////////////////////////

DECLARE_FCT_NAME(RandomString)

std::string RandomString()
{
    DataStructure data;
    cs_RandomString(&data);
    std::string res = std::string((char*)data.outputs);
    delete data.outputs;
    return res;
}


DECLARE_FCT_NAME(CsUpper)

std::string CsUpper(const std::string &text)
{
    DataStructure data;
    data.inputs = (void*) text.c_str();
    cs_CsUpper(&data);
    std::string res = std::string((char*)data.outputs);
    delete data.outputs;
    return res;
}


DECLARE_FCT_NAME(CreateFunction)

typedef struct CreateFunctionInput
{
public:
    char * name;
    char * code;
    char ** usings;
    char ** dependencies;
} CreateFunctionInput;

std::pair<__int64, std::string> CsCreateFunction(const std::string& functionName,
                                                 const std::string& functionCode,
                                                 const std::vector<std::string>& usings,
                                                 const std::vector<std::string>& dependencies)
{
    CreateFunctionInput input;
    input.name = (char*)functionName.c_str();
    input.code = (char*)functionCode.c_str();
    
    char ** c_usings = new char* [usings.size()+1];
    for(int i = 0; i < usings.size(); ++i)
        c_usings[i] = (char*)usings[i].c_str();
    c_usings[usings.size()] = NULL;
    input.usings = c_usings;    
    
    char ** c_dependencies = new char* [dependencies.size()+1];
    for(int i = 0; i < dependencies.size(); ++i)
        c_dependencies[i] = (char*)dependencies[i].c_str();
    c_dependencies[dependencies.size()] = NULL;
    input.dependencies = c_dependencies;    

    __int64 oid;
    DataStructure data;
    data.inputs = &input;
    data.outputs = &oid;
    cs_CreateFunction(&data);
    std::string res = std::string((char*)data.exc);
    delete data.exc;
    delete input.usings;
    delete input.dependencies;
    if (oid == -1)
        throw std::runtime_error(res);
    return std::pair<__int64, std::string>(oid, res);
}


////////////////////
// Module definition
////////////////////


PYBIND11_MODULE(csmain, m) {
    Py_Initialize();
    
    retrieve_dotnetcore_path(_coreclrpath_default);

    m.doc() = "Calls C# functions from C++.";

    static pybind11::exception<CsNativeExecutionError> exc(m, "CsNativeExecutionError");
    pybind11::register_exception_translator([](std::exception_ptr p) {
        try {
            if (p)
                std::rethrow_exception(p);
        }
        catch (const std::exception &e) {
            exc(e.what());
        }
    });
    
    m.def("cs_start", &cs_start,
        R"pbdoc(
    Loads the DLL in memory,
    sets up the constants to call C# function from this C extension.

    :param coreclrpath: path to dotnet, usuall the result of @see fn get_clr_path
    :param CSharpyPyExtension: absolute location of DLL CSharpyPyExtension)pbdoc");
    
    m.def("_core_clr_path", &_core_clr_path,
          "Returns path to dot net used to load this assemblies.");

    m.def("_core_clr_path_default", &_core_clr_path_default,
          "Returns path to dot net used to load this assemblies.");

    m.def("cs_end", &cs_end,
          "Unload the DLL.");    

    m.def("CsCreateFunction", &CsCreateFunction,
        R"pbdoc(
    Compiles a C# function and returns an identifier which refers to the
    created method.
    :param name: method name in the given code
    :param code: function code
    :param usings: list of references the code is usings
    :param dependencies: list of dependencies the code needs
    :return: *(__int64, str)* idendifier, the method is stored as a static
        object in the Bridge, the string contains either an exception message
        or the signature of the compiled function.
    
    .. faqref::
        :title: Caught an unknown exception!
        
        The DLL needs to be initialized to be able to call
        C# functions. That's the purpose of method
        @see fn start otherwise any call to a function
        calling a C# function will display the following
        error message:
        
        ::
        
            Caught an unknown exception!
    )pbdoc");    

    m.def("SquareNumber", &SquareNumber,
        "Returns the square of a number as an example for C#.");

    m.def("RandomString", &RandomString,
        "Returns a string with a non English character.");

    m.def("CsUpper", &CsUpper,
        R"pbdoc(
    Converts a string into upper case using a C# function.
    Shows a way to expose a function taking a string and returning
    another string.

    :param text: any string)pbdoc");

    m.def("dotnetcore_path", []() -> std::string {
        std::string path_clr;
        retrieve_dotnetcore_path(path_clr);
        return path_clr;
    }, "Returns the path for dotnetcore binaries.");
}
