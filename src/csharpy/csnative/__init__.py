"""
@file
@brielf Shortcut to *csnative*.
"""
import os


def start():
    """
    Loads *dotnetcore*.
    """
    from .csmain import cs_start  # pylint: disable=E0611
    from ..binaries import __file__
    loc = os.path.join(os.path.abspath(os.path.dirname(__file__)), "Release")
    if not os.path.exists(loc):
        loc = os.path.join(os.path.abspath(os.path.dirname(__file__)), "Debug")
    if not os.path.exists(loc):
        raise FileNotFoundError(
            "Unable to find any DLL in folder '{}'.".format(loc))
    csext = os.path.join(loc, "CSharPyExtension.dll")
    if not os.path.exists(csext):
        raise FileNotFoundError("Unable to find DLL '{}'.".format(csext))
    return cs_start(get_clr_path(), loc)


def close():
    """
    Unloads *dotnetcore*.
    """
    from .csmain import cs_end  # pylint: disable=E0611
    cs_end()


def get_clr_path():
    """
    Returns path to .NET CLR libs.
    Use :epkg:`dotnetcore2` package.

    .. runpython::
        :showcode:

        from csharpy.csnative import get_clr_path
        print(get_clr_path())
    """
    from dotnetcore2 import runtime as clr_runtime
    libs_root = os.path.join(clr_runtime._get_bin_folder(), 'shared',  # pylint: disable=W0212
                             'Microsoft.NETCore.App')

    # Search all libs folders to find which one contains the .NET CLR libs
    libs_folders = os.listdir(libs_root)
    if len(libs_folders) == 0:
        raise ImportError("Trouble importing dotnetcore2: "
                          "{} had no libs folders.".format(libs_root))
    clr_path = None
    for folder in libs_folders:
        if os.path.exists(os.path.join(libs_root, folder,
                                       'Microsoft.CSharp.dll')):
            clr_path = os.path.join(libs_root, folder)
            break
    if not clr_path:
        raise ImportError(
            "Trouble importing dotnetcore2: Microsoft.CSharp.dll was not "
            "found in {}.".format(libs_root))
    return clr_path
