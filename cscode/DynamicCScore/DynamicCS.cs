// See https://github.com/joelmartinez/dotnet-core-roslyn-sample/blob/master/Program.cs.

using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using System.Reflection;
using System.Collections.Immutable;

#if NET4
#else
using Microsoft.CodeAnalysis;
using Microsoft.CodeAnalysis.CSharp;
using Microsoft.CodeAnalysis.Emit;
#endif


namespace DynamicCS
{
    public static class DynamicFunction
    {
        internal static Assembly MissingAssemblies()
        {
            var r = new ImmutableArray<float>();
            return r.GetType().Assembly;
        }

        private const string embedCode = @"
{4}
namespace DynamicCS
{0}                
    public static class DynamicCSFunctions_{2}
    {0}  
        {3}
    {1}
{1}
";

        public static MethodInfo CreateFunction(string functionName, string code,
                                                string[] usings, string[] dependencies)
        {
            Assembly resultAssembly;
            var str_usings = usings == null
                                ? string.Empty
                                : string.Join("\n", usings.Select(u => string.Format("using {0};", u)));

            code = string.Format(embedCode, "{", "}", functionName, code, str_usings);

#if NET4
            var provider = new CSharpCodeProvider();
            var parameters = new CompilerParameters();
            if (dependencies != null)
                foreach (var d in dependencies)
                    parameters.ReferencedAssemblies.Add(d);

            parameters.GenerateInMemory = true;
            parameters.GenerateExecutable = false;

            var results = provider.CompileAssemblyFromSource(parameters, code);
            if (results.Errors.HasErrors)
            {
                StringBuilder sb = new StringBuilder();
                foreach (CompilerError error in results.Errors)
                    sb.AppendLine(String.Format("Error ({0}): {1}", error.ErrorNumber, error.ErrorText));
                sb.AppendLine("---------------");
                sb.AppendLine(code);
                throw new InvalidOperationException(sb.ToString());
            }
            resultAssembly = results.CompiledAssembly;
#else
            SyntaxTree syntaxTree = CSharpSyntaxTree.ParseText(code);

            var assemblies = new List<MetadataReference>();
            assemblies.Add(MetadataReference.CreateFromFile(typeof(object).GetTypeInfo().Assembly.Location));
            if (dependencies != null)
                foreach (var d in dependencies)
                    assemblies.Add(MetadataReference.CreateFromFile(d));

            string assemblyName = "...";

            var compilation = CSharpCompilation.Create(
                            assemblyName,
                            syntaxTrees: new[] { syntaxTree },
                            references: assemblies.ToArray(),
                            options: new CSharpCompilationOptions(OutputKind.DynamicallyLinkedLibrary));

            using (var ms = new MemoryStream())
            {
                EmitResult result = compilation.Emit(ms);

                if (!result.Success)
                {
                    var failures = result.Diagnostics.Where(diagnostic =>
                        diagnostic.IsWarningAsError ||
                        diagnostic.Severity == DiagnosticSeverity.Error);
                    var mes = string.Join("\n", failures.Select(diagnostic => string.Format("\t{0}: {1}", diagnostic.Id, diagnostic.GetMessage())));
                    StringBuilder sb = new StringBuilder();
                    sb.AppendLine(string.Format("Compilation Error, status is {0}.", result.ToString()));
                    sb.AppendLine(mes);
                    sb.AppendLine("---------------");
                    sb.AppendLine(code);
                    throw new InvalidOperationException(sb.ToString());
                }
                else
                {
                    // ms.Seek(0, SeekOrigin.Begin);
                    var content = ms.ToArray();
                    resultAssembly = Assembly.Load(content);
                }
            }
#endif

            Type binaryFunction = resultAssembly.GetType(string.Format("DynamicCS.DynamicCSFunctions_{0}", functionName));
            return binaryFunction.GetMethod(functionName);
        }

        public static object RunFunction(MethodInfo function, object[] parameters)
        {
            return function.Invoke(null, parameters);
        }

        public static Tuple<object, string, string> RunFunctionRedirectOutput(MethodInfo function, object[] parameters)
        {
            using (var std = new StdCapture())
            {
                var res = RunFunction(function, parameters);
                return new Tuple<object, string, string>(res, std.StdOut, std.StdErr);
            }
        }
    }
}
