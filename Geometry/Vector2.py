# coding=utf-8
import random
import math
from .Scalar import Scalar


class Vector2(object):
    """
    THIS WILL BE A TRANSLATION OF A VECTOR2 FUNCTION
    BECAUSE I DONT LIKE THE PYGAME MATH VERSION,
    I WILL ADD ALL THE METHODS TO IT
    """

    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def add(self, vector):
        return Vector2(self.x + vector.x, self.y + vector.y)

    def add_to(self, vector):
        self.x += vector.x
        self.y += vector.y

    def sub_from(self, vector):
        self.x -= vector.x
        self.y -= vector.y

    def add_scalar(self, scalar):
        return Vector2(self.x + scalar, self.y + scalar)

    def sub_scalar_from(self, scalar):
        self.x -= scalar
        self.y -= scalar

    def add_scalar_to(self, scalar):
        self.x += scalar
        self.y += scalar

    def add_x(self, x):
        return Vector2(self.x + x, self.y)

    def add_y(self, y):
        return Vector2(self.x, self.y + y)

    def sub_x(self, x):
        return Vector2(self.x - x, self.y)

    def sub_y(self, y):
        return Vector2(self.x, self.y - y)

    def add_x_to(self, x):
        self.x += x

    def add_y_to(self, y):
        self.y += y

    def sub_x_from(self, x):
        self.x -= x

    def sub_y_from(self, y):
        self.y -= y

    def sub(self, vector):
        return Vector2(self.x - vector.x, self.y - vector.y)

    def mul(self, vector):
        return Vector2(self.x * vector.x, self.y * vector.y)

    def mul_to(self, vector):
        self.x *= vector.x
        self.y *= vector.y

    def div(self, vector):
        return Vector2(self.x / vector.x, self.y / vector.y)

    def mul_scalar(self, scalar):
        return Vector2(self.x * scalar, self.y * scalar)

    def mul_add_scalar_to(self, vector, scalar):
        self.x += vector.x * scalar
        self.y += vector.y * scalar

    def mul_sub_scalar_to(self, vector, scalar):
        self.x -= vector.x * scalar
        self.y -= vector.y * scalar

    def dot(self, vector):
        return self.x * vector.x + self.y * vector.y

    def get_len(self):
        return math.sqrt(self.get_len_sqr)

    def get_abs(self):
        return Vector2(abs(self.x), abs(self.y))

    def get_floor(self):
        return Vector2(int(math.floor(self.x)), int(math.floor(self.y)))

    def clamp(self, min_vector, max_vector):
        return Vector2(
            max(min(self.x, max_vector.x), min_vector.x),
            max(min(self.y, max_vector.y), min_vector.y))

    def clamp_into(self, min_vector, max_vector):
        self.x = max(min(self.x, max_vector.x), min_vector.x)
        self.y = max(min(self.y, max_vector.y), min_vector.y)

    def get_perp(self):
        return Vector2(-self.x, self.y)

    def m_neg(self):
        return Vector2(-self.x, -self.y)

    def neg_to(self):
        self.x = -self.x
        self.y = -self.y

    def equal(self, vector):
        return self.x == vector.x and self.y == vector.y

    @staticmethod
    def from_angle(angle):
        return Vector2(math.cos(angle), math.sin(angle))

    @staticmethod
    def random_radius(radius):
        return Vector2(
            random.randint() * 2 - 1,
            random.randint() * 2 - 1
        ).mul_scalar(radius)

    @staticmethod
    def from_point(point):
        return Vector2(point.x, point.y)

    def clear(self):
        self.x = self.y = 0

    def clone(self):
        return Vector2(self.x, self.y)

    def __repr__(self):
        return self.to_string()

    def to_string(self):
        return "x=" + str(self.x) + " y=" + str(self.y)

    def clone_into(self, vector):
        self.x = vector.x
        self.y = vector.y

    def max_into(self, vector):
        self.x = max(self.x, vector.x)
        self.y = max(self.y, vector.y)

    def min_into(self, vector):
        self.x = min(self.x, vector.x)
        self.y = min(self.y, vector.y)

    def max(self, vector):
        return Vector2(self.x, self.y).max_into(vector)

    def abs_to(self):
        self.x = abs(self.x)
        self.y = abs(self.y)

    def get_major_axis(self):
        if abs(self.x) > abs(self.y):
            return Vector2(Scalar().sign(self.x), 0)
        else:
            return Vector2(0, Scalar().sign(self.y))
