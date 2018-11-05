"""
@brief      test log(time=2s)
"""
import sys
import os
import unittest
from contextlib import redirect_stdout, redirect_stderr
from io import StringIO
import numpy
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

from src.csharpy.runtime import create_cs_function
from src.csharpy.notebook.csmagics import CsMagics


class TestDynamicCS(ExtTestCase):
    """Test dynamic compilation."""

    def test_src(self):
        "skip pylint"
        self.assertFalse(src is None)

    def test_pythonnet(self):
        clr.AddReference("System")
        from System import String
        s = String("example")
        x = s.Replace("e", "j")
        self.assertEqual("jxamplj", x)

        from System.Collections.Generic import Dictionary
        d = Dictionary[String, String]()
        d["un"] = "1"
        self.assertEqual(d.Count, 1)

    def test_add_reference_system(self):
        clr.AddReference("System")

    def test_pythonnet_array(self):
        clr.AddReference("System")
        from System import IntPtr, Array, Double, Int64
        self.assertTrue(Double is not None)
        self.assertTrue(Array is not None)
        self.assertTrue(IntPtr is not None)

        array = numpy.ones((2, 2), dtype=int)
        ar = array.__array_interface__['data'][0]
        ar2 = Array[Int64]([0, 0, 0, 0] * 2)
        self.assertEqual(str(type(ar)), "<class 'int'>")
        self.assertEqual(str(type(ar2)), "<class 'System.Int64[]'>")
        self.assertEqual(list(ar2), [0, 0, 0, 0, 0, 0, 0, 0])
        # from System.Runtime.InteropServices import Marshal
        # try:
        #     Marshal.Copy(ar, ar2, 0, len(ar2))
        # except TypeError as e:
        #     warnings.warn(str(e))

    def test_create_cs_function(self):
        code = "public static double SquareX(double x) { return x*x; }"
        f = create_cs_function("SquareX", code)
        r = f(2.0)
        self.assertEqual(r, 4)

    def test_create_cs_function_output(self):
        code = 'public static double SquareX(double x) { Console.WriteLine("check output"); return x*x ; }'
        f = create_cs_function(
            "SquareX", code, redirect=True, usings=["System"])
        r, out, err = f(2.0)
        self.assertEqual(r, 4)
        self.assertEqual(out, "check output\n")
        self.assertEqual(err, "")

    def test_magic_cs(self):
        cm = CsMagics()
        code = "public static double SquareX(double x) {return x*x ; }"
        code = """
                public static int[] cs_qsortl(int[] li)
                {
                    if (li.Length == 0)
                        return null;
                    else
                    {
                        var pivot = li[0];
                        var lesser = cs_qsortl(li.Skip(1).Where(x => x < pivot).ToArray());
                        var greater = cs_qsortl(li.Skip(1).Where(x => x >= pivot).ToArray());
                        var res = new int[li.Length];

                        if (lesser != null && lesser.Length > 0)
                            Array.Copy(lesser, 0, res, 0, lesser.Length);
                        int nb = lesser == null ? 0 : lesser.Length;
                        res[nb] = pivot;
                        if (greater != null && greater.Length > 0)
                            Array.Copy(greater, 0, res, nb + 1, greater.Length);

                        return res;
                    }
                }

                public static int[] cs_qsort(string lis)
                {
                    return cs_qsortl(lis.Split(';').Select(c=>int.Parse(c)).ToArray()) ;
                }
                """
        f = cm.CS("cs_qsort -i System -i System.Linq -d System.Core",
                  code)
        if f is None:
            raise Exception(code)
        li = [2, 4, 5, 3, 1]
        lis = ";".join(str(i) for i in li)
        x = f(lis)
        self.assertNotEqual(x, 4)
        self.assertTrue(x is not None)

        f = cm.CS("cs_qsort -i System.Linq",
                  "-i System -d System.Core\n" + code)
        if f is None:
            raise Exception(code)
        li = [2, 4, 5, 3, 1]
        lis = ";".join(str(i) for i in li)
        x = f(lis)
        self.assertNotEqual(x, 4)
        self.assertTrue(x is not None)

        out = StringIO()
        err = StringIO()
        with redirect_stdout(out):
            with redirect_stderr(err):
                f = cm.CS("cs_qsort -c", code)
                self.assertEmpty(f)
        exp = "usage: CS [-h] [-i [IDEP [IDEP ...]]] [-d [DEP [DEP ...]]] [-c CATCH] name"
        res = out.getvalue().split('\n')[0]
        self.assertEqual(res, exp)
        err = err.getvalue().split('\n')[0]
        self.assertEqual(res, exp)


if __name__ == "__main__":
    unittest.main()
