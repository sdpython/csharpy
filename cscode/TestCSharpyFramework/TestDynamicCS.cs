using System;
using System.Linq;
using System.Runtime;
using Microsoft.VisualStudio.TestTools.UnitTesting;
using DynamicCS;


namespace TestCSharpyFramework
{
    [TestClass]
    public class TestDynamicCS
    {
        [TestMethod]
        public void TestSimpleFunction()
        {
            var code = "public static float SquareX(float x) { return x*x; }";
            var csfunc = DynamicFunction.CreateFunction("SquareX", code, null, null);
            var res = DynamicFunction.RunFunction(csfunc, new object[] { 1.5f });
            Assert.AreEqual(res, 2.25f);
        }
    }
}
