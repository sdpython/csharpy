using Microsoft.VisualStudio.TestTools.UnitTesting;
using CSharPyExtension;


namespace TestCSharpyCore
{
    [TestClass]
    public class TestCSharpy
    {
        [TestMethod]
        public void TestGetFullName()
        {
            var res = Constants.GetFullName();
            Assert.IsTrue(res.Contains("CSharPy"));
        }

        [TestMethod]
        public void TestStorage()
        {
            object obj = new object();
            var i = ObjectStorage.Inst.AddIncref(obj);
            Assert.AreEqual(ObjectStorage.Inst.Nref(i), 1);
            ObjectStorage.Inst.Incref(i);
            Assert.AreEqual(ObjectStorage.Inst.Nref(i), 2);
            ObjectStorage.Inst.Decref(i);
            Assert.AreEqual(ObjectStorage.Inst.Nref(i), 1);
            ObjectStorage.Inst.Decref(i);
            Assert.AreEqual(ObjectStorage.Inst.Nref(i), 0);
        }
    }
}
