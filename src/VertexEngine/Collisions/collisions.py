import math

class Collider:
    """Base class for all colliders"""
    def collides_with(self, other):
        """Polymorphic collision detection"""
        method_name = f"_collides_with_{type(other).__name__.lower()}"
        if hasattr(self, method_name):
            return getattr(self, method_name)(other)
        # fallback: try the other object
        method_name = f"_collides_with_{type(self).__name__.lower()}"
        if hasattr(other, method_name):
            return getattr(other, method_name)(self)
        raise NotImplementedError(f"Collision not implemented between {type(self)} and {type(other)}")
    
class Polygon(Collider):
    """Polygon collider allows you to draw a collider between 3 and 4 points."""
    def __init__(self, points):
        assert 3 <= len(points) <= 4, "Only triangles and quads supported"
        self.points = points

    def _edges(self):
        return [(self.points[i], self.points[(i+1) % len(self.points)]) for i in range(len(self.points))]

    def _normals(self):
        normals = []
        for p1, p2 in self._edges():
            edge = (p2[0]-p1[0], p2[1]-p1[1])
            normal = (-edge[1], edge[0])
            length = math.hypot(*normal)
            normals.append((normal[0]/length, normal[1]/length))
        return normals

    def _project_onto_axis(self, axis):
        dots = [pt[0]*axis[0] + pt[1]*axis[1] for pt in self.points]
        return min(dots), max(dots)

    def _collides_with_polygon(self, other):
        axes = self._normals() + other._normals()
        for axis in axes:
            min1, max1 = self._project_onto_axis(axis)
            min2, max2 = other._project_onto_axis(axis)
            if max1 < min2 or max2 < min1:
                return False
        return True

    def _collides_with_circle(self, circle):
        for i in range(len(self.points)):
            p1, p2 = self.points[i], self.points[(i+1) % len(self.points)]
            # Closest point on edge to circle center
            dx, dy = p2[0]-p1[0], p2[1]-p1[1]
            t = max(0, min(1, ((circle.x - p1[0])*dx + (circle.y - p1[1])*dy)/(dx*dx + dy*dy)))
            closest = (p1[0] + t*dx, p1[1] + t*dy)
            dist_sq = (circle.x - closest[0])**2 + (circle.y - closest[1])**2
            if dist_sq <= circle.radius**2:
                return True
        # Also check if circle inside polygon
        if self._point_inside(circle.x, circle.y):
            return True
        return False

    def _point_inside(self, px, py):
        # Ray-casting algorithm
        inside = False
        n = len(self.points)
        xints = 0
        p1x, p1y = self.points[0]
        for i in range(n+1):
            p2x, p2y = self.points[i % n]
            if py > min(p1y,p2y):
                if py <= max(p1y,p2y):
                    if px <= max(p1x,p2x):
                        if p1y != p2y:
                            xints = (py-p1y)*(p2x-p1x)/(p2y-p1y)+p1x
                        if p1x == p2x or px <= xints:
                            inside = not inside
            p1x,p1y = p2x,p2y
        return inside
    
class Circle(Collider):
    """This is the collider for a circle.
    `x` is the x axis of the position of the collider
    `y` is the y axis of the position of the collider
    `radius` is the radius of the collider"""
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius

    def _collides_with_circle(self, other):
        dx = self.x - other.x
        dy = self.y - other.y
        distance_sq = dx*dx + dy*dy
        radius_sum = self.radius + other.radius
        return distance_sq <= radius_sum * radius_sum

    def _collides_with_rotatedcollider(self, rect):
        # Approximate rectangle as polygon for SAT
        poly = Polygon(rect.get_corners())
        return poly._collides_with_circle(self)
    
class RotatedCollider(Collider):
    """This is an `ACCURATE HITBOX` for more advanced collisions.
    This is a rect collider, as it's simpler.
    The reason I can't do polygons like triangles because it uses more cpu and gpu to calculate the points, as you have to take in rotation matrices, and more."""
    def __init__(self, x, y, width, height, angle=0):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.angle = angle  # in degrees

    def get_corners(self):
        cx, cy = self.x, self.y
        w, h = self.width/2, self.height/2
        rad = math.radians(self.angle)
        cos_a, sin_a = math.cos(rad), math.sin(rad)
        corners = []
        for dx, dy in [(-w, -h), (w, -h), (w, h), (-w, h)]:
            x_rot = cx + dx * cos_a - dy * sin_a
            y_rot = cy + dx * sin_a + dy * cos_a
            corners.append((x_rot, y_rot))
        return corners

    def _collides_with_rotatedcollider(self, other):
        poly1 = Polygon(self.get_corners())
        poly2 = Polygon(other.get_corners())
        return poly1._collides_with_polygon(poly2)

    def _collides_with_circle(self, circle):
        poly = Polygon(self.get_corners())
        return poly._collides_with_circle(circle)
    