# coding: utf-8
"""
@brief      test log(time=2s)
"""
import unittest
import warnings
from pyquickhelper.pycode import ExtTestCase
from csharpy.csnative import start, get_clr_path


class TestCsNative(ExtTestCase):

    def setUp(self):
        start()

    def test_get_clr_path(self):
        path = get_clr_path()
        self.assertExists(path)

    def test_csnative_start(self):
        v = start()
        self.assertNotEmpty(v)
        from csharpy.csnative.csmain import (  # pylint: disable=E0611,C0415,E0401
            _core_clr_path, _core_clr_path_default)
        p = _core_clr_path()
        self.assertNotEmpty(p)
        p2 = _core_clr_path_default()
        if p2 != get_clr_path():
            warnings.warn("p2=%r != %r" % (p2, get_clr_path()))

    def test_cs_square_number(self):
        from csharpy.csnative.csmain import SquareNumber  # pylint: disable=E0611,C0415,E0401
        y = SquareNumber(9.)
        self.assertEqual(y, 81)
        y = SquareNumber(4.)
        self.assertEqual(y, 16)

    def test_cs_random_string(self):
        from csharpy.csnative.csmain import RandomString  # pylint: disable=E0611,C0415,E0401
        y = RandomString()
        self.assertEqual(y, "Français")

    def test_cs_square_number_exception(self):
        from csharpy.csnative.csmain import SquareNumber  # pylint: disable=E0611,C0415,E0401
        try:
            SquareNumber(9.)  # replace by a negative value
            raise Exception("Not implemented yet")
        except Exception:
            pass

    def test_cs_upper(self):
        from csharpy.csnative.csmain import CsUpper  # pylint: disable=E0611,C0415,E0401
        texts = ['UP', 'Up', 'ùp']
        for text in texts:
            up = CsUpper(text)
            uppy = text.upper()
            if up != uppy:
                raise ValueError(
                    "Mismatch for '{}' -> '{}' != '{}'.".format(text, up, uppy))


if __name__ == "__main__":
    unittest.main()
