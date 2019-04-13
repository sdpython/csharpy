using System.Reflection;

namespace CSharPyExtension
{
    public static class Constants
    {
        public static string Version()
        {
            return "0.1";
        }

        public static string GetFullName()
        {
            return Assembly.GetExecutingAssembly().FullName;
        }
    }
}
