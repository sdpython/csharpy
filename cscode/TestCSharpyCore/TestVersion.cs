using Microsoft.VisualStudio.TestTools.UnitTesting;
using CSharPyExtension;


namespace TestCSharpyCore
{
    [TestClass]
    public class TestVersion
    {
        [TestMethod]
        public void TesTestVersion()
        {
            Assert.AreEqual(Constants.Version(), "0.1");
        }
    }
}
