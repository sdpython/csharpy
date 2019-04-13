using System;
using System.Runtime.InteropServices;
using System.Text;

namespace CSharPyExtension
{
    public unsafe static partial class CsBridge
    {
        /// <summary>
        /// Copy of a C++ structure.
        /// </summary>
        [StructLayout(LayoutKind.Explicit)]
        private struct DataStructure
        {
#pragma warning disable 649 // never assigned
            [FieldOffset(0x00)]
            public readonly long aLong;
            [FieldOffset(0x08)]
            public readonly double aDouble;
            [FieldOffset(0x10)]
            public readonly float aFloat;
            [FieldOffset(0x14)]
            public readonly byte aByte;
            [FieldOffset(0x15)]
            public readonly byte aSecondByte;
            [FieldOffset(0x17)]
            public readonly short aShort;
            [FieldOffset(0x18)]
            public readonly float* aFloatPointer;
            [FieldOffset(0x20)]
            public readonly char* aString;
#pragma warning restore 649 // never assigned
        }

        /// <summary>
        /// Converts UTF8 bytes with known length to ROM<char>. Negative length unsupported.
        /// </summary>
        public static void BytesToText(sbyte* prgch, ulong bch, ref string dst)
        {
            dst = (bch > 0) ? BytesToString(prgch, bch) : string.Empty;
        }

        /// <summary>
        /// Converts null-terminated UTF8 bytes to ROM<char>. Null pointer unsupported.
        /// </summary>
        public static void BytesToText(sbyte* psz, ref string dst)
        {
            dst = (psz != null) ? BytesToString(psz) : string.Empty;
        }

        /// <summary>
        /// Converts UTF8 bytes with known positive length to a string.
        /// </summary>
        public static string BytesToString(sbyte* prgch, ulong bch)
        {
            return Encoding.UTF8.GetString((byte*)prgch, (int)bch);
        }

        /// <summary>
        /// Convert null-terminated UTF8 bytes to a string.
        /// </summary>
        public static string BytesToString(sbyte* psz)
        {
            if (psz == null)
                return null;
            int cch = 0;
            while (psz[cch] != 0)
                cch++;

            if (cch == 0)
                return null;
#if CORECLR
            return Encoding.UTF8.GetString((byte*)psz, cch);
#else
            if (cch <= 0)
                return "";

            var decoder = Encoding.UTF8.GetDecoder();
            var chars = new char[decoder.GetCharCount((byte*)psz, cch, true)];
            int bytesUsed;
            int charsUsed;
            bool complete;
            fixed (char* pchars = chars)
                decoder.Convert((byte*)psz, cch, pchars, chars.Length, true, out bytesUsed, out charsUsed, out complete);
            return new string(chars);
#endif
        }

        /// <summary>
        /// Converts a string to null-terminated UTF8 bytes.
        /// </summary>
        internal static byte[] StringToNullTerminatedBytes(string str)
        {
            // Note that it will result in multiple UTF-8 null bytes at the end, which is not ideal but harmless.
            return Encoding.UTF8.GetBytes(str + Char.MinValue);
        }
    }
}
