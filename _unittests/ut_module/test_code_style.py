"""
@brief      test log(time=0s)
"""
import os
import unittest
from pyquickhelper.loghelper import fLOG
from pyquickhelper.pycode import check_pep8, ExtTestCase


class TestCodeStyle(ExtTestCase):
    """Test style."""

    def test_style_src(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")
        thi = os.path.abspath(os.path.dirname(__file__))
        src_ = os.path.normpath(os.path.join(thi, "..", "..", "csharpy"))
        check_pep8(src_, fLOG=fLOG,
                   pylint_ignore=('C0103', 'C1801', 'R0201', 'R1705', 'W0108', 'W0613',
                                  'C011111', 'C0415'),
                   skip=["Unable to import 'CSharPyExtension'",
                         "Unable to import 'System'",
                         "Unable to import 'System.Collections.Generic'",
                         "Unable to import 'DynamicCS'",
                         "csmagics.py:113: W0703",
                         "add_reference.py:14: W0703",
                         "No name 'version_c' in module 'csharpy.cparts.cmodule'",
                         "compile.py:45: W0703",
                         ])

    def test_style_test(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")
        thi = os.path.abspath(os.path.dirname(__file__))
        test = os.path.normpath(os.path.join(thi, "..", ))
        check_pep8(test, fLOG=fLOG, neg_pattern="temp_.*",
                   pylint_ignore=('C0103', 'C1801', 'R0201', 'R1705', 'W0108', 'W0613',
                                  'C0111', 'W0703'),
                   skip=["Unable to import 'CSharPyExtension'",
                         "Unable to import 'System'",
                         "Unable to import 'System.Collections.Generic'",
                         ])


if __name__ == "__main__":
    unittest.main()
