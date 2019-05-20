// Modified from https://github.com/Microsoft/NimbusML.
// See https://docs.microsoft.com/en-us/dotnet/core/tutorials/netcore-hosting.

#include "stdafx.h"
#include <string>
#include <iostream>
#include "_filesystem.h"

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


NetInterface * GetNetInterface(const char *coreclrpath = NULL, bool remove = false)
{
    if (_interface == NULL) {
        if (coreclrpath == NULL || strlen(coreclrpath) == 0)
            retrieve_dotnetcore_path(_coreclrpath);
        else
            _coreclrpath = coreclrpath;
        int extPos = _coreclrpath.length() - 4;
        if ((extPos <= 0) || (_coreclrpath.compare(extPos, 4, ".dll") == 0) || 
            (_coreclrpath.compare(extPos + 1, 3, ".so") == 0)) {
            std::stringstream message;
            message << "_coreclrpath is wrong '" << _coreclrpath << "'\n";
            throw CsNativeExecutionError(message.str().c_str());
        }
        
        _interface = new NetInterface(_coreclrpath.c_str());
        if (_interface == NULL) {
            std::stringstream message;
            message << "Cannot not load NetInterface, _coreclrpath='" << _coreclrpath << "'\n";
            throw CsNativeExecutionError(message.str().c_str());
        }
    }
    else if (remove)
    {
        delete _interface;
        _interface = NULL;
    }
    return _interface;
}


typedef double (STDCALL TypeSquareNumber)(double);


TypeSquareNumber* GetSquareNumberFunction()
{
    static TypeSquareNumber* _fct = NULL;
    if (_fct == NULL) {
        NetInterface * dll = GetNetInterface(_coreclrpath.c_str());
        if (dll == NULL)
            throw CsNativeExecutionError("Cannot get a pointer to NetInterface.");
        void* fct = dll->CreateDelegate(
            _CSharpyPyExtension.c_str(),
            W("CSharPyExtension"),
            W("CSharPyExtension.CsBridge"),
            W("SquareNumber"));
        if (fct == NULL)
            throw CsNativeExecutionError("Cannot retrieve function SquareNumber.");
        _fct = (TypeSquareNumber*)fct;
    }
    return _fct;
}


double SquareNumber(double x)
{
    // Exception do not work well.
    // They should be handled in C# as it makes python crash.
    static TypeSquareNumber* fct = (TypeSquareNumber*)GetSquareNumberFunction();
    double r = fct(x);
    return r;
}


typedef int (STDCALL TypeAgnosticFunction)(DataStructure * data);


TypeAgnosticFunction* GetAgnosticFunction(const FUNCTION_NAME_TYPE function_name)
{
    NetInterface * dll = GetNetInterface(_coreclrpath.c_str());
    if (dll == NULL)
        throw CsNativeExecutionError("Cannot get a pointer to NetInterface.");
    void* fct = dll->CreateDelegate(
        _CSharpyPyExtension.c_str(),
        W("CSharPyExtension"),
        W("CSharPyExtension.CsBridge"),
        function_name);
    if (fct == NULL)
        throw CsNativeExecutionError("Cannot retrieve a function.");
    return (TypeAgnosticFunction*)fct;
}


MANAGED_CALLBACK(void) CallBackMalloc(int size, void **ptr)
{
    *ptr = malloc(size);
}


MANAGED_CALLBACK(void) CallPrintf(const char * msg)
{
    if (msg != NULL)
        std::cout << msg;
}

MANAGED_CALLBACK(void) CallPrintfw(const wchar_t * msg)
{
    if (msg != NULL)
        std::cout << msg;
}

MANAGED_CALLBACK(void) CallPythonPrintf(const char * msg)
{
#ifdef SKIP_PYBIND11
    if (msg != NULL)
        std::cout << "++" << msg;
#else
    if (msg != NULL)
        pybind11::print(msg);
#endif
}

int CallAgnosticFunction(TypeAgnosticFunction * fct, DataStructure * data, bool redirect)
{
    if (data == NULL)
        throw CsNativeExecutionError("data pointer cannot be NULL.");
    data->allocate_fct = (void*)&CallBackMalloc;
    data->printf_fct = redirect ? (void*)&CallPythonPrintf : NULL;
    return (*fct)(data);
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


#define DECLARE_FCT_NAME(name)\
    int cs_##name(DataStructure * data, bool redirect)      \
    {                                                       \
        static TypeAgnosticFunction * fct = NULL;           \
        if (fct == NULL)                                    \
            fct = GetAgnosticFunction(W(#name));            \
        return CallAgnosticFunction(fct, data, redirect);   \
    }
