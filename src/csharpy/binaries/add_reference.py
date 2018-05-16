"""
@file
@brief 
"""
from clr import AddReference as ClrAddReference

def AddReference(name):
    """
    Imports a :epkg:`C#` dll.
    """
    ClrAddReference(name)

