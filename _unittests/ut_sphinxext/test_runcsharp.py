"""
@brief      test log(time=6s)
"""
import unittest
from pyquickhelper.helpgen import rst2html
from pyquickhelper.pycode import ExtTestCase
from csharpy.sphinxext import RunCSharpDirective
from csharpy.csnative import start


class TestRunCSharp(ExtTestCase):
    """Test sphinx extension."""

    def setUp(self):
        start()

    def test_runcsharp_fct(self):
        content = """
                    .. runcsharpthis::
                        :showcode:
                        :entrypoint: main

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
                        :using: System.Linq, System.Text, System.Collections.Generic

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
