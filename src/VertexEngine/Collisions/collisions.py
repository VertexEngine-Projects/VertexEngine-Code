class Collider:
    """A collider is a rectangular area that can be used for collision detection. It has an x and y position, a width and height, and a method for checking if it collides with another collider.
    The method used is AABB (Axis-Aligned Bounding Box) collision detection, which checks if the rectangles of the two colliders overlap. If they do, then a collision has occurred.
    """
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def collides_with(self, other):
        """Checks if this collider collides with another collider. Returns True if they collide, False otherwise.
        Uses AABB method as explained in the docstring of the class.
        For fair collisions, make sure the hitbox (collider) is smaller than the actual sprite. This will make the game feel more responsive and less frustrating for the player.
        """
        return (
            self.x < other.x + other.width and
            self.x + self.width > other.x and
            self.y < other.y + other.height and
            self.y + self.height > other.y
        )
