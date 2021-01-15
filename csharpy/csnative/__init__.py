"""
@file
@brielf Shortcut to *csnative*.
"""
import os
import sys
from .dotnet_helper import get_clr_path


this_location = os.path.abspath(os.path.dirname(__file__))


def start():
    """
    Loads :epkg:`dotnetcore`.
    """
    from .csmain import cs_start  # pylint: disable=E0611,E0401
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

    if sys.platform.startswith("win"):
        native_lib = "csmain.cp%d%d-win_amd64.pyd" % sys.version_info[:2]
    elif sys.platform.startswith("darwin"):
        native_lib = "csmain.cpython-%d%dm-x86_64-darwin-gnu.dylib" % sys.version_info[:2]
        native_lib = os.path.join(this_location, native_lib)
    else:
        native_lib = "csmain.cpython-%d%dm-x86_64-linux-gnu.so" % sys.version_info[:2]
        native_lib = os.path.join(this_location, native_lib)

    return cs_start(get_clr_path(), native_lib, loc)


def close():
    """
    Unloads *dotnetcore*.
    """
    from .csmain import cs_end  # pylint: disable=E0611,E0401
    cs_end()
