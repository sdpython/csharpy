"""
@brief      test log(time=2s)
"""
import unittest
from dotnetcore2 import runtime as clr_runtime
from pyquickhelper.pycode import ExtTestCase
from csharpy.csnative import start, get_clr_path


class TestCsNative(ExtTestCase):

    def setUp(self):
        start()

    def test_get_clr_path(self):
        path = get_clr_path()
        self.assertExists(path)
        self.assertIn(clr_runtime._get_bin_folder(),  # pylint: disable=W0212
                      path)

    def test_csnative_start(self):
        v = start()
        self.assertNotEmpty(v)
        from csharpy.csnative.csmain import _core_clr_path  # pylint: disable=E0611
        from csharpy.csnative.csmain import _core_clr_path_default  # pylint: disable=E0611
        p = _core_clr_path()
        self.assertNotEmpty(p)
        p2 = _core_clr_path_default()
        self.assertEqual(p2, get_clr_path())

    def test_cs_square_number(self):
        from csharpy.csnative.csmain import SquareNumber  # pylint: disable=E0611
        y = SquareNumber(9.)
        self.assertEqual(y, 81)
        y = SquareNumber(4.)
        self.assertEqual(y, 16)


if __name__ == "__main__":
    unittest.main()