# coding=utf-8
from . import Vector2

class Contact(object):
    def __init__(self, normal, dist, p): #( n:Vector2, dist:Number, p:Vector2 ):void
        self.normal = normal
        self.dist = dist
        self.impulse = 0
        self.p = p
