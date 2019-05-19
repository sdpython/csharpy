using Microsoft.VisualStudio.TestTools.UnitTesting;
using System;
using DynamicCS;
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

        [TestMethod]
        public void TestStorageObject()
        {
            double x = 5.67;
            var i = ObjectStorage.Inst.AddIncref(x);
            var obj = ObjectStorage.Inst.Get(i).Object;
            var d = (double)obj;
            Assert.AreEqual(d, x);
        }

        public delegate double FctTypeDoubleDouble(double x);

        [TestMethod]
        public void TestStorageDelegate()
        {
            double x = 3.456;
            double y = CsBridge.SquareNumber(x);
            var i = ObjectStorage.Inst.AddIncref((FctTypeDoubleDouble)CsBridge.SquareNumber);
            var fct = ObjectStorage.Inst.Get(i).Del;
            var fct_type = (FctTypeDoubleDouble)fct;
            var y2 = fct_type(x);
            Assert.AreEqual(y, y2);
        }

        [TestMethod]
        public void TestStorageMethodInfo()
        {
            var meth = DynamicFunction.CreateFunction("SquareX", "public static double SquareX(double x){return x * x;}",
                                                      null, null, null);
            double x = 3.456;
            double y = (double)meth.Invoke(null, new object[] { x });
            var i = ObjectStorage.Inst.AddIncref(meth);
            var fct = ObjectStorage.Inst.Get(i).MethodInfo;
            double y2 = (double)fct.Invoke(null, new object[] { x });
            Assert.AreEqual(y, y2);
        }
    }
}
