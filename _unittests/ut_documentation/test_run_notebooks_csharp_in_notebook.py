# -*- coding: utf-8 -*-
"""
@brief      test log(time=8s)
"""
import os
import unittest
from pyquickhelper.loghelper import fLOG
from pyquickhelper.ipythonhelper import test_notebook_execution_coverage
from pyquickhelper.pycode import add_missing_development_version, ExtTestCase
import csharpy


class TestNotebook_csharp_in_notebook(ExtTestCase):

    def setUp(self):
        add_missing_development_version(["pymyinstall", "pyensae", "jyquickhelper"],
                                        __file__, hide=True)

    def test_notebook_csharp_in_notebook(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")

        self.assertTrue(csharpy is not None)
        folder = os.path.join(os.path.dirname(__file__),
                              "..", "..", "_doc", "notebooks")
        test_notebook_execution_coverage(__file__, "csharp_in_notebook", folder,
                                         this_module_name="csharpy", fLOG=fLOG)


if __name__ == "__main__":
    unittest.main()
