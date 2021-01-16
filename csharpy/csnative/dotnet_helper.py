"""
@file
@brielf Helper for :epkg:`dotnetcore2`.
"""
import os


def get_clr_path():
    """
    Returns path to .NET CLR libs.

    .. runpython::
        :showcode:

        from csharpy.csnative import get_clr_path
        print(get_clr_path())
    """
    # Search all libs folders to find which one contains the .NET CLR libs
    clr_paths = [
        r"C:\Program Files\dotnet\shared\Microsoft.NETCore.App\5.0.2",
        r"C:\Program Files\dotnet\shared\Microsoft.NETCore.App\3.1.11",
        r"C:\Program Files\dotnet\shared\Microsoft.NETCore.App\3.1.3"]
    clr_paths_ = [_ for _ in clr_paths if os.path.exists(_)]
    if len(clr_paths_) > 0 and os.path.exists(clr_paths_[0]):
        return clr_paths_[0]
    import clr  # pylint: disable=W0611,E0401
    from System import __file__ as dotnetfile
    libs_root = os.path.dirname(dotnetfile)
    if "GAC_MSIL" in libs_root:
        spl = libs_root.split("GAC_MSIL")
        part1 = os.path.join(spl[0], "GAC_MSIL")
        # part2 = os.path.split(spl[1].strip("\\/"))[-1]
        libs_root = part1
    else:
        # part2 = ""
        pass
    libs_folders = os.listdir(libs_root)
    if len(libs_folders) == 0:
        raise ImportError("Trouble: "
                          "'{}' had no libs folders.".format(libs_root))
    clr_path = libs_root
    return clr_path
