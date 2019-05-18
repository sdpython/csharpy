"""
@brief      test log(time=2s)
"""
import unittest
from contextlib import redirect_stdout, redirect_stderr
from io import StringIO
from dotnetcore2 import runtime as clr_runtime
from pyquickhelper.pycode import ExtTestCase
from csharpy.csnative import start, get_clr_path
from csharpy.runtime import create_cs_function
from csharpy.notebook.csmagics import CsMagics


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
        self.assertIn(clr_runtime._get_bin_folder(),  # pylint: disable=W0212
                      path)

    def test_create_cs_function_fails(self):
        from csharpy.csnative.csmain import CsNativeExecutionError  # pylint: disable=E0611
        code = "public static double SquareX(doubles x) { return x*x; }"
        self.assertRaise(lambda: create_cs_function("SquareX", code, use_clr=False),
                         CsNativeExecutionError, "'doubles' could not be found")

    def test_create_cs_function(self):
        code = "public static double SquareX(double x) { return x*x; }"
        f = create_cs_function("SquareX", code, use_clr=False)
        r = f(2.0)
        self.assertEqual(r, 4)

    def test_create_cs_function_clr(self):
        code = "public static double SquareX(double x) { return x*x; }"
        f = create_cs_function("SquareX", code, use_clr=True)
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
    # print(get_clr_path())
    # ADD: metaadd = Assembly Path='C:\Program Files\dotnet\shared\Microsoft.NETCore.App\2.1.9\System.Private.CoreLib.dll'
    TestDynamicCS().setUp()
    TestDynamicCS().test_create_cs_function_fails()
    TestDynamicCS().test_create_cs_function()
    unittest.main()
