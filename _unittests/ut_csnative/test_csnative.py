"""
@brief      test log(time=2s)
"""
import unittest
from pyquickhelper.pycode import ExtTestCase
from csharpy.csnative import start, close, get_clr_path


class TestCsNative(ExtTestCase):
    
    def setUp(self):
        start()

    def test_csnative_start(self):
        v = start()
        self.assertNotEmpty(v)
        from csharpy.csnative.csmain import _core_clr_path
        p = _core_clr_path()
        self.assertNotEmpty(p)
        
    def test_cs_square_number(self):
        from csharpy.csnative.csmain import SquareNumber
        y = SquareNumber(9.)
        self.assertEqual(y, 3)
        y = SquareNumber(4.)
        self.assertEqual(y, 2)

if __name__ == "__main__":
    unittest.main()
