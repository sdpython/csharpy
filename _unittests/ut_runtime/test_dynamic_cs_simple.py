"""
@brief      test log(time=4s)
"""
import unittest
from pyquickhelper.pycode import ExtTestCase
from csharpy.csnative import start, get_clr_path
from csharpy.runtime import create_cs_function


class TestDynamicCSSimple(ExtTestCase):
    """Test dynamic compilation.
    System.Security.Permissions
    System.Private.CoreLib
    """

    def _setUp(self):
        start()

    def test_get_clr_path(self):
        path = get_clr_path()
        self.assertExists(path)

    @unittest.skipIf(True, reason="use_clr=True too complex to maintain")
    def test_create_cs_function(self):
        code = "public static double SquareX(double x) { return x*x; }"
        f = create_cs_function("SquareX", code, use_clr=False)
        r = f(2.0)
        self.assertEqual(r, 4)

    def test_create_cs_function_clr(self):
        code = "public static double SquareX(double x) { return x*x; }"
        f = create_cs_function("SquareX", code, use_clr=True,
                               verbose=True)
        r = f(2.0)
        self.assertEqual(r, 4)


if __name__ == "__main__":
    unittest.main()
