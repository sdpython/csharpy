
@echo off
@echo SCRIPT: windows_prefix
if "%1"=="" goto default_value_python:
if "%1"=="default" goto default_value_python:
set pythonexe=%1
goto start_script:

:default_value_python:
set pythonexe=c:\Python387_x64\python.exe
if not exist %pythonexe% set pythonexe="c:\Python372_x64\python.exe"

@echo ~SET pythonexe=%pythonexe%

:start_script:
set current=%~dp0
if EXIST %current%setup.py goto current_is_setup:
set current=%current%..\
cd ..
if EXIST %current%setup.py goto current_is_setup:
@echo Unable to find %current%setup.py
exit /b 1

:current_is_setup:
@echo ~SET current=%current%

set PYTHONPATH=%PYTHONPATH%;%current%\..\pyquickhelper\src;%current%\..\jyquickhelper\src
%pythonexe% -u %current%setup.py build_ext --inplace
if %errorlevel% neq 0 exit /b %errorlevel%