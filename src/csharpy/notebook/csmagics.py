# -*- coding: utf-8 -*-
"""
@file
@brief Defines magic commands to interact with C# in a :epkg:`Python` notebook.
"""
import sys

from IPython.core.magic import Magics, magics_class, line_magic, cell_magic
from IPython.core.magic import line_cell_magic
from IPython.core.display import HTML
from ..runtime import create_cs_function


@magics_class
class CsMagics(Magics):
    """
    Defines magic commands for notebooks.
    """

    @cell_magic
    def CS(self, line, cell):
        """
        Defines magic command ``%%CS``.

        .. nbref::
            :title: %%CS

            The magic command wraps the :epkg:`C#` code into a
            :epkg:`Python` function the user can call.

            ::

                %%CS cspower System.dll
                public static double cspower(double x, double y)
                {
                    if (y == 0) return 1.0 ;
                    return System.Math.Pow(x,y) ;
                }

            To call it:

            ::

                cspower(3.0, 3.0)
                
            The magic command relies on @see fn create_cs_function
            and adds it to the notebook context.            
        """
        if not sys.platform.startswith("win"):
            raise Exception("Works only on Windows.")

        if line is not None:
            spl = line.strip().split(" ")
            name = spl[0]
            deps = spl[1].split(";") if len(spl) > 1 else ""
            suse = spl[2].split(";") if len(spl) > 2 else ""

        if name == "-h":
            print("Usage: "
                  "   %%CS function_name [dependency1;dependency2] [System;System.Linq]"
                  "   function code")
        else:
            try:
                f = create_cs_function(name, cell, deps, suse)
            except Exception as e:
                print(e)
                return
            if self.shell is not None:
                self.shell.user_ns[name] = f
            return f
        return None


def register_magics(ip):
    """
    Registers magics commands.
    """
    ip.register_magics(CsMagics)
    patch = ("IPython.config.cell_magic_highlight['csmagic'] = "
             "{'reg':[/^%%CS/]};")
    js = display.Javascript(data=patch,
                            lib=["https://github.com/codemirror/CodeMirror/blob/master/mode/clike/clike.js"])
    