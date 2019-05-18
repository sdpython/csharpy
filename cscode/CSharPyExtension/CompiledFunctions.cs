using System;
using System.Runtime.InteropServices;


namespace CSharPyExtension
{
    public unsafe static partial class CsBridge
    {
        [StructLayout(LayoutKind.Explicit)]
        public struct CallDoubleDoubleInput
        {
#pragma warning disable 649 // never assigned
            [FieldOffset(0)]
            public Int64 fct;
            [FieldOffset(8)]
            public double x;
#pragma warning restore 649 // never assigned
        }

        public delegate double FctDoubleDouble(double x);

        public static unsafe int CallDoubleDouble(DataStructure* data)
        {
            Console.WriteLine("has data");
            CallDoubleDoubleInput* input = (CallDoubleDoubleInput*)data->inputs;
            Console.WriteLine("x {0}", input->x);
            Console.WriteLine("has data0");
            var fctobj = ObjectStorage.Inst.Get(input->fct);
            Console.WriteLine("has data1 {0}", fctobj);
            var fct = (FctDoubleDouble)fctobj;
            Console.WriteLine("has data2");
            double* output = (double*)data->outputs;
            Console.WriteLine("x {0}", input->x);
            *output = fct(input->x);
            Console.WriteLine("y {0}", *output);
            return 0;
        }
    }
}
