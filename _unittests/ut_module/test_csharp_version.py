"""
@brief      test log(time=1s)
"""
import unittest
from pyquickhelper.pycode import ExtTestCase
from csharpy.binaries import add_csharp_extension
from csharpy import __version__


class TestCSharpVersion(ExtTestCase):
    """Test csharp version is aligned with module version."""

    def test_version_number(self):
        import clr  # pylint: disable=E0401
        add_csharp_extension()
        from CSharPyExtension import Constants
        vers = Constants.Version()
        self.assertEqual(__version__, vers)


if __name__ == "__main__":
    unittest.main()
