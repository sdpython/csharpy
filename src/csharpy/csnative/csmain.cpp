// Modified from https://github.com/Microsoft/NimbusML.
// See https://docs.microsoft.com/en-us/dotnet/core/tutorials/netcore-hosting.

#include <pybind11/pybind11.h>
#include <pybind11/operators.h>
#include "stdafx.h"
#include <string>
#include <iostream>
#include <filesystem>

#if __cplusplus < 201402L
namespace fs = std::experimental::filesystem;
#else
namespace fs = std::filesystem;
#endif

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

static std::string _coreclrpath;
static std::string _coreclrpath_default;
static std::string _CSharpyPyExtension;
static NetInterface * _interface = NULL;


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
    throw CsNativeExecutionError("Unable to find dotnetcore2.");
}


NetInterface * GetNetInterface(const char *coreclrpath = NULL, bool remove = false)
{
    if (_interface == NULL) {
        if (coreclrpath == NULL || strlen(coreclrpath) == 0)
            retrieve_dotnetcore_path(_coreclrpath);
        else
            _coreclrpath = coreclrpath;
        _interface = new NetInterface(_coreclrpath.c_str());
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
            W("CSharPyExtension"),
            W("CSharPyExtension.CsBridge"),
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
    // Exception do not work well.
    // They should be handled in C# as it makes python crash.
    static TypeSquareNumber fct = (TypeSquareNumber)GetSquareNumberFunction();
    double r = fct(x);
    return r;
}


typedef void (STDCALL * TypeRandomString)(std::string &);

void* GetRandomStringFunction()
{
    static void* _fct = NULL;
    if (_fct == NULL) {
        NetInterface * dll = GetNetInterface(_coreclrpath.c_str());
        if (dll == NULL)
            throw CsNativeExecutionError("Cannot get a pointer to NetInterface.");
        void* fct = dll->CreateDeledate(
            _CSharpyPyExtension.c_str(),
            W("CSharPyExtension"),
            W("CSharPyExtension.CsBridge"),
            W("RandomString"));
        if (fct == NULL)
            throw CsNativeExecutionError("Cannot retrieve function RandomString.");
        _fct = fct;
    }
    return _fct;
}

std::string RandomString()
{
    // Exception do not work well.
    // They should be handled in C# as it makes python crash.
    static TypeRandomString fct = (TypeRandomString)GetRandomStringFunction();
    std::string dst;
    fct(dst);
    return dst;
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


const char * _core_clr_path_default()
{
    return _coreclrpath_default.c_str();
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
}
