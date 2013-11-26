# coding=utf-8
import random
import math

class Scalar(object):
    """WRITING MY OWN SCALAR CLASS WITH METHODS"""
    def __init__(self):
        self.kMaxRandValue = 65535

    @staticmethod
    def Frac(number):
        absolute = abs(number)
        return absolute - math.floor(absolute)

    @staticmethod
    def Wrap(x, my_range):
        t = x / my_range
        ft = Frac(t)
        return my_range * ft

    @staticmethod
    def EaseOut(x):
        a = x -1
        return a * a * a + 1

    @staticmethod
    def EaseOutVel(x):
        a = x -1
        return a * a * 3

    @staticmethod
    def RandBetween(a, b):
        return random.randint() * (b - a) + a

    @staticmethod
    def RandBetweenInt(a, b):
        return int(RandBetween(a, b))

    """
    def RandUint(self):
        return uint(random.randint() * self.kMaxRandValue)
    """

    def RandInt(self):
        return int(random.randint() * self.kMaxRandValue)

    """
    def FromVector2(self, vector):
        return math.atan2(vector.x, vector.y)
    """

    @staticmethod
    def InfinityCurve(number):
        return -1 / (x + 1) + 1

    @staticmethod
    def Clamp(a, min_vector, max_vector):
        a = max(min_vector, a)
        a = min(max_vector, a)
        return a

    @staticmethod
    def Sign(a):
        if a > 0:
            return 1
        elif a < 0:
            return -1
        else:
            return 0
