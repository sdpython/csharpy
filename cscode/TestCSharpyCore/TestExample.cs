using Microsoft.VisualStudio.TestTools.UnitTesting;
using CSharPyExtension;


namespace TestCSharpyCore
{
    [TestClass]
    public class TestCsharpyExt
    {
        [TestMethod]
        public void TestStaticSquare()
        {
            var exp = CsBridge.SquareNumber(3);
            Assert.AreEqual(exp, 9);
        }

        [TestMethod]
        public void TestFullName()
        {
            var exp = Constants.GetFullName();
            // throw new System.Exception(exp);
            Assert.IsTrue(exp.StartsWith("CSharPyExtension"));
        }
    }
}
