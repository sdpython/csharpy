// Modified from https://github.com/Microsoft/NimbusML.

#include <pybind11/pybind11.h>
#include <pybind11/operators.h>
#include "cmain.h"


#if _MSC_VER
#include "WinInterface.h"
typedef WinMlInterface NetInterface;
#else
#include "UnixInterface.h"
typedef UnixNetInterface NetInterface;
#endif


void * EnsureExec(const char *cslib, const char *coreclrpath)
{
    if (g_mlnetInterface == nullptr)
        g_mlnetInterface = new NetInterface();

    if (g_exec == nullptr)
    {
    }
    return g_exec;
}    

void * CallSharp()
{
    GENERICEXEC exec = EnsureExec(cslibpath, coreclrpath);
    if (exec == nullptr)
        throw std::invalid_argument("Failed to communicate with the managed library. Path searched: "
            + cslibpath + " and " + coreclrpath);
}

double SquareNumber(double x)
{
}


PYBIND11_MODULE(csmain, m) {
    Py_Initialize();
    
	m.doc() = "Calls C# function from C++.";
    
    static bp::exception<BridgeExecutionError> exc(m, "BridgeExecutionError");
    bp::register_exception_translator([](std::exception_ptr p) {
        try {
            if (p)
                std::rethrow_exception(p);
        }
        catch (const std::exception &e) {
            exc(e.what());
        }
    });
    
    m.def("SquareNumber", &SquareNumber,
          "Returns the square of a number as an example for C#.");
}
