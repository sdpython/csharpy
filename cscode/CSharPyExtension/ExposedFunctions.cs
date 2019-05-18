using System;
using System.Runtime.InteropServices;
using System.Reflection;
using System.Collections.Generic;
using DynamicCS;



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

        public static unsafe int CsUpper(DataStructure* data)
        {
            string text = BytesToString((sbyte*)data->inputs);
            text = text.ToUpper();
            var raw = StringToNullTerminatedBytesUTF8(text);
            NativeAllocation allocate = MarshalDelegate<NativeAllocation>(data->allocate_fct);
            allocate(raw.Length, out data->outputs);
            data->exc = null;
            Marshal.Copy(raw, 0, (IntPtr)data->outputs, raw.Length);
            return 0;
        }

        [StructLayout(LayoutKind.Explicit)]
        public struct CreateFunctionInput
        {
#pragma warning disable 649 // never assigned
            [FieldOffset(0)]
            public void* namePointer;
            [FieldOffset(8)]
            public void* codePointer;
            [FieldOffset(16)]
            public void* usingsPointer;
            [FieldOffset(24)]
            public void* dependenciesPointer;
#pragma warning restore 649 // never assigned
        }

        public static unsafe int CreateFunction(DataStructure* data)
        {
            CreateFunctionInput* inputPtr = (CreateFunctionInput*)data->inputs;
            Int64* outputPtr = (Int64*)data->outputs;
            string name = BytesToString((sbyte*)inputPtr->namePointer);
            string code = BytesToString((sbyte*)inputPtr->codePointer);

            sbyte** c_usings = (sbyte**)inputPtr->usingsPointer;
            var usings = new List<string>();
            while (*c_usings != null)
            {
                usings.Add(BytesToString(*c_usings));
                c_usings++;
            }

            sbyte** c_dependencies = (sbyte**)inputPtr->dependenciesPointer;
            var dependencies = new List<string>();
            while (*c_dependencies != null)
            {
                dependencies.Add(BytesToString(*c_dependencies));
                c_dependencies++;
            }

            string text = "";
            MethodInfo meth;
            try
            {
                meth = DynamicFunction.CreateFunction(name, code, usings.ToArray(), dependencies.ToArray());
            }
            catch (Exception exc)
            {
                meth = null;
                text = exc.ToString();
                text = string.Format("Unable to compile function '{0}' due to {1}\n---CODE---\n{2}\n---USINGS---\n{3}\n---DEPENDENCIES---\n{4}\n---",
                    name, exc.ToString(), code, string.Join("\n", usings), string.Join("\n", dependencies));
            }

            if (meth != null)
            {
                try
                {
                    text = DynamicFunction.MethodSignature(meth);
                }
                catch (Exception exc)
                {
                    meth = null;
                    text = string.Format("Unable to get the signature due to: {0}.", exc.ToString());
                }
            }
            else if (string.IsNullOrEmpty(text))
                text = string.Format("Method '{0}' is null\n---CODE---\n{1}\n---USINGS---\n{2}\n---DEPENDENCIES---\n{3}\n---",
                    name, code, string.Join("\n", usings), string.Join("\n", dependencies));

            *outputPtr = meth == null ? -1 : ObjectStorage.Inst.AddIncref(meth);
            if (meth == null)
                text = text.Replace("\r", "").Replace("\n\n", "\n");
            var raw = StringToNullTerminatedBytesUTF8(text);
            NativeAllocation allocate = MarshalDelegate<NativeAllocation>(data->allocate_fct);
            allocate(raw.Length, out data->exc);
            Marshal.Copy(raw, 0, (IntPtr)data->exc, raw.Length);
            return 0;
        }
    }
}
