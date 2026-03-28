import math

class _Vector2:
    """Represents a 2D vector using (x, y) coordinates.

    Supports common vector math operations such as addition,
    subtraction, scaling, normalization, dot product, and more.
    """

    def __init__(self, x=0.0, y=0.0):
        """Initialize a _Vector2.

        Args:
            x (float): X-coordinate.
            y (float): Y-coordinate.
        """
        self.x = x
        self.y = y

    def __repr__(self):
        """Return a readable string representation."""
        return f"_Vector2({self.x}, {self.y})"

    # ------------------------
    # Basic Operators
    # ------------------------

    def __add__(self, other):
        """Add two vectors."""
        return _Vector2(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        """Subtract another vector from this vector."""
        return _Vector2(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar):
        """Multiply vector by a scalar."""
        return _Vector2(self.x * scalar, self.y * scalar)

    def __rmul__(self, scalar):
        """Allow scalar * vector multiplication."""
        return self.__mul__(scalar)

    def __truediv__(self, scalar):
        """Divide vector by a scalar."""
        if scalar == 0:
            raise ValueError("Cannot divide by zero.")
        return _Vector2(self.x / scalar, self.y / scalar)

    # ------------------------
    # Magnitude & Normalization
    # ------------------------

    def magnitude(self):
        """Return the length (magnitude) of the vector."""
        return math.sqrt(self.x**2 + self.y**2)

    def magnitude_squared(self):
        """Return the squared magnitude (faster, avoids sqrt)."""
        return self.x**2 + self.y**2

    def normalize(self):
        """Return a normalized (unit length) version of the vector."""
        mag = self.magnitude()
        if mag == 0:
            return _Vector2(0, 0)
        return self / mag

    # ------------------------
    # Vector Math
    # ------------------------

    def dot(self, other):
        """Return the dot product with another vector.""" 
        return self.x * other.x + self.y * other.y

    def distance_to(self, other):
        """Return the distance to another vector."""
        return (self - other).magnitude()

    def angle_to(self, other):
        """Return the angle (in degrees) between two vectors."""
        dot = self.dot(other)
        mags = self.magnitude() * other.magnitude()
        if mags == 0:
            return 0.0
        cos_theta = max(-1.0, min(1.0, dot / mags))
        return math.degrees(math.acos(cos_theta))

    def rotate(self, angle_degrees):
        """Return a new vector rotated by angle (in degrees)."""
        angle_radians = math.radians(angle_degrees)
        cos_a = math.cos(angle_radians)
        sin_a = math.sin(angle_radians)
        return _Vector2(
            self.x * cos_a - self.y * sin_a,
            self.x * sin_a + self.y * cos_a
        )

class _UtilityFunctions:
    """These are the Utility Functions of `GraphicalMath`."""
    # ------------------------
    # Utility Functions
    # ------------------------

    def clamp(self, min_vec, max_vec):
        """Clamp this vector between two vectors.

        Args:
            min_vec (_Vector2): Minimum bounds.
            max_vec (_Vector2): Maximum bounds.

        Returns:
            _Vector2: Clamped vector.
        """
        return _Vector2(
            max(min_vec.x, min(self.x, max_vec.x)),
            max(min_vec.y, min(self.y, max_vec.y))
        )

    def clamp_magnitude(self, max_length):
        """Clamp the vector's magnitude to a maximum length."""
        mag = self.magnitude()
        if mag > max_length:
            return self.normalize() * max_length
        return _Vector2(self.x, self.y)

    def lerp(self, other, t):
        """Linearly interpolate between this vector and another.

        Args:
            other (_Vector2): Target vector.
            t (float): Interpolation factor (0.0 to 1.0).

        Returns:
            _Vector2: Interpolated vector.
        """
        return _Vector2(
            self.x + (other.x - self.x) * t,
            self.y + (other.y - self.y) * t
        )

    def floor(self):
        """Return a vector with each component floored."""
        return _Vector2(math.floor(self.x), math.floor(self.y))

    def ceil(self):
        """Return a vector with each component ceiled."""
        return _Vector2(math.ceil(self.x), math.ceil(self.y))

    def round(self):
        """Return a vector with each component rounded."""
        return _Vector2(round(self.x), round(self.y))

    def abs(self):
        """Return a vector with absolute values."""
        return _Vector2(abs(self.x), abs(self.y))

    # ------------------------
    # Static Helpers
    # ------------------------

    @staticmethod
    def clamp_value(value, min_value, max_value):
        """Clamp a scalar value between min and max."""
        return max(min_value, min(value, max_value))