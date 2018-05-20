import sphinx_gallery
import sphinx_rtd_theme
from pyquickhelper.helpgen.default_conf import set_sphinx_variables, get_default_stylesheet
from csharpy import __file__
print(__file__)

set_sphinx_variables(__file__, "csharpy", "sdpython", 2018,
                     "sphinx_rtd_theme", [
                         sphinx_rtd_theme.get_html_theme_path()],
                     locals(), book=True,
                     extlinks=dict(issue=('https://github.com/sdpython/csharpy/issues/%s', 'issue')))

blog_root = "http://www.xavierdupre.fr/app/csharpy/helpsphinx/"

html_context = {
    'css_files': get_default_stylesheet(),
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
