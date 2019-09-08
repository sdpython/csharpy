using System;
using System.Text;
using System.Collections.Generic;
using System.Security.Cryptography;


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

        public static string ComputeSha256Hash(string rawData)
        {
            // Create a SHA256   
            using (SHA256 sha256Hash = SHA256.Create())
            {
                // ComputeHash - returns byte array  
                byte[] bytes = sha256Hash.ComputeHash(Encoding.UTF8.GetBytes(rawData));

                // Convert byte array to a string   
                StringBuilder builder = new StringBuilder();
                for (int i = 0; i < bytes.Length; i++)
                {
                    builder.Append(bytes[i].ToString("x2"));
                }
                return builder.ToString();
            }
        }
    }
}
