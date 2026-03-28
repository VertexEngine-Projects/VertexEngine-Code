"""This is the math module of VertexEngine. This contains some math classes for sprites and other things.
This is NOT to be confused with `math` python stdlib. This is `VertexEngine.GraphicalMath`, not `math`"""
from ._Vector2 import _Vector2, _UtilityFunctions

class math:
    """This is the GraphicalMath class of VertexEngine. It contains some math classes for sprites and other things."""
    def __init__(self):
        self.Vector2 = _Vector2()
        self.Utils = _UtilityFunctions()