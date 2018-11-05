"""
@brief      test log(time=4s)
"""
import sys
import os
import unittest
from pyquickhelper.helpgen import rst2html
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

from src.csharpy.sphinxext import RunCSharpDirective


class TestRunCSharp(ExtTestCase):
    """Test sphinx extension."""

    def test_src(self):
        "skip pylint"
        self.assertFalse(src is None)

    def test_runcsharp(self):
        content = """
                    .. runcsharpthis::
                        :showcode:
                        :prefix_unittest: src.

                        Console.WriteLine("{0}", 3*3);
                    """.replace("                    ", "")

        tives = [("runcsharpthis", RunCSharpDirective)]

        res = rst2html(content, layout='sphinx',
                       writer="rst",
                       directives=tives)
        self.assertIn('Console.WriteLine("{0}", 3 * 3)', res)

    def test_runcsharp_fct(self):
        content = """
                    .. runcsharpthis::
                        :showcode:
                        :entrypoint: main
                        :prefix_unittest: src.

                        public static double Square(double x) { return x*x; }

                        public static void main() { Console.WriteLine("{0}", Square(3)); }
                    """.replace("                    ", "")

        tives = [("runcsharpthis", RunCSharpDirective)]

        res = rst2html(content, layout='sphinx',
                       writer="rst",
                       directives=tives)
        self.assertIn('9', res)

    def test_runcsharp_class(self):
        content = """
                    .. runcsharpthis::
                        :showcode:
                        :entrypoint: main
                        :prefix_unittest: src.

                        public static class Zoo {
                        public static double Square(double x) { return x*x; }
                        }

                        public static void main() { Console.WriteLine("{0}", Zoo.Square(3)); }
                    """.replace("                    ", "")

        tives = [("runcsharpthis", RunCSharpDirective)]

        res = rst2html(content, layout='sphinx',
                       writer="rst",
                       directives=tives)
        self.assertIn('9', res)

    def test_runcsharp_linq(self):
        content = """
                    .. runcsharpthis::
                        :showcode:
                        :dependency: System.Core
                        :using: System.Linq, System.Text, System.Collections.Generic
                        :prefix_unittest: src.

                        var li = new [] {"a", "b"};
                        var mes = string.Join(",", li.Select(c => c.ToUpper()));
                        Console.WriteLine("{0}", mes);
                    """.replace("                    ", "")

        tives = [("runcsharpthis", RunCSharpDirective)]

        res = rst2html(content, layout='sphinx',
                       writer="rst",
                       directives=tives)
        self.assertIn('A,B', res)


if __name__ == "__main__":
    unittest.main()
