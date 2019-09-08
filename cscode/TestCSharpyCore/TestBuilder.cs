using Microsoft.VisualStudio.TestTools.UnitTesting;
using DynamicCS;
using CSharPyExtension;


namespace TestCSharpyCore
{
    [TestClass]
    public class TestBuilder
    {
        [TestMethod]
        public void TestSHA256()
        {
            var raw = "abc";
            var cmp = BuildHelper.ComputeSha256Hash(raw);
            Assert.IsNotNull(cmp);
            Assert.IsTrue(cmp.Length >= 10);
        }
    }
}

