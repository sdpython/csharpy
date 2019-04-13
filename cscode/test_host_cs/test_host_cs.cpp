#include <iostream>

#include <stdio.h>
#include "mscoree.h"	// Generated from mscoree.idl

#define W(str) L ## str

static const wchar_t *coreCLRInstallDirectory = L"c:\\Python372_x64\\lib\\site-packages\\dotnetcore2\\bin\\shared\\Microsoft.NETCore.App\\2.1.5";
static const wchar_t* coreCLRDll = L"coreclr.dll";

HMODULE LoadCoreCLR(const wchar_t* directoryPath);

typedef void (STDMETHODCALLTYPE MainMethodFp)(LPWSTR* args);

int main1()
{
    printf("Sample CoreCLR Host\n\n");

    wchar_t targetApp[MAX_PATH] = L"C:\\xavierdupre\\__home_\\GitHub\\csharpy\\cscode\\bin\\x64.Debug\\CSharPyExtension\\netstandard2.0\\CSharPyExtension.dll";

    wchar_t targetAppPath[MAX_PATH];
    wcscpy_s(targetAppPath, targetApp);

    // Walk the string backwards looking for '\'
    size_t i = wcsnlen(targetAppPath, MAX_PATH);
    while (i > 0 && targetAppPath[i - 1] != L'\\') i--;

    // Replace the first '\' found (if any) with \0
    if (i > 0)
        targetAppPath[i - 1] = L'\0';

    HMODULE coreCLRModule;
    wchar_t coreRoot[MAX_PATH];
    size_t outSize;
    _wgetenv_s(&outSize, coreRoot, MAX_PATH, L"CORE_ROOT");
    coreCLRModule = LoadCoreCLR(coreRoot);
    if (!coreCLRModule)
    {
        wcscpy_s(coreRoot, MAX_PATH, targetAppPath);
        coreCLRModule = LoadCoreCLR(coreRoot);
    }

    if (!coreCLRModule)
    {
        ::ExpandEnvironmentStringsW(coreCLRInstallDirectory, coreRoot, MAX_PATH);
        coreCLRModule = LoadCoreCLR(coreRoot);
    }

    if (!coreCLRModule)
    {
        printf("ERROR - CoreCLR.dll could not be found");
        return -1;
    }
    else
    {
        wprintf(L"CoreCLR loaded from %s\n", coreRoot);
    }

    ICLRRuntimeHost4* runtimeHost;
    FnGetCLRRuntimeHost pfnGetCLRRuntimeHost =
        (FnGetCLRRuntimeHost)::GetProcAddress(coreCLRModule, "GetCLRRuntimeHost");
    if (!pfnGetCLRRuntimeHost)
    {
        printf("ERROR - GetCLRRuntimeHost not found");
        return -1;
    }

    HRESULT hr = pfnGetCLRRuntimeHost(IID_ICLRRuntimeHost4, (IUnknown**)&runtimeHost);
    if (FAILED(hr))
    {
        printf("ERROR - Failed to get ICLRRuntimeHost4 instance.\nError code:%x\n", hr);
        return -1;
    }

    hr = runtimeHost->SetStartupFlags(
        static_cast<STARTUP_FLAGS>(
            // STARTUP_FLAGS::STARTUP_SERVER_GC |								// Use server GC
            // STARTUP_FLAGS::STARTUP_LOADER_OPTIMIZATION_MULTI_DOMAIN |		// Maximize domain-neutral loading
            // STARTUP_FLAGS::STARTUP_LOADER_OPTIMIZATION_MULTI_DOMAIN_HOST |	// Domain-neutral loading for strongly-named assemblies
            STARTUP_FLAGS::STARTUP_CONCURRENT_GC |						// Use concurrent GC
            STARTUP_FLAGS::STARTUP_SINGLE_APPDOMAIN |					// All code executes in the default AppDomain
                                                                        // (required to use the runtimeHost->ExecuteAssembly helper function)
            STARTUP_FLAGS::STARTUP_LOADER_OPTIMIZATION_SINGLE_DOMAIN	// Prevents domain-neutral loading
            )
    );

    if (FAILED(hr))
    {
        printf("ERROR - Failed to set startup flags.\nError code:%x\n", hr);
        return -1;
    }

    hr = runtimeHost->Start();
    if (FAILED(hr))
    {
        printf("ERROR - Failed to start the runtime.\nError code:%x\n", hr);
        return -1;
    }
    else
    {
        printf("Runtime started\n");
    }

    int appDomainFlags =
        // APPDOMAIN_FORCE_TRIVIAL_WAIT_OPERATIONS |		// Do not pump messages during wait
        // APPDOMAIN_SECURITY_SANDBOXED |					// Causes assemblies not from the TPA list to be loaded as partially trusted
        APPDOMAIN_ENABLE_PLATFORM_SPECIFIC_APPS |			// Enable platform-specific assemblies to run
        APPDOMAIN_ENABLE_PINVOKE_AND_CLASSIC_COMINTEROP |	// Allow PInvoking from non-TPA assemblies
        APPDOMAIN_DISABLE_TRANSPARENCY_ENFORCEMENT;			// Entirely disables transparency checks

    size_t tpaSize = 100 * MAX_PATH; // Starting size for our TPA (Trusted Platform Assemblies) list
    wchar_t* trustedPlatformAssemblies = new wchar_t[tpaSize];
    trustedPlatformAssemblies[0] = L'\0';

    const wchar_t *tpaExtensions[] = {
        L"*.dll",
    };

    for (int i = 0; i < _countof(tpaExtensions); i++)
    {
        wchar_t searchPath[MAX_PATH];
        wcscpy_s(searchPath, MAX_PATH, coreRoot);
        wcscat_s(searchPath, MAX_PATH, L"\\");
        wcscat_s(searchPath, MAX_PATH, tpaExtensions[i]);

        WIN32_FIND_DATAW findData;
        HANDLE fileHandle = FindFirstFileW(searchPath, &findData);
        if (fileHandle != INVALID_HANDLE_VALUE)
        {
            do
            {
                wchar_t pathToAdd[MAX_PATH];
                wcscpy_s(pathToAdd, MAX_PATH, coreRoot);
                wcscat_s(pathToAdd, MAX_PATH, L"\\");
                wcscat_s(pathToAdd, MAX_PATH, findData.cFileName);
                if (wcsnlen(pathToAdd, MAX_PATH) + (3) + wcsnlen(trustedPlatformAssemblies, tpaSize) >= tpaSize)
                {
                    // Expand, if needed
                    tpaSize *= 2;
                    wchar_t* newTPAList = new wchar_t[tpaSize];
                    wcscpy_s(newTPAList, tpaSize, trustedPlatformAssemblies);
                    trustedPlatformAssemblies = newTPAList;
                }
                wcscat_s(trustedPlatformAssemblies, tpaSize, pathToAdd);
                wcscat_s(trustedPlatformAssemblies, tpaSize, L";");
            } while (FindNextFileW(fileHandle, &findData));
            FindClose(fileHandle);
        }
    }

    for (int i = 0; i < _countof(tpaExtensions); i++)
    {
        wchar_t searchPath[MAX_PATH];
        wcscpy_s(searchPath, MAX_PATH, targetAppPath);
        wcscat_s(searchPath, MAX_PATH, L"\\");
        wcscat_s(searchPath, MAX_PATH, tpaExtensions[i]);

        WIN32_FIND_DATAW findData;
        HANDLE fileHandle = FindFirstFileW(searchPath, &findData);
        if (fileHandle != INVALID_HANDLE_VALUE)
        {
            do
            {
                wchar_t pathToAdd[MAX_PATH];
                wcscpy_s(pathToAdd, MAX_PATH, targetAppPath);
                wcscat_s(pathToAdd, MAX_PATH, L"\\");
                wcscat_s(pathToAdd, MAX_PATH, findData.cFileName);
                if (wcsnlen(pathToAdd, MAX_PATH) + (3) + wcsnlen(trustedPlatformAssemblies, tpaSize) >= tpaSize)
                {
                    // Expand, if needed
                    tpaSize *= 2;
                    wchar_t* newTPAList = new wchar_t[tpaSize];
                    wcscpy_s(newTPAList, tpaSize, trustedPlatformAssemblies);
                    trustedPlatformAssemblies = newTPAList;
                }
                wcscat_s(trustedPlatformAssemblies, tpaSize, pathToAdd);
                wcscat_s(trustedPlatformAssemblies, tpaSize, L";");
            } while (FindNextFileW(fileHandle, &findData));
            FindClose(fileHandle);
        }
    }

    wchar_t appPaths[MAX_PATH * 50];
    wcscpy_s(appPaths, targetAppPath);

    wchar_t appNiPaths[MAX_PATH * 50];
    wcscpy_s(appNiPaths, targetAppPath);
    wcscat_s(appNiPaths, MAX_PATH * 50, L";");
    wcscat_s(appNiPaths, MAX_PATH * 50, targetAppPath);
    wcscat_s(appNiPaths, MAX_PATH * 50, L"NI");

    wchar_t nativeDllSearchDirectories[MAX_PATH * 50];
    wcscpy_s(nativeDllSearchDirectories, appPaths);
    wcscat_s(nativeDllSearchDirectories, MAX_PATH * 50, L";");
    wcscat_s(nativeDllSearchDirectories, MAX_PATH * 50, coreRoot);

    wchar_t platformResourceRoots[MAX_PATH * 50];
    wcscpy_s(platformResourceRoots, appPaths);
    DWORD domainId;
    const wchar_t* propertyKeys[] = {
        L"TRUSTED_PLATFORM_ASSEMBLIES",
        L"APP_PATHS",
        L"APP_NI_PATHS",
        L"NATIVE_DLL_SEARCH_DIRECTORIES",
        L"PLATFORM_RESOURCE_ROOTS"
    };

    const wchar_t* propertyValues[] = {
        trustedPlatformAssemblies,
        appPaths,
        appNiPaths,
        nativeDllSearchDirectories,
        platformResourceRoots
    };

    hr = runtimeHost->CreateAppDomainWithManager(
        L"Sample Host AppDomain",		// Friendly AD name
        appDomainFlags,
        NULL,							// Optional AppDomain manager assembly name
        NULL,							// Optional AppDomain manager type (including namespace)
        sizeof(propertyKeys) / sizeof(wchar_t*),
        propertyKeys,
        propertyValues,
        &domainId);

    if (FAILED(hr))
    {
        printf("ERROR - Failed to create AppDomain.\nError code:%x\n", hr);
        return -1;
    }
    else
    {
        printf("AppDomain %d created\n\n", domainId);
    }

    wprintf(L"Executing %s...\n\n", targetApp);

    void *pfnDelegate = NULL;
    hr = runtimeHost->CreateDelegate(
        domainId,
        L"CSharPyExtension",	        // Target managed assembly name (https://docs.microsoft.com/dotnet/framework/app-domains/assembly-names)
        L"CSharPyExtension.CsBridge",	// Target managed type
        L"SquareNumber",			    // Target entry point (static method)
        (INT_PTR*)&pfnDelegate);
    if (FAILED(hr))
    {
        printf("ERROR - Failed to create delegate.\nError code:%x\n", hr);
        return -1;
    }
    typedef double (STDMETHODCALLTYPE * TypeSquareNumber)(double);
    TypeSquareNumber fct = (TypeSquareNumber)pfnDelegate;
    printf("Results %f\n", fct(9));

    runtimeHost->UnloadAppDomain(domainId, true /* Wait until unload complete */);
    runtimeHost->Stop();
    runtimeHost->Release();
    printf("\nDone\n");
    return 0;
}


// Helper methods

// Check for CoreCLR.dll in a given path and load it, if possible
HMODULE LoadCoreCLR(const wchar_t* directoryPath)
{
    wchar_t coreDllPath[MAX_PATH];
    wcscpy_s(coreDllPath, MAX_PATH, directoryPath);
    wcscat_s(coreDllPath, MAX_PATH, L"\\");
    wcscat_s(coreDllPath, MAX_PATH, coreCLRDll);

    // <Snippet2>
    HMODULE ret = LoadLibraryExW(coreDllPath, NULL, 0);
    // </Snippet2>

    if (!ret)
    {
        // This logging is likely too verbose for many scenarios, but is useful
        // when getting started with the hosting APIs.
        DWORD errorCode = GetLastError();
        wprintf(L"CoreCLR not loaded from %s. LoadLibrary error code: %d\n", coreDllPath, errorCode);
    }

    return ret;
}

/////////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////


// Copyright (c) Microsoft Corporation. All rights reserved.
// Licensed under the MIT license.

#include <string>
#include <cstdlib>
//#include "inc/mscoree.h"

std::wstring Utf8ToUtf16le(const char* utf8Str)
{
    // Allocate the utf16 string buffer.
    unsigned int iSizeOfStr = MultiByteToWideChar(CP_UTF8, 0, utf8Str, -1, NULL, 0);
    wchar_t* utf16Str = new wchar_t[iSizeOfStr];
    std::wstring result;

    try
    {
        // Convert the utf8 string.
        MultiByteToWideChar(CP_UTF8, 0, utf8Str, -1, utf16Str, iSizeOfStr);

        // Copy it to a std::wstring to simplify heap management.
        result = utf16Str;

        // Free the utf16 string buffer.
        delete[] utf16Str;
        utf16Str = NULL;
    }
    catch (...)
    {
        // On exception clean up and re-throw.
        if (utf16Str) delete[] utf16Str;
        throw;
    }

    return result;
}

void ConvertToWinPath(std::wstring & dir)
{
    for (int ich = 0; ich < dir.size(); ich++)
    {
        if (dir[ich] == '/')
            dir[ich] = '\\';
    }
    if (dir[dir.size() - 1] != '\\')
        dir.append(W("\\"));
}

class WinNetInterface
{
private:
    std::string _coreclrpath;
public:
    WinNetInterface(const char *coreclrpath) : _coreclrpath(coreclrpath), _host(nullptr), _hmodCore(nullptr)
    {
    }

private:
    // The coreclr.dll module.
    HMODULE _hmodCore;
    // The runtime host and app domain.
    ICLRRuntimeHost2 *_host;
    DWORD _domainId;

private:
    void Shutdown()
    {
        if (_host)
        {
            // Unload the app domain, waiting until done.
            HRESULT hr = _host->UnloadAppDomain(_domainId, true);
            if (FAILED(hr))
            {
                // REVIEW: Handle failure.
                //log << W("Failed to unload the AppDomain. ERRORCODE: ") << hr << Logger::endl;
                //return false;
            }

            hr = _host->Stop();
            if (FAILED(hr)) {
                // REVIEW: Handle failure.
                //log << W("Failed to stop the host. ERRORCODE: ") << hr << Logger::endl;
                //return false;
            }

            // Release the reference to the host.
            _host->Release();
            _host = nullptr;
        }

        if (_hmodCore)
        {
            // Free the module. This is done for completeness, but in fact CoreCLR.dll
            // was pinned earlier so this call won't actually free it. The pinning is
            // done because CoreCLR does not support unloading.
            ::FreeLibrary(_hmodCore);

            _hmodCore = nullptr;
        }
    }

    HMODULE EnsureCoreClrModule(const wchar_t *path)
    {
        if (_hmodCore == nullptr)
        {
            std::wstring pathCore(path);
            //std::wstring env(path);
            //env.append(L";").append(_wgetenv(L"PATH"));
            //_wputenv(env.c_str());

            pathCore.append(W("CoreCLR.dll"));

            // Load CoreCLR from the indicated directory.
            SetDllDirectoryW(path);
            HMODULE hmodCore = ::LoadLibraryExW(pathCore.c_str(), NULL,
                LOAD_LIBRARY_SEARCH_DLL_LOAD_DIR
                // | LOAD_LIBRARY_SEARCH_SYSTEM32
                | LOAD_LIBRARY_SEARCH_DEFAULT_DIRS
            );
            SetDllDirectoryW(nullptr);
            if (!hmodCore)
            {
                // REVIEW: Log failure somehow.
                return nullptr;
            }

            // Pin the module - CoreCLR.dll does not support being unloaded.
            HMODULE hmodTmp;
            if (!::GetModuleHandleExW(GET_MODULE_HANDLE_EX_FLAG_PIN, pathCore.c_str(), &hmodTmp))
            {
                // REVIEW: Log failure somehow.
                // *m_log << W("Failed to pin: ") << pathCore << Logger::endl;
                return nullptr;
            }

            _hmodCore = hmodCore;
        }
        return _hmodCore;
    }

    // Appends all .dlls in the given directory to list, semi-colon terminated.
    void AddDllsToList(const wchar_t *path, std::wstring & list)
    {
        std::wstring wildPath(path);
        wildPath.append(W("*.dll"));

#ifdef _MSC_VER
        WIN32_FIND_DATAW data;
        HANDLE findHandle = FindFirstFileW(wildPath.c_str(), &data);
#else
        WIN32_FIND_DATA data;
        HANDLE findHandle = FindFirstFile(wildPath.c_str(), &data);
#endif
        if (findHandle == INVALID_HANDLE_VALUE)
        {
            // REVIEW: Report failure somehow.
            return;
        }

        do
        {
            if ((data.dwFileAttributes & FILE_ATTRIBUTE_DIRECTORY) == 0)
                list.append(path).append(data.cFileName).append(W(";"));
        } while (0 !=
#ifdef _MSC_VER
            FindNextFileW(findHandle, &data)
#else        
            FindNextFile(findHandle, &data)
#endif
            );
        FindClose(findHandle);
    }

    ICLRRuntimeHost2* EnsureClrHost(const wchar_t * libsRoot, const wchar_t * coreclrDirRoot, const LPCWSTR dll_cs_name)
    {
        if (_host != nullptr)
            return _host;

        // Set up paths.
        std::wstring tpaList;
        AddDllsToList(libsRoot, tpaList);
        AddDllsToList(coreclrDirRoot, tpaList);

        // Start the CoreCLR.
        HMODULE hmodCore = EnsureCoreClrModule(coreclrDirRoot);

        FnGetCLRRuntimeHost pfnGetCLRRuntimeHost =
            (FnGetCLRRuntimeHost)::GetProcAddress(hmodCore, "GetCLRRuntimeHost");
        if (!pfnGetCLRRuntimeHost)
            return nullptr;

        ICLRRuntimeHost2 *host;
        HRESULT hr = pfnGetCLRRuntimeHost(IID_ICLRRuntimeHost2, (IUnknown**)&host);
        if (FAILED(hr))
            return nullptr;

        // Default startup flags.
        hr = host->SetStartupFlags((STARTUP_FLAGS)
            (STARTUP_FLAGS::STARTUP_LOADER_OPTIMIZATION_SINGLE_DOMAIN |
                STARTUP_FLAGS::STARTUP_SINGLE_APPDOMAIN));
        if (FAILED(hr))
        {
            // log << W("Failed to set startup flags. ERRORCODE: ") << hr << Logger::endl;
            host->Release();
            return nullptr;
        }

        hr = host->Start();
        if (FAILED(hr))
        {
            // log << W("Failed to start CoreCLR. ERRORCODE: ") << hr << Logger::endl;
            host->Release();
            return nullptr;
        }

        DWORD appDomainFlags = APPDOMAIN_ENABLE_PLATFORM_SPECIFIC_APPS |
            APPDOMAIN_ENABLE_PINVOKE_AND_CLASSIC_COMINTEROP |
            APPDOMAIN_DISABLE_TRANSPARENCY_ENFORCEMENT;

        // Create an AppDomain.

        // Allowed property names:
        // APPBASE
        // - The base path of the application from which the exe and other assemblies will be loaded
        //
        // TRUSTED_PLATFORM_ASSEMBLIES
        // - The list of complete paths to each of the fully trusted assemblies
        //
        // APP_PATHS
        // - The list of paths which will be probed by the assembly loader
        //
        const wchar_t *property_keys[] = {
            W("TRUSTED_PLATFORM_ASSEMBLIES"),
            W("APP_PATHS"),
            W("AppDomainCompatSwitch"),
        };
        const wchar_t *property_values[] = {
            // TRUSTED_PLATFORM_ASSEMBLIES
            tpaList.c_str(),
            // APP_PATHS
            libsRoot,
            // AppDomainCompatSwitch
            W("UseLatestBehaviorWhenTFMNotSpecified")
        };

        hr = host->CreateAppDomainWithManager(
            dll_cs_name,  // The friendly name of the AppDomain
            // Flags:
            // APPDOMAIN_ENABLE_PLATFORM_SPECIFIC_APPS
            // - By default CoreCLR only allows platform neutral assembly to be run. To allow
            //   assemblies marked as platform specific, include this flag
            //
            // APPDOMAIN_ENABLE_PINVOKE_AND_CLASSIC_COMINTEROP
            // - Allows sandboxed applications to make P/Invoke calls and use COM interop
            //
            // APPDOMAIN_SECURITY_SANDBOXED
            // - Enables sandboxing. If not set, the app is considered full trust
            //
            // APPDOMAIN_IGNORE_UNHANDLED_EXCEPTION
            // - Prevents the application from being torn down if a managed exception is unhandled
            appDomainFlags,
            NULL, // Name of the assembly that contains the AppDomainManager implementation.
            NULL, // The AppDomainManager implementation type name.
            sizeof(property_keys) / sizeof(wchar_t*), // The number of properties.
            property_keys,
            property_values,
            &_domainId);
        if (FAILED(hr))
        {
            // log << W("Failed call to CreateAppDomainWithManager. ERRORCODE: ") << hr << Logger::endl;
            host->Release();
            return nullptr;
        }

        _host = host;
        return _host;
    }

public:
    void* CreateDeledate(const char *dll_lib_path,
        const LPCWSTR dll_cs_name,
        const LPCWSTR class_name,
        const LPCWSTR function_name)
    {
        std::wstring libsdir = Utf8ToUtf16le(dll_lib_path);
        ConvertToWinPath(libsdir);

        std::wstring coreclrdir;
        if (strlen(_coreclrpath.c_str()) != 0)
        {
            coreclrdir = Utf8ToUtf16le(_coreclrpath.c_str());
            ConvertToWinPath(coreclrdir);
        }
        else
        {
            coreclrdir = libsdir;
        }

        ICLRRuntimeHost2* host = EnsureClrHost(libsdir.c_str(), coreclrdir.c_str(), dll_cs_name);
        if (host == NULL)
            throw std::runtime_error("Host is NULL.");

        // CoreCLR currently requires using environment variables to set most CLR flags.
        // cf. https://github.com/dotnet/coreclr/blob/master/Documentation/project-docs/clr-configuration-knobs.md
        // if (_wputenv(W("COMPlus_gcAllowVeryLargeObjects=1")) == -1)
        //    throw std::runtime_error("Issue with COMPlus_gcAllowVeryLargeObjects.");

        void* getter = NULL;
        HRESULT hr = host->CreateDelegate(
            _domainId,
            dll_cs_name,
            class_name,
            function_name,
            (INT_PTR*)&getter);
        if (FAILED(hr))
            throw std::runtime_error("Unable to retrieve a function.");
        if (getter == NULL)
            throw std::runtime_error("Unable to retrieve a function due to NULL pointer.");
        return getter;
    }
};

typedef double(__stdcall * TypeSquareNumber)(double);

int main2()
{
    static const char *coreCLRInstallDirectory = "c:\\Python372_x64\\lib\\site-packages\\dotnetcore2\\bin\\shared\\Microsoft.NETCore.App\\2.1.5";
    //static const wchar_t* coreCLRDll = L"coreclr.dll";
    const char * dllname = "C:\\xavierdupre\\__home_\\GitHub\\csharpy\\cscode\\bin\\x64.Debug\\CSharPyExtension\\netstandard2.0";
    WinNetInterface *winnet = new WinNetInterface(coreCLRInstallDirectory);
    void* fct = winnet->CreateDeledate(
        dllname,
        W("CSharPyExtension"),
        W("CSharPyExtension.CsBridge"),
        W("SquareNumber"));
    TypeSquareNumber tfct = (TypeSquareNumber)fct;
    double r = tfct(9.);
    printf("square = %f\n", r);
    return 0;
}

///////////////////////////////////////////////////////////////////////////////////////////////////

int main()
{
    return main2();
}
