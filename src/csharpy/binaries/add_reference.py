"""
@file
@brief
"""


def AddReference(name):
    """
    Imports a :epkg:`C#` dll.
    """
    from clr import AddReference as ClrAddReference  # pylint: disable=E0401
    try:
        return ClrAddReference(name)
    except Exception as e:
        if "Unable to find assembly" in str(e):
            import sys
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


def add_csharp_extension():
    """
    Imports *CSharpExtension* into global context.

    This binary has a version. On :epkg:`Windows`,
    the system might decide to skip the replacement
    of an assembly because it is in use. You can
    check the version of this by using the following code.

    .. exref::
        :title: Imports the C# extension into :epkg:`Python`

        .. runpython::
            :showcode:

            from csharpy.binaries import add_csharp_extension
            from csharpy import __version__

            add_csharp_extension()

            # This line needs to be after the previous one.
            from CSharPyExtension import Constants

            vers = Constants.Version()
            print(__version__, vers)
    """
    AddReference("CSharPyExtension")
