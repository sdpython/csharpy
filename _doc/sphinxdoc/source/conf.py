import sys
import os
import sphinx_gallery
import sphinx_rtd_theme
from pyquickhelper.helpgen.default_conf import set_sphinx_variables, get_default_stylesheet

sys.path.insert(0, os.path.abspath(os.path.join(os.path.split(__file__)[0])))

set_sphinx_variables(__file__, "csharpy", "sdpython", 2019,
                     "sphinx_rtd_theme", [
                         sphinx_rtd_theme.get_html_theme_path()],
                     locals(), book=True,
                     add_extensions=[
                         "csharpy.sphinxext.sphinx_runcsharp_extension"],
                     extlinks=dict(issue=('https://github.com/sdpython/csharpy/issues/%s', 'issue')))

blog_root = "http://www.xavierdupre.fr/app/csharpy/helpsphinx/"

html_context = {
    'css_files': get_default_stylesheet() + ['_static/my-styles.css', '_static/gallery.css'],
}

nblinks = {'slideshowrst': 'http://www.xavierdupre.fr/'}


def custom_latex_processing(latex):
    """
    Processes a :epkg:`latex` file and returned the modified version.

    @param      latex       string
    @return                 string
    """
    if latex is None:
        raise ValueError("Latex is null")
    # this weird modification is only needed when jenkins run a unit test in
    # pyquickhelper (pycode)
    return latex


epkg_dictionary.update({
    'C#': 'https://en.wikipedia.org/wiki/C_Sharp_(programming_language)',
    'C++': 'https://en.wikipedia.org/wiki/C%2B%2B',
    'csharpy': 'http://www.xavierdupre.fr/app/csharpy/helpsphinx/index.html',
    'dotnet': 'https://dotnet.microsoft.com/',
    'dotnetcore': 'https://github.com/dotnet/core',
    'dotnetcore2': 'https://pypi.org/project/dotnetcore2/',
    'JIT': 'https://en.wikipedia.org/wiki/Just-in-time_compilation',
    'mono': 'https://www.mono-project.com/',
    'nimbusml': 'https://github.com/Microsoft/NimbusML',
    'pybind11': 'https://github.com/pybind/pybind11',
    'pythonnet': 'https://github.com/pythonnet/pythonnet',
    'runpython': 'http://www.xavierdupre.fr/app/pyquickhelper/helpsphinx/pyquickhelper/sphinxext/sphinx_runpython_extension.html#pyquickhelper.sphinxext.sphinx_runpython_extension.RunPythonDirective',
})
