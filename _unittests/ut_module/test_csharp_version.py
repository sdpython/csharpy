"""
@brief      test log(time=1s)

You should indicate a time in seconds. The program ``run_unittests.py``
will sort all test files by increasing time and run them.
"""
import sys
import os
import unittest
import clr
from pyquickhelper.pycode import ExtTestCase

try:
    import src
except ImportError:
    path = os.path.normpath(
        os.path.abspath(
            os.path.join(
                os.path.split(__file__)[0],
                "..",
                "..")))
    if path not in sys.path:
        sys.path.append(path)
    import src

from src.csharpy.binaries import add_csharp_extension
from src.csharpy import __version__


class TestCSharpVersion(ExtTestCase):
    """Test csharp version is aligned with module version."""

    def test_version_number(self):
        add_csharp_extension()
        from CSharPyExtension import Constants
        vers = Constants.Version()
        self.assertEqual(__version__, vers)


if __name__ == "__main__":
    unittest.main()
