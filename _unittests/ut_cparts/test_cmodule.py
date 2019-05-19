"""
@brief      test log(time=1s)

You should indicate a time in seconds. The program ``run_unittests.py``
will sort all test files by increasing time and run them.
"""
import unittest
from pyquickhelper.pycode import ExtTestCase
from csharpy.cparts import version_c


class TestCModule(ExtTestCase):
    """Test dynamic compilation."""

    def test_version_c(self):
        ver = version_c()
        self.assertEqual(ver, "0.2")


if __name__ == "__main__":
    unittest.main()
