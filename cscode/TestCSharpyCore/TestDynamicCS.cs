using Microsoft.VisualStudio.TestTools.UnitTesting;
using DynamicCS;
using System.IO;
using System.Linq;


namespace TestCSharpyCore
{
    [TestClass]
    public class TestDynamicCS
    {
        [TestMethod]
        public void TestPyDynamicCS()
        {
            var meth = DynamicFunction.CreateFunction("SquareX", "public static double SquareX(double x){return x * x;}",
                                                      null, null, null);
            var sig = DynamicFunction.MethodSignature(meth);
            Assert.AreEqual(sig, "Double->Double");
            var result = DynamicFunction.RunFunctionRedirectOutput(meth, new object[] { (double)3 });
            Assert.AreEqual(result.Item1, 9.0);
        }

        [TestMethod]
        public void TestListAssemblies()
        {
            var meth = DynamicFunction.CreateFunction("SquareX", "public static double SquareX(double x){return x * x;}",
                                                      null, null, null);
            var result = DynamicFunction.RunFunctionRedirectOutput(meth, new object[] { (double)3 });
            Assert.AreEqual(result.Item1, 9.0);

            var cslist = BuildHelper.GetAssemblyList();
            cslist = cslist.OrderBy(c => c).ToArray();
            Assert.IsTrue(cslist.Length > 0);
            var thispath = Path.Combine("..", "..", "..", "..");
            var tpath = Path.Combine(thispath, "csdependencies.txt");
            File.WriteAllText(tpath, string.Join("\n", cslist));
        }
    }
}
