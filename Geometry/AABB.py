# coding=utf-8
import pygame
import math
from .Vector2 import Vector2

class AABB(object):
    def __init__(self, center, half_extents):
        center = center
        half_extents = half_extents
        self.rect = pygame.Rect(center.x - half_extents.x, center.y - half_extents.y, (half_extents.x * 2),
                                (half_extents.y * 2))

    def set_rect(self, new_width, new_height):
        self.rect.center = (self.rect.center[0] - (new_width - self.rect.width), self.rect.center[1]
                            - (new_height - self.rect.height))
        self.rect.width = new_width
        self.rect.height = new_height

    def get_surface(self, color):
        self.aabb_surface = pygame.Surface((self.rect.width, self.rect.height))
        self.aabb_surface.fill(color)
        return self.aabb_surface
