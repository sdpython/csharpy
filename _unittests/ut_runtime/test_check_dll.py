"""
@brief      test log(time=2s)
"""
import unittest
import warnings
from pyquickhelper.pycode import ExtTestCase


class TestCheckDll(ExtTestCase):
    """Test dynamic import."""

    def test_add_reference_system_collections(self):
        import clr  # pylint: disable=E0401
        try:
            clr.AddReference("System.Collections")
        except Exception as e:
            warnings.warn(
                "[csharpy] issue with System.Collections {0}".format(e))


if __name__ == "__main__":
    unittest.main()
