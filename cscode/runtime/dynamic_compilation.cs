using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.CodeDom.Compiler;
using Microsoft.CSharp;
using System.Reflection;


namespace DynamicCS
{
    public static class DynamicFunction
    {
        private const string embedCode = @"
                    namespace DynamicCS
                    {0}                
                        public static class DynamicCSFunctions_{2}
                        {0}  
                            {3}
                        {1}
                    {1}
                    ";

        public static MethodInfo CreateFunction(string functionName, string code, string[] dependencies)
        {
            CSharpCodeProvider provider = new CSharpCodeProvider();
            CompilerParameters parameters = new CompilerParameters();

            if (dependencies != null) {
                foreach (var d in dependencies)
                    parameters.Refer
                encedAssemblies.Add(d);
            }

            parameters.GenerateInMemory = true;
            parameters.GenerateExecutable = false;

            code = string.Format(embedCode, "{", "}", functionName, code);

            CompilerResults results = provider.CompileAssemblyFromSource(parameters, code);
            if (results.Errors.HasErrors) {
                StringBuilder sb = new StringBuilder();
                foreach (CompilerError error in results.Errors) {
                    sb.AppendLine(String.Format("Error ({0}): {1}", error.ErrorNumber, error.ErrorText));
                }
                throw new InvalidOperationException(sb.ToString());
            }
            Type binaryFunction = results.CompiledAssembly.GetType(string.Format("DynamicCS.DynamicCSFunctions_{0}", functionName));
            return binaryFunction.GetMethod(functionName);
        }

        public static object RunFunction(MethodInfo function, object[] parameters)
        {
            return function.Invoke(null, parameters);
        }
    }
}
