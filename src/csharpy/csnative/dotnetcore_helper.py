"""
@file
@brielf Helper for :epkg:`dotnetcore2`.
"""
import os


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
