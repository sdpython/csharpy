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
#define FUNCTION_NAME_TYPE wchar_t*

#else // Linux/Mac
// For Unix, ignore __stdcall.
#define STDCALL
#define W(str) str
#define FAILED(Status) ((Status) < 0)
#define MANAGED_CALLBACK(ret) ret
#define MANAGED_CALLBACK_PTR(ret, name) ret ( *name)
#define CLASS_ALIGN __attribute__((aligned(8)))
#define FUNCTION_NAME_TYPE char*

typedef long long	CxInt64;
typedef unsigned long long	CxUInt64;
typedef unsigned char	BYTE;

#endif //_MSC_VER

#include <string>
#include <exception>

typedef struct DataStructure
{
public:
    void* exc;          // Stores an exception. If not NULL, it should a string.    
    void* inputs;       // Inputs.    
    void* outputs;      // Outputs.    
    void* allocate_fct; // Allocates spaces in C++ world: allocate(int size, void** output)
    void* printf_fct;   // Printf function: printf(char msg)
} DataStructure;

typedef int type_agnostic_function(DataStructure *);
