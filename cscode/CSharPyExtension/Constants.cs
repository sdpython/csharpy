using System.Reflection;


namespace CSharPyExtension
{
    public static class Constants
    {
        public static string GetFullName()
        {
            return Assembly.GetExecutingAssembly().FullName;
        }
    }
}
