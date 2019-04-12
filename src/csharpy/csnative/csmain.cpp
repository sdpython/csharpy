// Modified from https://github.com/Microsoft/NimbusML.
// See https://docs.microsoft.com/en-us/dotnet/core/tutorials/netcore-hosting.

#include <pybind11/pybind11.h>
#include <pybind11/operators.h>
#include "stdafx.h"
#include <string>
#include <iostream>


#if _MSC_VER
#include "WinInterface.h"
typedef WinNetInterface NetInterface;
#else
#include "UnixInterface.h"
typedef UnixNetInterface NetInterface;
#endif


struct CsNativeExecutionError : std::exception
{
    CsNativeExecutionError(const char *message) : msg_(message) { }
    virtual char const *what() const noexcept { return msg_.c_str(); }

private:
    std::string msg_;
};

std::string _coreclrpath;
std::string _CSharpyPyExtension;
static NetInterface * _interface = NULL;


NetInterface * GetNetInterface(const char *coreclrpath = NULL, bool remove = false)
{
    if (_interface == NULL) {
        if (coreclrpath == NULL || strlen(coreclrpath) == 0)
            throw CsNativeExecutionError("coreclrpath is empty or a function is called before calling function cs_start.");
        _interface = new NetInterface(coreclrpath);
        _coreclrpath = coreclrpath;
        if (_interface == NULL)
            throw CsNativeExecutionError("Cannot not load CoreClr.");
    }
    else if (remove)
    {
        delete _interface;
        _interface = NULL;
    }
    return _interface;
}


void* GetSquareNumberFunction()
{
    static void* _fct = NULL;
    if (_fct == NULL) {
        NetInterface * dll = GetNetInterface(_coreclrpath.c_str());
        if (dll == NULL)
            throw CsNativeExecutionError("Cannot get a pointer to NetInterface.");
        void* fct = dll->CreateDeledate(
            _CSharpyPyExtension.c_str(),
            W("CSharPyExtension, Version=0.1.0, Culture=neutral"),
            W("CSharPyExtension.StaticExample"),
            W("SquareNumber"));
        if (fct == NULL)
            throw CsNativeExecutionError("Cannot retrieve function SquareNumber.");
        _fct = fct;
    }
    return _fct;
}


typedef double (STDCALL * TypeSquareNumber)(double);


double SquareNumber(double x)
{
    static TypeSquareNumber fct = (TypeSquareNumber)GetSquareNumberFunction();
    std::cout << "x = " << x << " fct is NULL " << (fct == NULL) << "\n";
    double r = (*fct)(x);
    std::cout << "r = " << r << "\n";
    return r;
}


void * cs_start(const std::string& coreclrpath,
                const std::string& CSharpyPyExtension)
{
    _CSharpyPyExtension = CSharpyPyExtension;
    return GetNetInterface(coreclrpath.c_str());
}


void cs_end()
{
    GetNetInterface(NULL, true);
}


const char * _core_clr_path()
{
    return _coreclrpath.c_str();
}


PYBIND11_MODULE(csmain, m) {
    Py_Initialize();

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

    m.def("cs_end", &cs_end,
          "Unload the DLL.");    

    m.def("SquareNumber", &SquareNumber,
        "Returns the square of a number as an example for C#.");
}
