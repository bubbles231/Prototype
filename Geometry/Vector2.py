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
    def __init__(self, x = 0, y = 0):
        self.x = x
        self.y = y

    def Add(self, vector):
        return Vector2(self.x + vector.x, self.y + vector.y)

    def AddTo(self, vector):
        self.x += vector.x
        self.y += vector.y

    def SubFrom(self, vector):
        self.x -= vector.x
        self.y -= vector.y

    def SubScalar(self, scalar):
        return Vector2(self.x - scalar, m_y - scalar)

    def AddScalar(self, scalar):
        return Vector2(self.x + scalar, self.y + scalar)

    def SubScalarFrom(self, scalar):
        self.x -= scalar
        self.y -= scalar

    def AddScalarTo(self, scalar):
        self.x += scalar
        self.y += scalar

    def AddX(self, x):
        return Vector2(self.x + x, self.y)

    def AddY(self, y):
        return Vector2(self.x, self.y + y)

    def SubX(self, x):
        return Vector2(self.x - x, self.y)

    def SubY(self, y):
        return Vector2(self.x, self.y - y)

    def AddXTo(self, x):
        self.x += x

    def AddYTo(self, y):
        self.y += y

    def SubXFrom(self, x):
        self.x -= x

    def SubYFrom(self, y):
        self.y -= y

    def Sub(self, vector):
        return Vector2(self.x - vector.x, self.y - vector.y)

    def Mul(self, vector):
        return Vector2(self.x * vector.x, self.y * vector.y)

    def MulTo(self, vector):
        self.x *= vector.x
        self.y *= vector.y

    def Div(self, vector):
        return Vector2(self.x / vector.x, self.y / vector.y)

    def MulScalar(self, scalar):
        return Vector2(self.x * scalar, self.y * scalar)

    def MulAddScalarTo(self, vector, scalar):
        self.x += vector.x * scalar
        self.y += vector.y * scalar

    def MulSubScalarTo(self, vector, scalar):
        self.x -= vector.x * scalar
        self.y -= vector.y * scalar

    def Dot(self, vector):
        return self.x * vector.x + self.y * vector.y

    def get_LenSqr(self):
        return Dot(self)

    def get_Len(self):
        return math.sqrt(self.get_LenSqr)

    def get_Abs(self):
        return Vector2(abs(self.x), abs(self.y))

    def get_Unit(self):
        invLen = 1.0 / self.get_Len
        return MulScalar(invLen)

    def get_Floor(self):
        return Vector2(math.floor(self.x), math.floor(self.y))

    def Clamp(self, min_vector, max_vector):
        return Vector2(
            max( min(self.x, max_vector.x), min_vector.x),
            max( min(self.y, max_vector.y), min_vector.y)
        )

    def ClampInto(self, min_vector, max_vector):
        self.x = max( min(self.x, max_vector.x), min_vector.x)
        self.y = max( min(self.y, max_vector.y), min_vector.y)

    def get_Perp(self):
        return Vector2( -self.x, self.y )

    def m_Neg(self):
        return Vector2( -self.x, -self.y )

    def NegTo(self):
        self.x = -self.x
        self.y = -self.y

    def Equal(self, vector):
        return self.x == vector.x and self.y == vector.y

    @staticmethod
    def FromAngle(angle):
        return Vector2(math.cos(angle), math.sin(angle))

    """
    def ToAngle(self):
        angle = math.atan2(self.x, self.y)

        #make the returned range 0 --> 2*PI
        if (angle < 0.0):
            angle += kTwoPi
        return angle
    """

    @staticmethod
    def RandomRadius(radius):
        return Vector2(
            random.randint() * 2 - 1,
            random.randint() * 2 - 1
            ).MulScalar( radius )

    @staticmethod
    def FromPoint(point):
        return Vector2(point.x, point.y)

    def get_Point(self):
        return Point(self.x, self.y)

    def Clear(self):
        self.x = self.y = 0

    def Clone(self):
        return Vector2(self.x, self.y)

    def __repr__(self):
        return self.toString()

    def toString(self):
        return "x=" + str(self.x) + " y=" + str(self.y)

    def CloneInto(self, vector):
        self.x = vector.x
        self.y = vector.y

    def MaxInto(self, vector):
        self.x = max(self.x, vector.x)
        self.y = max(self.y, vector.y)

    def MinInto(self, vector):
        self.x = min(self.x, vector.x)
        self.y = min(self.y, vector.y)

    """
    def Min(self, vector):
        return Vector2(self.x, self.y).MinInto(vector)

    """

    def Max(self, vector):
        return Vector2(self.x, self.y).MaxInto(vector)

    def AbsTo(self):
        self.x = abs(self.x)
        self.y = abs(self.y)

    def get_MajorAxis(self):
        if abs(self.x) > abs(self.y):
            return Vector2( Scalar().Sign(self.x), 0)
        else:
            return Vector2( 0, Scalar().Sign(self.y))
