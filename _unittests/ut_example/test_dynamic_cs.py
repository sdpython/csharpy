"""
@brief      test log(time=1s)

You should indicate a time in seconds. The program ``run_unittests.py``
will sort all test files by increasing time and run them.
"""
import sys
import os
import unittest
import warnings
import numpy
import clr
from pyquickhelper.pycode import ExtTestCase

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
        clr.AddReference("System.Collections")
        from System import String
        s = String("example")
        x = s.Replace("e", "j")
        self.assertEqual("jxamplj", x)

        from System.Collections.Generic import Dictionary
        d = Dictionary[String, String]()
        d["un"] = "1"
        self.assertEqual(d.Count, 1)

    def test_pythonnet_array(self):
        clr.AddReference("System.Collections")
        from System import IntPtr, Array, Double
        from System.Runtime.InteropServices import Marshal
        self.assertTrue(Double is not None)
        self.assertTrue(Array is not None)
        self.assertTrue(IntPtr is not None)

        array = numpy.ones((2, 2), dtype=int)
        ar = array.__array_interface__['data'][0]
        ar2 = Array[int]([0, 0, 0, 0] * 2)
        self.assertEqual(str(type(ar)), "<class 'int'>")
        self.assertEqual(str(type(ar2)), "<class 'System.Int32[]'>")
        self.assertEqual(list(ar2), [0, 0, 0, 0, 0, 0, 0, 0])
        try:
            Marshal.Copy(ar, ar2, 0, len(ar2))
        except TypeError as e:
            warnings.warn(str(e))
            
    def test_create_cs_function(self):
        code = "public static double SquareX(double x) {return x*x ; }"
        f = create_cs_function("SquareX", code)
        r = f(2.0)
        self.assertEqual(r, 4)     

    def test_magic_cs(self):
        cm = CsMagics()
        code = "public static double SquareX(double x) {return x*x ; }"
        code = """
                public static long[] cs_qsortl(long[] li)
                {
                    if (li.Length == 0)
                    {
                        return null;
                    }
                    else
                    {
                        var pivot = li[0];
                        var lesser = cs_qsortl(li.Skip(1).Where(x => x < pivot).ToArray());
                        var greater = cs_qsortl(li.Skip(1).Where(x => x >= pivot).ToArray());
                        long[] res = new long[li.Length];

                        if (lesser != null && lesser.Length > 0) Array.Copy(lesser, 0, res, 0, lesser.Length);
                        int nb = lesser == null ? 0 : lesser.Length;
                        res[nb] = pivot;
                        if (greater != null && greater.Length > 0) Array.Copy(greater, 0, res, nb + 1, greater.Length);

                        return res;
                    }
                }

                public static long[] cs_qsort(string lis)
                {
                    return cs_qsortl(lis.Split(';').Select(c=>long.Parse(c)).ToArray()) ;
                }
                """
        f = cm.CS("cs_qsort", code)
        if f is None:
            raise Exception(code)
        li = [2, 4, 5, 3, 1]
        lis = ";".join(str(i) for i in li)
        x = f(lis)
        self.assertNotEqual(x, 4)
        self.assertTrue(x is not None)        

if __name__ == "__main__":
    unittest.main()
