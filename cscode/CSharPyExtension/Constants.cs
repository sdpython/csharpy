using System;
using System.Reflection;


namespace CSharPyExtension
{
    public static class Constants
    {
        public static string GetFullName()
        {
            return Assembly.GetExecutingAssembly().FullName;
        }

        public static Span<int> GetSpan(int[] array, int begin = 0, int end = -1)
        {
            return array.AsSpan(begin, end == -1 ? array.Length - begin : end - begin);
        }
    }
}
