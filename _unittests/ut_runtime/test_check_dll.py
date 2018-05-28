"""
@brief      test log(time=2s)
"""
import sys
import os
import unittest
import warnings
from pyquickhelper.pycode import ExtTestCase
import clr

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


class TestCheckDll(ExtTestCase):
    """Test dynamic import."""

    def test_src(self):
        "skip pylint"
        self.assertFalse(src is None)

    def test_add_reference_system_collections(self):
        try:
            clr.AddReference("System.Collections")
        except Exception as e:
            warnings.warn(
                "[csharpy] issue with System.Collections {0}".format(e))


if __name__ == "__main__":
    unittest.main()
