"""
@file
@brief Extends Sphinx to easily write documentation.
"""
import os
import sphinx
from docutils.parsers.rst import directives
from pyquickhelper.sphinxext.sphinx_runpython_extension import RunPythonDirective


def _make_options():
    option_spec = RunPythonDirective.option_spec.copy()
    option_spec.update({
        'dependency': directives.unchanged,
        'entrypoint': directives.unchanged,
        'using': directives.unchanged,
        'prefix_unittest': directives.unchanged,
    })
    return option_spec


class RunCSharpDirective(RunPythonDirective):
    """
    Runs a :epkg:`C#` script based on
    :epkg:`runpython`.
    The directive adds a couple of options:

    * ``'dependency'``: list of necessary dependencies,
      list comma separated
    * ``'entrypoint'``: function to call first to start the program,
      it can be empty, it must be a function without any argument.
    * ``'using'``: list of necessary usings,
      list comma separated

    A few examples, the first one shows how to call one
    function inside others.

    ::

        .. runcsharp::
            :showcode:
            :entrypoint: main

            public static class Zoo
            {
                public static double Square(double x)
                {
                    return x*x;
                }
            }

            public static void main()
            {
                Console.WriteLine("{0}", Zoo.Square(3));
            }

    Which renders as:

    .. runcsharp::
        :showcode:
        :entrypoint: main

        public static class Zoo
        {
            public static double Square(double x)
            {
                return x*x;
            }
        }

        public static void main()
        {
            Console.WriteLine("{0}", Zoo.Square(3));
        }

    The next one does not have any function (and cannot have)
    but requires some dependencies.

    ::

        .. runcsharp::
            :showcode:
            :dependency: System.Core
            :language: csharp
            :using: System.Linq, System.Text, System.Collections.Generic

            var li = new [] {"a", "b"};
            var mes = string.Join(",", li.Select(c => c.ToUpper()));
            Console.WriteLine("{0}", mes);

    Which renders as:

    .. runcsharp::
        :showcode:
        :dependency: System.Core
        :language: csharp
        :using: System.Linq, System.Text, System.Collections.Generic

        var li = new [] {"a", "b"};
        var mes = string.Join(",", li.Select(c => c.ToUpper()));
        Console.WriteLine("{0}", mes);
    """

    option_spec = _make_options()

    def modify_script_before_running(self, script):
        """
        The methods modifies the script to *csharpy* to
        run :epkg:`C#` from :epkg:`Python`.
        """
        usings = self.options.get('using', '')
        dependencies = self.options.get('dependency', '')
        return self._modify_script_before_running(script, usings, dependencies)

    def _modify_script_before_running(self, script, usings, dependencies):
        if 'language' not in self.options:
            self.options['language'] = 'csharp'
        if isinstance(usings, str):
            usings = [n.strip() for n in usings.strip().split(',')]
        if isinstance(dependencies, str):
            dependencies = [n.strip().replace("\\", "\\\\")
                            for n in dependencies.strip().split(',')]
        usings = [_ for _ in usings if _]
        dependencies = [_ for _ in dependencies if _]
        if "System" not in usings:
            usings.append("System")
        usings.sort()
        dependencies.sort()

        local_path = os.path.abspath(os.path.dirname(
            self.state.document.current_source))

        entrypoint = self.options.get('entrypoint', '').strip()
        const = 'const string RELPATH = @"{0}";'.format(
            local_path.replace("\\", "\\\\"))
        if len(entrypoint) == 0:
            entrypoint = "main_{0}".format(id(self))
            script = "public static void {0}()\n{{\n{1}\n\n{2}\n}}\n".format(
                entrypoint, const, script)
        else:
            script = "\n{0}\n\n{1}".format(const, script)

        prefix = self.options.get('prefix_unittest', '')

        script = ["from textwrap import dedent",
                  "from {0}csharpy.runtime import create_cs_function".format(
                      prefix),
                  "content = dedent('''",
                  script,
                  "''')"
                  "",
                  "name = '{0}'".format(entrypoint),
                  "fct = create_cs_function(name, content, redirect=True,",
                  "                         usings={0},".format(usings),
                  "                         dependencies={0},".format(
                      dependencies),
                  "                        )",
                  "_, out, err = fct()",
                  "if err:",
                  "    print('--OUT--\\n{0}\\n--ERR--\\n{1}'.format(out, err))",
                  "else:",
                  "    print(out)",
                  ]
        return "\n".join(script)


def setup(app):
    """
    Adds the directive @see cl RunCSharpDirective.
    """
    app.add_directive('runcsharp', RunCSharpDirective)
    return {'version': sphinx.__display_version__, 'parallel_read_safe': True}
