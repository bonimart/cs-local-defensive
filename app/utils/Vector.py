import math


class Vector:
    class NullVectorException(Exception):
        """The operation is not defined for null vector"""
        pass

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __iadd__(self, other):
        self = self + other
        return self

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        return Vector(self.x * other, self.y * other)

    def __truediv__(self, other):
        return Vector(self.x / other, self.y / other)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def distance(self, other) -> float:
        """Method for calculating distance between two vectors

        Args:
            other (Vector): other vector

        Returns:
            float: distance
        """
        return math.sqrt((self.x - other.x)**2 + (self.y - other.y)**2)

    def norm(self) -> float:
        """Method for norm calculation

        Returns:
            float: Norm of self
        """
        return math.sqrt(self.x**2 + self.y**2)

    def normalize(self):
        """Returns a normalized vector

        Returns:
            Vector: normalized vector
        """
        n = self.norm()
        return Vector(self.x, self.y) / (n + (n == 0))
