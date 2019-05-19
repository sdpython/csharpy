using System;
using System.Runtime.InteropServices;
using DynamicCS;


namespace CSharPyExtension
{
    public unsafe static partial class CsBridge
    {
        #region CallVoid

        public static unsafe int CallVoid(DataStructure* data)
        {
            if (data->printf_fct != null)
                return CaptureStdOutput(CallVoid, data);
            Int64* p_fct = (Int64*)data->exc;
            var fctref = ObjectStorage.Inst.Get(*p_fct);
            var fct = fctref.MethodInfo;
            fct.Invoke(null, null);
            return 0;
        }

        #endregion

        #region CallDoubleDouble

        public static unsafe int CallDoubleDouble(DataStructure* data)
        {
            if (data->printf_fct != null)
                return CaptureStdOutput(CallDoubleDouble, data);
            double* p_x = (double*)data->inputs;
            Int64* p_fct = (Int64*)data->exc;
            var fctref = ObjectStorage.Inst.Get(*p_fct);
            var fct = fctref.MethodInfo;
            double* output = (double*)data->outputs;
            *output = (double)fct.Invoke(null, new object[] { *p_x });
            return 0;
        }

        #endregion

        #region CallArrayInt32String

        [StructLayout(LayoutKind.Explicit)]
        public struct CallArrayInt32StringOutput
        {
#pragma warning disable 649 // never assigned
            [FieldOffset(0)]
            public void* p;
            [FieldOffset(8)]
            public int nb;
#pragma warning restore 649 // never assigned
        }

        public static unsafe int CallArrayInt32String(DataStructure* data)
        {
            if (data->printf_fct != null)
                return CaptureStdOutput(CallArrayInt32String, data);
            string content = BytesToString((sbyte*)data->inputs);
            Int64* p_fct = (Int64*)data->exc;
            var fctref = ObjectStorage.Inst.Get(*p_fct);
            var fct = fctref.MethodInfo;
            var cs_output = fct.Invoke(null, new object[] { content }) as int[];
            CallArrayInt32StringOutput* output = (CallArrayInt32StringOutput*)data->outputs;
            output->nb = cs_output.Length;
            if (cs_output.Length > 0)
            {
                NativeAllocation allocate = MarshalDelegate<NativeAllocation>(data->allocate_fct);
                int size = cs_output.Length * sizeof(int);
                allocate(size, out output->p);
                Marshal.Copy(cs_output, 0, (IntPtr)output->p, cs_output.Length);
            }
            return 0;
        }

        #endregion

        #region CallArrayDoubleArrayDouble

        [StructLayout(LayoutKind.Explicit)]
        public struct CallArrayDoubleArrayDoubleIO
        {
#pragma warning disable 649 // never assigned
            [FieldOffset(0)]
            public void* p;
            [FieldOffset(8)]
            public int nb;
#pragma warning restore 649 // never assigned
        }

        public static unsafe int CallArrayDoubleArrayDouble(DataStructure* data)
        {
            if (data->printf_fct != null)
                return CaptureStdOutput(CallArrayDoubleArrayDouble, data);

            CallArrayDoubleArrayDoubleIO* input = (CallArrayDoubleArrayDoubleIO*)data->inputs;
            var vec = new double[input->nb];
            double* src = (double*)input->p;
            for (int i = 0; i < vec.Length; ++i)
                vec[i] = src[i];

            Int64* p_fct = (Int64*)data->exc;
            var fctref = ObjectStorage.Inst.Get(*p_fct);
            var fct = fctref.MethodInfo;
            var cs_output = fct.Invoke(null, new object[] { vec }) as double[];
            CallArrayDoubleArrayDoubleIO* output = (CallArrayDoubleArrayDoubleIO*)data->outputs;
            output->nb = cs_output.Length;
            if (cs_output.Length > 0)
            {
                NativeAllocation allocate = MarshalDelegate<NativeAllocation>(data->allocate_fct);
                int size = cs_output.Length * sizeof(double);
                allocate(size, out output->p);
                Marshal.Copy(cs_output, 0, (IntPtr)output->p, cs_output.Length);
            }
            return 0;
        }

        #endregion
    }
}
