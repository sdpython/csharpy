"""
@file
@brief
"""
import sys
import warnings


def AddReference(name, use_clr):
    """
    Imports a :epkg:`C#` dll.

    @param      name        assembly name
    @param      use_clr     use :epkg:`pythonnet` or not
                            (native bridge)

    This function only works if :epkg:`pythonnet` is installed
    but the package is not mandatory to call C# functions
    from python.
    """
    try:
        import clr
    except ImportError:
        # pythonnet is not installed
        if use_clr:
            raise ImportError("pythonnet is not installed.")
        else:
            warnings.warn("pythonnet is not installed. AddReference does nothing with '{0}'.".format(
                name))
            return

    from clr import AddReference as ClrAddReference  # pylint: disable=E0401
    try:
        return ClrAddReference(name)
    except Exception as _:
        try:
            from ..csnative.dotnetcore_helper import get_clr_path
            clr_path = get_clr_path()
            if clr_path not in sys.path:
                sys.path.append(clr_path)
            return ClrAddReference(name)
        except Exception as e:
            if "Unable to find assembly" in str(e):
                import os
                this = os.path.abspath(os.path.dirname(__file__))
                rel = os.path.join(this, "Release")
                if os.path.exists(os.path.join(rel, '__init__.py')):
                    this = rel
                else:
                    rel = os.path.join(this, "Debug")
                    if not os.path.exists(os.path.join(rel, '__init__.py')):
                        raise FileNotFoundError(
                            "Unable to find folders 'Release' or 'Debug' in '{0}'".format(this))
                    this = rel
                if this and os.path.exists(this):
                    sys.path.append(this)
                    try:
                        res = ClrAddReference(name)
                    except Exception:
                        del sys.path[-1]
                        raise
                    del sys.path[-1]
                    return res
                else:
                    raise
            else:
                raise


def add_csharp_extension(use_clr):
    """
    Imports *CSharpExtension* into global context.

    This binary has a version. On :epkg:`Windows`,
    the system might decide to skip the replacement
    of an assembly because it is in use. You can
    check the version of this by using the following code.

    @param      use_clr     use :epkg:`pythonnet` or not
                            (native bridge)

    .. exref::
        :title: Imports the C# extension into :epkg:`Python`

        .. runpython::
            :showcode:

            from csharpy.binaries import add_csharp_extension
            from csharpy import __version__

            add_csharp_extension(False)

            # This line needs to be after the previous one.
            from CSharPyExtension import Constants

            vers = Constants.Version()
            print(__version__, vers)
    """
    AddReference("CSharPyExtension", use_clr)
