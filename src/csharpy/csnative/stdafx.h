// Modified from https://github.com/Microsoft/NimbusML.

#pragma once

#if defined( _MSC_VER )
//
// Exclude rarely-used stuff from Windows headers
//
#define WIN32_LEAN_AND_MEAN             
#define EXPORT_API(ret) extern "C" __declspec(dllexport) ret __stdcall
#define STDCALL __stdcall
#define W(str) L ## str
#define MANAGED_CALLBACK(ret) ret __stdcall
#define MANAGED_CALLBACK_PTR(ret, name) ret (__stdcall *name)
#define CLASS_ALIGN __declspec(align(8))

typedef __int64				CxInt64;
typedef unsigned __int64	CxUInt64;
typedef unsigned char		BYTE;

//
// Windows Header Files:
//
#include <windows.h>

#else // Linux/Mac
// For Unix, ignore __stdcall.
#define STDCALL
#define W(str) str
#define FAILED(Status) ((Status) < 0)
#define MANAGED_CALLBACK(ret) ret
#define MANAGED_CALLBACK_PTR(ret, name) ret ( *name)
#define CLASS_ALIGN __attribute__((aligned(8)))

#ifdef BOOST_NO_CXX11_NULLPTR
#define nullptr 0
#endif //BOOST_NO_CXX11_NULLPTR

typedef long long	CxInt64;
typedef unsigned long long	CxUInt64;
typedef unsigned char	BYTE;

#endif //_MSC_VER

#include <pybind11/pybind11.h>
#include <string>
#include <exception>
#include <pybind11/numpy.h>
//#include <pybind11/scope.h>
#include <sysmodule.h>

namespace bp = pybind11;
//namespace np = pybind11::
#if !defined(extract_or_cast)
#define extract_or_cast cast
#define has_key_or_contains contains
#define numpy_array bp::array
#define numpy_array_bool bp::array_t<bool>
#define numpy_array_int bp::array_t<int>
#define numpy_array_double bp::array_t<double>
#define numpy_array_float bp::array_t<float>
#endif
