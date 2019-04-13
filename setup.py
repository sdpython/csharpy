# -*- coding: utf-8 -*-
import sys
import os
import shutil
import warnings
from setuptools import setup, Extension
from setuptools import find_packages

#########
# settings
#########

project_var_name = "csharpy"
project_owner = "sdpython"
versionPython = "%s.%s" % (sys.version_info.major, sys.version_info.minor)
path = "Lib/site-packages/" + project_var_name
readme = 'README.rst'
history = 'HISTORY.rst'


KEYWORDS = project_var_name + ', first name, last name'
DESCRIPTION = "Tools to use C# + Python mostly from Python."


CLASSIFIERS = [
    'Programming Language :: Python :: %d' % sys.version_info[0],
    'Intended Audience :: Developers',
    'Topic :: Scientific/Engineering',
    'Topic :: Education',
    'License :: OSI Approved :: MIT License',
    'Development Status :: 5 - Production/Stable'
]


#######
# data
#######


packages = find_packages('src', exclude='src')
package_dir = {k: "src/" + k.replace(".", "/") for k in packages}
package_data = {project_var_name + ".binaries": ["*.dll", "*.so"],
                project_var_name + ".binaries.Debug": ["*.dll", "*.so"],
                project_var_name + ".binaries.Release": ["*.dll", "*.so"]}

############
# functions
############


def is_local():
    file = os.path.abspath(__file__).replace("\\", "/").lower()
    if "/temp/" in file and "pip-" in file:
        return False
    from pyquickhelper.pycode.setup_helper import available_commands_list
    return available_commands_list(sys.argv)


def ask_help():
    return "--help" in sys.argv or "--help-commands" in sys.argv


def verbose():
    print("---------------------------------")
    print("package_dir =", package_dir)
    print("packages    =", packages)
    print("package_data=", package_data)
    print("current     =", os.path.abspath(os.getcwd()))
    print("---------------------------------")

##########
# version
##########


if is_local() and not ask_help():
    def write_version():
        from pyquickhelper.pycode import write_version_for_setup
        return write_version_for_setup(__file__)

    write_version()

    versiontxt = os.path.join(os.path.dirname(__file__), "version.txt")
    if os.path.exists(versiontxt):
        with open(versiontxt, "r") as f:
            lines = f.readlines()
        subversion = "." + lines[0].strip("\r\n ")
        if subversion == ".0":
            raise Exception("Git version is wrong: '{0}'.".format(subversion))
    else:
        raise FileNotFoundError(versiontxt)
else:
    # when the module is installed, no commit number is displayed
    subversion = ""

if "upload" in sys.argv and not subversion and not ask_help():
    # avoid uploading with a wrong subversion number
    raise Exception(
        "Git version is empty, cannot upload, is_local()={0}".format(is_local()))


class get_pybind_include(object):
    """
    Helper class to determine the pybind11 include path
    The purpose of this class is to postpone importing pybind11
    until it is actually installed, so that the ``get_include()``
    method can be invoked.
    `Source <https://github.com/pybind/python_example/blob/master/setup.py>`_.
    """

    def __init__(self, user=False):
        self.user = user

    def __str__(self):
        import pybind11
        return pybind11.get_include(self.user)


##############
# common part
##############

if os.path.exists(readme):
    with open(readme, "r", encoding='utf-8-sig') as f:
        long_description = f.read()
else:
    long_description = ""
if os.path.exists(history):
    with open(history, "r", encoding='utf-8-sig') as f:
        long_description += f.read()

if "--verbose" in sys.argv:
    verbose()

if is_local():
    from pyquickhelper import get_fLOG, get_insetup_functions
    logging_function = get_fLOG()
    logging_function(OutputPrint=True)
    must_build, run_build_ext = get_insetup_functions()

    if must_build():
        out = run_build_ext(__file__)
        print(out)

    from pyquickhelper.pycode import process_standard_options_for_setup
    r = process_standard_options_for_setup(
        sys.argv, __file__, project_var_name,
        extra_ext=["cs"],
        add_htmlhelp=sys.platform.startswith("win"),
        coverage_options=dict(omit=["*exclude*.py"]),
        github_owner=project_owner,
        fLOG=logging_function, covtoken=(
            "80f56646-c804-4fb7-8476-2211bb9108d1", "'_UT_37_std' in outfile"),
        requirements=["pyquickhelper", "jyquickhelper"],
        additional_notebook_path=["pyquickhelper", "jyquickhelper"],
        additional_local_path=["pyquickhelper", "jyquickhelper"],
        copy_add_ext=["dll", 'so'], layout=["pdf", "html"])
    if not r and not ({"bdist_msi", "sdist",
                       "bdist_wheel", "publish", "publish_doc", "register",
                       "upload_docs", "bdist_wininst", "build_ext"} & set(sys.argv)):
        raise Exception("unable to interpret command line: " + str(sys.argv))
else:
    r = False

if not r:
    if len(sys.argv) in (1, 2) and sys.argv[-1] in ("--help-commands",):
        from pyquickhelper.pycode import process_standard_options_for_setup_help
        process_standard_options_for_setup_help(sys.argv)
    from pyquickhelper.pycode import clean_readme
    from csharpy import __version__ as sversion
    long_description = clean_readme(long_description)
    root = os.path.abspath(os.path.dirname(__file__))

    # version
    version = None
    if "debug" in sys.argv:
        version = "Debug"
    elif "Debug" in sys.argv:
        version = "Debug"
    elif "release" in sys.argv:
        version = "Release"
    elif "Release" in sys.argv:
        version = "Release"
    sys.argv = [_ for _ in sys.argv if _ not in (
        "debug", "Debug", "release", "Release")]
    version2 = version if version else "Release"

    if "build_ext" in sys.argv:
        # We build a dotnet application.
        if '--inplace' not in sys.argv:
            raise Exception("Option --inplace must be set up.")
        from pyquickhelper.loghelper import run_cmd
        env = os.environ.get('DOTNET_CLI_TELEMETRY_OPTOUT', None)
        if env is None:
            os.environ['DOTNET_CLI_TELEMETRY_OPTOUT'] = '1'
        print('[csharpy.env] DOTNET_CLI_TELEMETRY_OPTOUT={0}'.format(
            os.environ['DOTNET_CLI_TELEMETRY_OPTOUT']))
        cmds = ['dotnet restore CSharPyExtension_netcore.sln',
                #'dotnet restore CSharPyExtension_netframework.sln',
                'dotnet build -c %s CSharPyExtension_netcore.sln' % version2,
                'dotnet test -c %s TestCSharpyCore -v n' % version2]

        folder = os.path.abspath("cscode")
        outs = []
        for cmd in cmds:
            out, err = run_cmd(cmd, fLOG=print, wait=True, change_path=folder)
            if len(err) > 0:
                raise RuntimeError(
                    "Unable to compile C# code.\nCMD: {0}\n--ERR--\n{1}\n--OUT--\n{2}".format(
                        cmd, err, out))
            elif len(out) > 0:
                outs.append(out)
                print('[csharpy.dotnet] OUT')
                print(out)

        # Copy files.
        from pyquickhelper.filehelper import explore_folder_iterfile
        dest = os.path.join('src', 'csharpy', 'binaries', version2)
        if not os.path.exists(dest):
            os.makedirs(dest)
        init = os.path.join(dest, "__init__.py")
        if not os.path.exists(init):
            with open(init, 'w') as f:
                pass
        must_copy = {'DynamicCS': 0, 'CSharPyExtension': 0}
        copied = 0
        for name in explore_folder_iterfile(folder, pattern='.*[.]((dll)|(so))$'):
            full = os.path.join(folder, name)
            if version2 in full:
                short_name = os.path.split(os.path.splitext(name)[0])[-1]
                if short_name in must_copy:
                    must_copy[short_name] += 1
                copied += 1
                print("[csharpy.copy] '{0}'".format(name))
                shutil.copy(name, dest)
            else:
                # print("[csharpy.skip] '{0}'".format(name))
                pass
        min_must_copy = min(must_copy.values())
        if copied == 0 or min_must_copy == 0:
            raise RuntimeError(
                "Missing binaries in '{0}' for version='{1}'".format(folder, version2))

        # additional copies (dependencies)
        cscode = os.path.join(root, "cscode")
        deps = os.path.join(cscode, "csdependencies.txt")
        with open(deps, "r") as f:
            lines = [_.strip("\n\r ") for _ in f.readlines()]
        lines = [_ for _ in lines if _]
        for name in lines:
            shutil.copy(name, dest)

    libraries_native = None
    if sys.platform.startswith("win"):
        libraries_native = ['kernel32']
        extra_compile_args = None
        extra_compile_args_native = ['/EHsc', '-std=c++11', '-DNOMINMAX']
    elif sys.platform.startswith("darwin"):
        extra_compile_args = ['-std=c++11', '-lstdc++fs']
        extra_compile_args_native = [
            '-stdlib=libc++', '-mmacosx-version-min=10.7', '-DNOMINMAX']
    else:
        extra_compile_args = ['-lpthread', '-std=c++11']
        extra_compile_args_native = ['-std=c++11', '-DNOMINMAX', '-lstdc++fs']

    # C and C++ parts

    ext_cparts = Extension('csharpy.cparts.cmodule',
                           [os.path.join(root, 'src/csharpy/cparts/version.cpp'),
                               os.path.join(root, 'src/csharpy/cparts/cmodule.cpp')],
                           extra_compile_args=extra_compile_args,
                           include_dirs=[os.path.join(root, 'src/csharpy/cparts')])

    ext_native = Extension('csharpy.csnative.csmain',
                           [os.path.join(root, 'src/csharpy/csnative/csmain.cpp'),
                            os.path.join(root, 'src/csharpy/csnative/stdafx.cpp')],
                           extra_compile_args=extra_compile_args_native,
                           include_dirs=[
                               # Path to pybind11 headers
                               get_pybind_include(),
                               get_pybind_include(user=True),
                               os.path.join(
                                   root, 'src/csharpy/csnative')
                           ],
                           language='c++', libraries=libraries_native)

    # Regular setup.
    setup(
        name=project_var_name,
        ext_modules=[ext_cparts, ext_native],
        version='%s%s' % (sversion, subversion),
        author='Xavier Dupré',
        author_email='xavier.dupre@gmail.com',
        license="MIT",
        url="http://www.xavierdupre.fr/app/csharpy/",
        download_url="https://github.com/sdpython/csharpy/",
        description=DESCRIPTION,
        long_description=long_description,
        keywords=KEYWORDS,
        classifiers=CLASSIFIERS,
        packages=packages,
        package_dir=package_dir,
        package_data=package_data,
        setup_requires=["pyquickhelper"],
        install_requires=['dotnetcore2', 'pythonnet'],
        extras_require={
            'notebook': ['pyquickhelper'],
            'sphinxext': ['pyquickhelper'],
        },
    )
