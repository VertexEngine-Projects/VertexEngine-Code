import math

class Vector2:
    """Vector 2 is a class of math that is especially for Vector Twos.
    Vector 2 is the 2D position of a selected point in math.
    It uses (x,y) coordinates."""
    def __init__(self, x=0.0, y=0.0):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Vector2({self.x}, {self.y})"

    # Vector addition
    def __add__(self, other):
        return Vector2(self.x + other.x, self.y + other.y)

    # Vector subtraction
    def __sub__(self, other):
        return Vector2(self.x - other.x, self.y - other.y)

    # Scalar multiplication
    def __mul__(self, scalar):
        return Vector2(self.x * scalar, self.y * scalar)

    def __rmul__(self, scalar):
        return self.__mul__(scalar)

    # Vector magnitude
    def magnitude(self):
        """This is the magnitude of the Vector."""
        return math.sqrt(self.x**2 + self.y**2)

    # Vector normalization
    def normalize(self):
        """This will normalize the Vector."""
        mag = self.magnitude()
        if mag == 0:
            return Vector2(0, 0)
        return Vector2(self.x / mag, self.y / mag)

    # Dot product
    def dot(self, other):
        """Dot product can multiply this Vector 2 with another Vector 2, this will not work with Vector 2 * Vector [any number != 2]"""
        return self.x * other.x + self.y * other.y

    # Rotate vector by angle in degrees
    def rotate(self, angle_degrees):
        """This will rotate the Vector by `x` degrees."""
        angle_radians = math.radians(angle_degrees)
        cos_a = math.cos(angle_radians)
        sin_a = math.sin(angle_radians)
        x_new = self.x * cos_a - self.y * sin_a
        y_new = self.x * sin_a + self.y * cos_a
        return Vector2(x_new, y_new)
    
