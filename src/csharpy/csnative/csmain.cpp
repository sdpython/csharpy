// Modified from https://github.com/Microsoft/NimbusML.
// See https://docs.microsoft.com/en-us/dotnet/core/tutorials/netcore-hosting.

#include <pybind11/pybind11.h>
#include <pybind11/operators.h>
#include <pybind11/numpy.h>
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
