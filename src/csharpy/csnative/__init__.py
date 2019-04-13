"""
@file
@brielf Shortcut to *csnative*.
"""
import os
from .dotnetcore_helper import get_clr_path


def start():
    """
    Loads :epkg:`dotnetcore`.
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
