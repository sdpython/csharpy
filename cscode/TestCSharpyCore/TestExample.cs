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
            var exp = StaticExample.SquareNumber(3);
            Assert.AreEqual(exp, 9);
        }
    }
}
