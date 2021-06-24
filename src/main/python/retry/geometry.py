"""
"ReTry" (c) by Ignacio Slater M.
"ReTry" is licensed under a
Creative Commons Attribution 4.0 International License.
You should have received a copy of the license along with this
work. If not, see <https://creativecommons.org/licenses/by/4.0/>.
"""
import math

from matplotlib.patches import Circle, Rectangle


class GeoObject:
    """
    Base class for geometric objects.
    """


class Point(GeoObject):
    """
    Class to store a 2D point
    """

    def __init__(self, x: float, y: float):
        """
        Creates a new 2D point with coordinates (x, y)
        """
        self.x = x
        self.y = y

    # Methods for 'print'
    def __str__(self):
        return f"P({self.x},{self.y})"

    def __repr__(self):
        return f"P({self.x},{self.y})"

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.x == other.x and self.y == other.y

    def draw(self, ax):
        p = Circle((self.x, self.y), 0.2)
        ax.add_patch(p)

    # Distance between points
    def distance_to(self, point):
        valx = (self.x - point.x)
        valy = (self.y - point.y)

        return math.sqrt(valx * valx + valy * valy)


# Class to store a rectangle
class Rect(GeoObject):
    # The rectangle is always represented by the top-left and bottom-right points.
    # The constructor receives any two points and computes the top-left and bottom-right points.

    def __init__(self, point1, point2):
        minx = point1.x if point1.x < point2.x else point2.x
        maxx = point1.x if point1.x > point2.x else point2.x
        miny = point1.y if point1.y < point2.y else point2.y
        maxy = point1.y if point1.y > point2.y else point2.y

        self.topLeft = Point(minx, maxy)
        self.bottomRight = Point(maxx, miny)

    # Methods for 'print'
    def __str__(self):
        return f"R({self.topLeft.__str__()},{self.bottomRight.__str__()})"

    def draw(self, ax):
        p = Rectangle((self.topLeft.x, self.bottomRight.y), self.bottomRight.x - self.topLeft.x,
                      self.topLeft.y - self.bottomRight.y, fill=False)
        ax.add_patch(p)

    # Area of the rectangle
    def area(self):
        return max((self.bottomRight.x - self.topLeft.x) * (self.topLeft.y - self.bottomRight.y), 0)

    # Method to verify whether a point is inside a rectangle or not
    def is_point_in_rectangle(self, point):
        return point.x >= self.topLeft.x and point.x <= self.bottomRight.x and point.y >= \
               self.bottomRight.y and point.y <= self.topLeft.y

    # Method to verify if the given rectangle overlaps with this rectangle
    def has_overlap(self, rect):
        # If some of the rectangles is a line, there is no overlap
        if self.topLeft.x == self.bottomRight.x or self.topLeft.y == self.bottomRight.y or \
                rect.topLeft.x == rect.bottomRight.x or rect.topLeft.y == rect.bottomRight.y:
            return False

        if self.topLeft.x >= rect.bottomRight.x or rect.topLeft.x >= self.bottomRight.x:
            return False

        if self.topLeft.y <= rect.bottomRight.y or rect.topLeft.y <= self.bottomRight.y:
            return False

        return True

    # Method to compute the area increase of this rectangle to include the given rectangle
    def areaIncrease(self, rect):
        # Create container rectangle between self and rect
        minx = self.topLeft.x if self.topLeft.x < rect.topLeft.x else rect.topLeft.x
        maxx = self.bottomRight.x if self.bottomRight.x > rect.bottomRight.x else rect.bottomRight.x
        miny = self.bottomRight.y if self.bottomRight.y < rect.bottomRight.y else rect.bottomRight.y
        maxy = self.topLeft.y if self.topLeft.y > rect.topLeft.y else rect.topLeft.y

        return Rect(Point(minx, maxy), Point(maxx, miny)).area() - self.area()

    # Method to update a rectangle given a primitive: point or rect
    def updateRect(self, object):
        if isinstance(object, Point):
            if object.x < self.topLeft.x:
                self.topLeft.x = object.x
            if object.y > self.topLeft.y:
                self.topLeft.y = object.y
            if object.x > self.bottomRight.x:
                self.bottomRight.x = object.x
            if object.y < self.bottomRight.y:
                self.bottomRight.y = object.y
        elif isinstance(object, Rect):
            self.updateRect(object.topLeft)
            self.updateRect(object.bottomRight)

    # Method to compute the MINDIST between a point and this rectangle
    def mindist(self, point):
        dx = 0
        if point.x < self.topLeft.x:
            dx = (point.x - self.topLeft.x) ** 2
        elif point.x > self.bottomRight.x:
            dx = (point.x - self.bottomRight.x) ** 2

        dy = 0
        if point.y < self.bottomRight.y:
            dy = (point.y - self.bottomRight.y) ** 2
        elif point.y > self.topLeft.y:
            dy = (point.y - self.topLeft.y) ** 2

        return math.sqrt(dx + dy)

    def minmaxdist(self, point):
        # Taking into account X
        rmk = self.topLeft.x if point.x <= (
                (self.topLeft.x + self.bottomRight.x) / 2) else self.bottomRight.x
        rmi = self.bottomRight.y if point.y >= (
                (self.topLeft.y + self.bottomRight.y) / 2) else self.topLeft.y

        valx = math.sqrt((point.x - rmk) ** 2 + (point.y - rmi) ** 2)

        # Taking into account Y
        rmk = self.bottomRight.y if point.y <= (
                (self.topLeft.y + self.bottomRight.y) / 2) else self.topLeft.y
        rmi = self.topLeft.x if point.x >= (
                (self.topLeft.x + self.bottomRight.x) / 2) else self.bottomRight.x

        valy = math.sqrt((point.y - rmk) ** 2 + (point.x - rmi) ** 2)

        return min(valx, valy)
