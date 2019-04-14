using System;
using System.Runtime.InteropServices;


namespace CSharPyExtension
{
    public unsafe static partial class CsBridge
    {
        public static unsafe double SquareNumber(double x)
        {
            if (x < 0)
                throw new Exception("Fails if x < 0.");
            return x * x;
        }

        public static unsafe int RandomString(DataStructure* data)
        {
            string text = "Français";
            var raw = StringToNullTerminatedBytesUTF8(text);
            NativeAllocation allocate = MarshalDelegate<NativeAllocation>(data->allocate_fct);
            allocate(raw.Length, out data->outputs);
            data->exc = null;
            Marshal.Copy(raw, 0, (IntPtr)data->outputs, raw.Length);
            return 0;
        }
    }
}
