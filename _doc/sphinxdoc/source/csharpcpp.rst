
C# from C++
===========

The module does not directly calls :epkg:`C#` from :epkg:`Python`,
it does it from :epkg:`C++` first. The implemententation
comes from this article:
`Write a custom .NET Core host to control the .NET runtime from your native code
<https://docs.microsoft.com/en-us/dotnet/core/tutorials/netcore-hosting>`_.
It mixes some code from :epkg:`nimbusml`, uses :epkg:`pybind11`
to write a module which calls a :epkg:`C#` function.
Everything is implemented in folder `csnative
<https://github.com/sdpython/csharpy/tree/master/csharpy/csnative>`_.
It also locates the :epkg:`dotnet` assemblies installed with
:epkg:`dotnetcore2`. The design may not be the best but it works
for a demo.

Data
++++

The module first needs to load the main C# DLL
`CSharPyExtension <https://github.com/sdpython/csharpy/tree/master/cscode/CSharPyExtension>`_
which implements C# function callable from C++.
C# automatically managed its own data, a pointer coming out
from C# would only give a temporary pointer to any data it
holds. The data must either be copied or be referred with a
custom identifier, an integer for example.
That's the purpose of class
`ObjectStorage <https://github.com/sdpython/csharpy/blob/master/cscode/CSharPyExtension/Storage.cs>`_.
:pythonnet: creates a Python object for every live C# object,
:epkg:`csharpy` does not. It assumes the use of C# functions
is limited and does not need very complex features.

Agnostic Function
+++++++++++++++++

Passing Python data to C# means passing C++ data to C#.
It supports every signature but to make it simple,
it suggested to use only one signature
``void fct(DataStructure *)`` where *DataStructure* is:

::

    typedef struct DataStructure
    {
    public:
        void* exc;          // Stores an exception. If not NULL, it should a string.
        void* inputs;       // Inputs.
        void* outputs;      // Outputs.
        void* allocate_fct; // Allocates spaces in C++ world: allocate(int size, void** output)
        void* printf_fct;   // Printf function: printf(char msg)
    } DataStructure;

Every data should ba casted void pointers *inputs* and *outputs*
even if it needs to create intermediate structures.
The C# corresponding structure (:epkg:`unsafe`):

.. _l-DataStructure:

::

    [StructLayout(LayoutKind.Explicit)]
    public struct DataStructure
    {
#pragma warning disable 649 // never assigned

        [FieldOffset(0x00)]
        public void* exc;

        [FieldOffset(0x08)]
        public void* inputs;

        [FieldOffset(0x10)]
        public void* outputs;

        [FieldOffset(0x18)]
        public void* allocate_fct;

        [FieldOffset(0x20)]
        public void* printf_fct;
    #pragma warning restore 649 // never assigned
    }

The following example gets a string and returns the
upper case version of it:

::

    public static unsafe int CsUpper(DataStructure* data)
    {
        string text = BytesToString((sbyte*)data->inputs);
        text = text.ToUpper();
        var raw = StringToNullTerminatedBytesUTF8(text);
        NativeAllocation allocate = MarshalDelegate<NativeAllocation>(data->allocate_fct);
        allocate(raw.Length, out data->outputs);
        data->exc = null;
        Marshal.Copy(raw, 0, (IntPtr)data->outputs, raw.Length);
        return 0;
    }

The function needs to have a corresponding C++ function
which calls it. The macro `DECLARE_FCT_NAME
<https://github.com/sdpython/csharpy/blob/master/csharpy/csnative/csmain.hpp#L203>`_
stores a static pointer on the C# function through function
`GetAgnosticFunction
<https://github.com/sdpython/csharpy/blob/master/csharpy/csnative/csmain.hpp#L121>`_.
The macro implements function ``cs_CsUpper`` which calls
`CallAgnosticFunction
<https://github.com/sdpython/csharpy/blob/master/csharpy/csnative/csmain.hpp#L166>`_.

::

    DECLARE_FCT_NAME(CsUpper)

    std::string CsUpper(const std::string &text)
    {
        DataStructure data;
        data.inputs = (void*) text.c_str();
        cs_CsUpper(&data, true);
        std::string res = std::string((char*)data.outputs);
        delete data.outputs;
        return res;
    }

Finally the function needs to be exposed to Python world.
:epkg:`pybind11`` does it which the following lines:

::

    m.def("CsUpper", &CsUpper,
        R"pbdoc(
    Converts a string into upper case using a C# function.
    Shows a way to expose a function taking a string and returning
    another string.

    :param text: any string)pbdoc");

It gives function:

..autosignature:: csharpy.csnative.csmain.CsUpper

Printing, Console
+++++++++++++++++

Class :ref:`l-DataStructure` contains a pointer
``printf_fct``. If not null, it can be used to
prints on :epkg:`Python` standard output. In C# :

::

    Printf cprint = MarshalDelegate<Printf>(data->printf_fct);
    CPrintf(cprint, sout);

Allocation
++++++++++

Data must be copied from C# world to C++ world
unless it is available through a static storage which
keeps a pointer on it in order to avoid the garbage collector
to remove it. This copy must happen within the C# world.
That's the purpose of field ``allocate_fct`` in
:ref:`l-DataStructure`. One example:

::

    NativeAllocation allocate = MarshalDelegate<NativeAllocation>(data->allocate_fct);
    allocate(raw.Length, out data->outputs);

Exception
+++++++++

C# is responsible for catching exception which may happen.
It is not done by default. If it happens, the error message
can be stored into ``exc`` from :ref:`l-DataStructure`.
