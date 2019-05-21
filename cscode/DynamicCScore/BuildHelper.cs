using System;
using System.Collections.Generic;


namespace DynamicCS
{
    public static class BuildHelper
    {
        public static string[] GetAssemblyList()
        {
            var res = new List<string>();
            foreach (var c in AppDomain.CurrentDomain.GetAssemblies())
            {
                string name;
                try
                {
                    name = c.Location;
                }
                catch (Exception)
                {
                    continue;
                }
                if (!string.IsNullOrEmpty(name) && !name.Contains("TestCSharpyCore") &&
                    !name.Contains("testplatform") && !name.Contains("mstest"))
                    res.Add(name);
            }
            return res.ToArray();
        }
    }
}
