# coding=utf-8
import random
import math


class Scalar(object):
    """WRITING MY OWN SCALAR CLASS WITH METHODS"""
    def __init__(self):
        self.kMaxRandValue = 65535

    @staticmethod
    def frac(number):
        absolute = abs(number)
        return absolute - math.floor(absolute)

    @staticmethod
    def ease_out(x):
        a = x - 1
        return a * a * a + 1

    @staticmethod
    def ease_out_vel(x):
        a = x - 1
        return a * a * 3

    @staticmethod
    def rand_between(a, b):
        return random.randint() * (b - a) + a

    def rand_int(self):
        return int(random.randint() * self.kMaxRandValue)

    @staticmethod
    def infinity_curve(number):
        return -1 / (number + 1) + 1

    @staticmethod
    def clamp(a, min_vector, max_vector):
        a = max(min_vector, a)
        a = min(max_vector, a)
        return a

    @staticmethod
    def sign(a):
        if a > 0:
            return 1
        elif a < 0:
            return -1
        else:
            return 0
