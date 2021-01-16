"""
@brief      test log(time=5s)
"""
import unittest
from contextlib import redirect_stdout, redirect_stderr
from io import StringIO
from pyquickhelper.pycode import ExtTestCase
from csharpy.csnative import start, get_clr_path
from csharpy.runtime import create_cs_function
from csharpy.notebook.csmagics import CsMagics


def has_clr():
    try:
        import clr  # pylint: disable=W0611,C0415
    except ImportError:
        return False
    return True


class TestDynamicCS(ExtTestCase):
    """Test dynamic compilation.
    System.Security.Permissions
    System.Private.CoreLib
    """

    def setUp(self):
        start()

    def test_get_clr_path(self):
        path = get_clr_path()
        self.assertExists(path)

    def test_create_cs_function_fails(self):
        from csharpy.csnative.csmain import CsNativeExecutionError  # pylint: disable=E0611,C0415,E0401
        code = "public static double SquareX(doubles x) { return x*x; }"
        self.assertRaise(lambda: create_cs_function("SquareX", code, use_clr=False),
                         CsNativeExecutionError, "'doubles' could not be found")

    def test_create_cs_function_arraydouble(self):
        code = """
        public static double[] SumArrayDouble(double[] xs)
        {
            return new double[] { xs.Sum() };
        }
        """
        f = create_cs_function("SumArrayDouble", code, usings=['System.Linq'],
                               use_clr=False, redirect=False)
        r = f([2.0, 3.5])
        self.assertEqual(r, [5.5])

    def test_create_cs_function_void(self):
        code = "public static void main_void() { }"
        f = create_cs_function("main_void", code, use_clr=False)
        f()

    @unittest.skipIf(not has_clr(), "pythonnet is not installed.")
    def test_create_cs_function_clr(self):
        code = "public static double SquareX(double x) { return x*x; }"
        f = create_cs_function("SquareX", code, use_clr=True)
        r = f(2.0)
        self.assertEqual(r, 4)

    def test_create_cs_function_output(self):
        code = 'public static double SquareX(double x) { Console.WriteLine("check output"); return x*x ; }'
        f = create_cs_function(
            "SquareX", code, redirect=True, usings=["System"])
        if has_clr():
            r = f(2.0)
            self.assertEqual(r, 4)
        else:
            stdout = StringIO()
            with redirect_stdout(stdout):
                r = f(2.0)
            self.assertEqual(r, 4)
            out = stdout.getvalue()
            self.assertEqual(out.replace("\r", "").replace("\n\n", "\n"),
                             "check output\n")

    def test_magic_cs(self):
        cm = CsMagics()
        # code = "public static double SquareX(double x) { return x*x ; }"
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
        f = cm.CS("cs_qsort -i System -i System.Linq",
                  code)
        if f is None:
            raise Exception(code)
        li = [2, 4, 5, 3, 1]
        lis = ";".join(str(i) for i in li)
        x = f(lis)
        self.assertNotEqual(x, 4)
        self.assertTrue(x is not None)

        f = cm.CS("cs_qsort -i System.Linq",
                  "-i System\n" + code)
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
