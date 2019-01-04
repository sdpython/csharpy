using System;
using System.Linq;
using System.Collections.Generic;
using System.Reflection;


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
                if (name.Contains("csharpy") && !name.Contains("TestCSharpyCore") && 
                    !name.Contains("testplatform") && !name.Contains("mstest"))
                    res.Add(name);
            }
            return res.ToArray();
        }
    }
}
