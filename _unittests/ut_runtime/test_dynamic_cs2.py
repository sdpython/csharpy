"""
@brief      test log(time=6s)
"""
import unittest
from contextlib import redirect_stdout, redirect_stderr
from io import StringIO
from dotnetcore2 import runtime as clr_runtime
from pyquickhelper.pycode import ExtTestCase
from csharpy.csnative import start, get_clr_path
from csharpy.runtime import create_cs_function
from csharpy.notebook.csmagics import CsMagics


class TestDynamicCS2(ExtTestCase):
    """Test dynamic compilation.
    System.Security.Permissions
    System.Private.CoreLib
    """

    def setUp(self):
        start()

    def test_create_cs_function(self):
        code = "public static double SquareX(double x) { return x*x; }"
        f = create_cs_function("SquareX", code, use_clr=False)
        r = f(2.0)
        self.assertEqual(r, 4)


if __name__ == "__main__":
    unittest.main()
