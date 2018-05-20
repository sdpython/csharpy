
.. blogpost::
    :title: Playground with C# and Python
    :keywords: reference, blog, post
    :date: 2018-05-16
    :categories: intention

    The project offers the possibility to speed up :epkg:`Python`
    with :epkg:`C#`. That's what :epkg:`pythonnet` already does.
    The objective is also to add custom :epkg:`C#` assemblies
    as part of the build and to import them from ::epkg:`Python`.
    The first step of this project was to prepare a 
    continuous build which works on Windows and Linux.
    It was not that so obvious to install :epgk:`dotnet`,
    :epkg:`Python` and :epkg:`pythonnet` on the same
    build for :epkg:`travis` and :epkg:`circleci`.
    Some links to help:

    * `latest master cannot be installed with pip+git <https://github.com/pythonnet/pythonnet/issues/555>`_
    * `Failed building wheel <https://github.com/pythonnet/pythonnet/issues/562>`_
    * `Prérequis pour .NET Core sur Linux <https://docs.microsoft.com/fr-fr/dotnet/core/linux-prerequisites?tabs=netcore2x>`_
    * `Install .NET Core SDK 2.1.300-preview1 on Linux Ubuntu 14.04 <https://www.microsoft.com/net/download/linux-package-manager/ubuntu14-04/sdk-2.1.300-preview1>`_
    * `Install clang <https://github.com/travis-ci/apt-source-whitelist/issues/372>`_
    * `Mono Download for Debian <https://www.mono-project.com/download/stable/#download-lin-debian>`_
