// Modified from https://github.com/Microsoft/NimbusML.
// See https://docs.microsoft.com/en-us/dotnet/core/tutorials/netcore-hosting.

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


typedef double (STDCALL TypeSquareNumber)(double);


TypeSquareNumber* GetSquareNumberFunction()
{
    static TypeSquareNumber* _fct = NULL;
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

TypeAgnosticFunction* GetAgnosticFunction(const wchar_t * function_name)
{
    NetInterface * dll = GetNetInterface(_coreclrpath.c_str());
    if (dll == NULL)
        throw CsNativeExecutionError("Cannot get a pointer to NetInterface.");
    void* fct = dll->CreateDeledate(
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
        printf(msg);
}

MANAGED_CALLBACK(void) CallPrintfw(const wchar_t * msg)
{
    if (msg != NULL)
        std::cout << msg;
}

int CallAgnosticFunction(TypeAgnosticFunction * fct, DataStructure * data)
{
    if (data == NULL)
        throw CsNativeExecutionError("data pointer cannot be NULL.");
    data->allocate_fct = (void*)&CallBackMalloc;
    data->printfw_fct = (void*)&CallPrintfw;
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
    int cs_##name(DataStructure * data)             \
    {                                               \
        static TypeAgnosticFunction * fct = NULL;   \
        if (fct == NULL)                            \
            fct = GetAgnosticFunction(W(#name));    \
        return CallAgnosticFunction(fct, data);     \
    }
