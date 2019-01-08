
.. blogpost::
    :title: pythonnet is not fully netcore
    :keywords: compilation
    :date: 2019-01-08
    :categories: dotnet, pythonnet

    :epkg:`pythonnet` still has dependencies on .net
    through `UnmanagedExports <https://www.nuget.org/packages/UnmanagedExports/>`_
    which is compiled against .Net.
    A fork `DllExport <https://www.nuget.org/packages/DllExport/>`_
    may remove that dependency according to this issue
    `Request for updates on support for DllExport on CoreCLR <https://github.com/3F/DllExport/issues/90>`_
    but that might or might not happen soon.
    Which means that :epkg:`mono` cannot be completely removed
    from :epkg:`pythonnet` on :epkg:`linux`.
    