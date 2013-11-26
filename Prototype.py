#!/usr/bin/env python3
# coding=utf-8

__version__ = '$Id: Prototype.py v0.0.2$'
__author__ = 'bubbles231'

__doc__ = """ Prototype.py - A collision detection prototype for MarioQuest.

Prototype is going to try to make a reusable version of the Tile Base (Smooth) collision detection:

    1. It should do everything as instructed at
       http://higherorderfun.com/blog/2012/05/20/the-guide-to-implementing-2d-platformers/
       for Tile Base (Smooth)
    2. It will be easy to use in MarioQuest and modify to fit the game
    3. It will have the detection and resolution of collisions
    4. It will handle slopes, moving platforms, and maybe some other things

Make sure to keep the code clean, reusable, and magic numbers will be explained/labeled with a comment and
eventually replace them.
"""

import pygame
import sys
from Geometry.Vector2 import *

FPS = 1000/15


class TileSet(object):
    """

    TileSet() stores a 2d array of Tile()s and has some other tilemap information.

    Attributes:
        self.example: An example attribute that is made up
    """

    def __init__(self, level, screen, tile_size):
        self.tile_size = tile_size
        # self.tile_rect = pygame.Rect(0, 0, tile_size.x, tile_size.y)
        self.debug_screen = screen  # TODO: REMOVE AS SOON AS DONE DEBUGGING
        self.debug_img = pygame.Surface((self.tile_size.x, self.tile_size.y))
        self.debug_img.fill((255, 0, 0))

        self.map_size = Vector2(len(level[0]), len(level))
        self.image = pygame.Surface((self.map_size.x * self.tile_size.x, self.map_size.y * self.tile_size.y),
                                    pygame.SRCALPHA)
        self.tile_array = {}
        for x in range(0, self.map_size.x):
            for y in range(0, self.map_size.y):
                self.tile_array[x, y] = self.make_tile(level[y][x], x * self.tile_size.x, y * self.tile_size.y,
                                                       self.tile_size)
        self.draw()

    @staticmethod
    def make_tile(tile_id, tx, ty, tile_size):
        """

        @type tile_id: int
        @type tx: int
        @type ty: int
        @param tile_size:
        @return:
        """
        if tile_id == 0:
            return Tile(tx, ty, True, tile_size.x, tile_size.y, (125, 199, 245))
        elif tile_id == 1:
            return Tile(tx, ty, False, tile_size.x, tile_size.y, (150, 79, 35))
        elif tile_id == 2:
            return Tile(tx, ty, False, tile_size.x, tile_size.y, (245, 208, 0))
        elif tile_id == 3:
            return Tile(tx, ty, False, tile_size.x, tile_size.y, (0, 247, 0))

    def draw(self):
        """

        The draw() function is called in the main game loop and draws the stuff in this class.
        """
        for x in range(0, self.map_size.x):
            for y in range(0, self.map_size.y):
                tmp_tile = self.tile_array[x, y]
                self.image.blit(tmp_tile.image, (x * tmp_tile.tile_size.x, y * tmp_tile.tile_size.y))

    def scan_x_right(self, y, tile_x):
        """

        @type y: int
        @type tile_x: int
        @return:
        """
        solid_tile_list = []
        for x in range(tile_x - 1, self.map_size.x):  # TODO: find out why - 1 makes it work
            tmp_tile = self.tile_array[x, y]
            if not tmp_tile.walkable:
                solid_tile_list.append(tmp_tile)
                # print("scan_x_right")
                self.debug_screen.blit(self.debug_img, (tmp_tile.rect.x, tmp_tile.rect.y))
        return solid_tile_list

    def scan_x_left(self, y, tile_x):
        """

        @type y: int
        @type tile_x: int
        @return:
        """
        solid_tile_list = []
        for x in range(tile_x, -1, -1):
            tmp_tile = self.tile_array[x, y]
            if not tmp_tile.walkable:
                solid_tile_list.append(tmp_tile)
                # print("scan_x_right")
                self.debug_screen.blit(self.debug_img, (tmp_tile.rect.x, tmp_tile.rect.y))
        return solid_tile_list

    def scan_y_bottom(self, x, tile_y):
        """

        @type x: int
        @type tile_y: int
        @return:
        """
        solid_tile_list = []
        for y in range(tile_y - 1, self.map_size.y):
            tmp_tile = self.tile_array[x, y]
            if not tmp_tile.walkable:
                solid_tile_list.append(tmp_tile)
                # print("scan_y_bottom")
                self.debug_screen.blit(self.debug_img, (tmp_tile.rect.x, tmp_tile.rect.y))
        return solid_tile_list

    def scan_y_top(self, x, tile_y):
        """

        @type x: int
        @type tile_y: int
        @return:
        """
        solid_tile_list = []
        for y in range(tile_y, -1, -1):
            tmp_tile = self.tile_array[x, y]
            if not tmp_tile.walkable:
                solid_tile_list.append(tmp_tile)
                # print("scan_y_top")
                self.debug_screen.blit(self.debug_img, (tmp_tile.rect.x, tmp_tile.rect.y))
        return solid_tile_list

class Entity(pygame.sprite.Sprite):
    """

    Entity() is a parent class which will have Children like Player, MovingPlatform, and Tile.

    Attributes:
        self.
    """

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

class Tile(Entity):
    """

    @type x: int
    @type y: int
    @type walkable: bool
    @type width: int
    @type height: int
    @type color: tuple
    """

    def __init__(self, x, y, walkable, width, height, color):
        Entity.__init__(self)
        self.walkable = walkable
        self.tile_size = Vector2(width, height)
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        if color is not None:
            self.image.fill(color)

class MovingPlatform(Entity):

    """

    @type width: int
    @type height: int
    @type range_x: tuple
    @type range_y: tuple
    """

    def __init__(self, width, height, range_x, range_y, color):
        Entity.__init__(self)
        self.range_x = Vector2(range_x[0], range_x[1])
        self.range_y = Vector2(range_y[0], range_y[1])
        self.rect = pygame.Rect(range_x[0], range_y[0], width, height)
        self.image = pygame.Surface((width, height))
        self.image.fill(color)
        self.velocity = Vector2(0, 0)
        self.strait = Vector2(3, 1)  # preset velocity TODO: Use tilemap to determine path and velocity.
        self.normal = Vector2(0, 0)
        self.moving = True

    def update(self):
        """

        The update() will update the position and velocity.
        """
        if self.rect.left <= self.range_x.x:
            self.normal.x = 1
        elif self.rect.right >= self.range_x.y:
            self.normal.x = -1
        if self.rect.bottom <= self.range_y.x:
            self.normal.y = 1
        elif self.rect.top >= self.range_y.y:
            self.normal.y = -1

        self.velocity.x = self.strait.x * self.normal.x
        self.velocity.y = self.strait.y * self.normal.y
        self.rect.x += self.velocity.x
        self.rect.y += self.velocity.y

    def draw(self, screen):
        """

        @type screen: pygame.Surface
        """
        screen.blit(self.image, (self.rect.x, self.rect.y))


class Player(Entity):

    """

    @type x: int
    @type y: int
    @type width: int
    @type length: int
    @type color: tuple
    """

    def __init__(self, x, y, width, length, color, screen):
        Entity.__init__(self)
        self.rect = pygame.Rect(x, y, width, length)
        self.image = pygame.Surface((self.rect.width, self.rect.height))
        self.image.fill(color)
        self.velocity = Vector2(x, y)
        self.forward_edge_coord = Vector2()
        self.on_ground = False
        self.normal = Vector2(0, 0)
        self.tile = Vector2(0, 0)

        self.debug_screen = screen  # TODO: REMOVE AS SOON AS DONE DEBUGGING

    def update(self, tileset, moving_platforms):
        """

        @param moving_platforms:
        @type tileset: Prototype.TileSet
        """
        if self.velocity.x > 0:
            self.normal.x = 1
            self.forward_edge_coord.x = self.rect.right
        elif self.velocity.x < 0:
            self.normal.x = -1
            self.forward_edge_coord.x = self.rect.left
        elif self.velocity.x == 0:
            self.normal.x = 0
            self.forward_edge_coord.x = None

        if self.velocity.y > 0:
            self.normal.y = 1
            self.forward_edge_coord.y = self.rect.bottom
        elif self.velocity.y < 0:
            self.normal.y = -1
            self.forward_edge_coord.y = self.rect.top
        elif self.velocity.y == 0:
            self.normal.y = 0
            self.forward_edge_coord.y = None

        if self.normal.x != 0:
            tiles_to_check = self.scan_x(tileset)
            close_tile = self.find_closest_x(tiles_to_check, self.normal.x)
            close_moving = self.get_moving_stuff_x(moving_platforms, tileset)
            if close_tile is not None:
                # print("close X", close_tile.rect.x)
                self.react_x(close_tile)
            else:
                self.rect.x += self.velocity.x
            # if close_tile is not None and close_moving is not None:
            #     if abs(self.rect.centerx - close_tile.rect.centerx) <= abs(self.rect.centerx -
            #                                                                close_moving.rect.centerx):
            #         self.react_y(close_tile)
            #     else:
            #         self.react_y(close_moving)
            # elif close_tile is not None and close_moving is None:
            #     self.react_x(close_tile)
            # elif close_tile is None and close_moving is not None:
            #     self.react_x(close_moving)
            # else:
            #     print("close tile x", close_tile, "close moving x", close_moving)
            #     self.rect.x += self.velocity.x

        if self.normal.y != 0:
            tiles_to_check = self.scan_y(tileset)
            close_tile = self.find_closest_y(tiles_to_check, self.normal.y)
            close_moving = self.get_moving_stuff_y(moving_platforms, tileset)
            if close_tile is not None:
                # print("close Y", close_tile.rect.y)
                self.react_y(close_tile)
            else:
                self.rect.y += self.velocity.y
            # if close_tile is not None and close_moving is not None:
            #     if abs(self.rect.centery - close_tile.rect.centery) <= abs(self.rect.centery -
            #                                                                close_moving.rect.centery):
            #         self.react_y(close_tile)
            #     else:
            #         self.react_y(close_moving)
            # elif close_tile is not None and close_moving is None:
            #     self.react_y(close_tile)
            # elif close_tile is None and close_moving is not None:
            #     self.react_y(close_moving)
            # else:
            #     print("close tile y", close_tile, "close moving y", close_moving)
            #     self.rect.y += self.velocity.y

        self.velocity.x = 0
        self.velocity.y = 0

    def get_moving_stuff_x(self, moving_platforms, tileset):
        """

        @param moving_platforms:
        @param tileset:
        @return:
        """
        closest = None
        for platform in moving_platforms:
            player_intersecting = get_intersecting_y(self.rect, tileset.tile_array[0, 0].rect)
            platform_intersecting = get_intersecting_y(platform.rect, tileset.tile_array[0, 0].rect)
            if player_intersecting[0] >= platform_intersecting[0] and player_intersecting[1] <= platform_intersecting[1]:
                # print("#! player intersects !#")
                distance_from_self = 10000000
                if abs(platform.rect.centerx - self.rect.centerx) < distance_from_self:
                    closest = platform
                    distance_from_self = abs(platform.rect.centerx - self.rect.centerx)
            if closest is not None:
                if self.normal.x > 0 and self.rect.centerx < platform.rect.centerx:
                    closest_img = pygame.Surface((closest.rect.width, closest.rect.height))
                    closest_img.fill((0, 100, 255))
                    self.debug_screen.blit(closest_img, (closest.rect.x, closest.rect.y))
                elif self.normal.x < 0 and self.rect.centerx > platform.rect.centerx:
                    closest_img = pygame.Surface((closest.rect.width, closest.rect.height))
                    closest_img.fill((0, 100, 255))
                    self.debug_screen.blit(closest_img, (closest.rect.x, closest.rect.y))
        return closest

    def get_moving_stuff_y(self, moving_platforms, tileset):
        """

        @param moving_platforms:
        @param tileset:
        @return:
        """
        closest = None
        for platform in moving_platforms:
            player_intersecting = get_intersecting_x(self.rect, tileset.tile_array[0, 0].rect)
            platform_intersecting = get_intersecting_x(platform.rect, tileset.tile_array[0, 0].rect)
            if player_intersecting[0] >= platform_intersecting[0] and player_intersecting[1] <= platform_intersecting[1]:
                # print("#! player intersects !#")
                distance_from_self = 10000000
                if abs(platform.rect.centery - self.rect.centery) < distance_from_self:
                    closest = platform
                    distance_from_self = abs(platform.rect.centery - self.rect.centery)
            if closest is not None:
                if self.normal.y > 0 and self.rect.centery < platform.rect.centery:
                    closest_img = pygame.Surface((closest.rect.width, closest.rect.height))
                    closest_img.fill((0, 100, 255))
                    self.debug_screen.blit(closest_img, (closest.rect.x, closest.rect.y))
                elif self.normal.y < 0 and self.rect.centery > platform.rect.centery:
                    closest_img = pygame.Surface((closest.rect.width, closest.rect.height))
                    closest_img.fill((0, 100, 255))
                    self.debug_screen.blit(closest_img, (closest.rect.x, closest.rect.y))
        return closest

    def scan_x(self, tileset):
        """

        @type tileset: Prototype.TileSet
        """
        all_tiles = []
        intersecting_range = get_intersecting_y(self.rect, tileset.tile_array[0, 0].rect)
        print("range x", intersecting_range)
        if self.normal.x > 0:  # moving right
            # print("moving right")
            for i in range(intersecting_range[0], intersecting_range[1]):
                tmp_tile_list = tileset.scan_x_right(i, (self.forward_edge_coord.x // tileset.tile_size.x) + 1)
                all_tiles.append(tmp_tile_list)
                # print("right i:", i)
        else:
            # print("moving left")
            for i in range(intersecting_range[0], intersecting_range[1]):
                tmp_tile_list = tileset.scan_x_left(i, (self.forward_edge_coord.x // tileset.tile_size.x) - 1)
                all_tiles.append(tmp_tile_list)
                # print("left i:", i)
        return all_tiles

    def scan_y(self, tileset):
        """

        @type tileset: Prototype.TileSet
        """
        all_tiles = []
        intersecting_range = get_intersecting_x(self.rect, tileset.tile_array[0, 0].rect)
        print("range y", intersecting_range)
        if self.normal.y > 0:
            # print("moving down")
            for i in range(intersecting_range[0], intersecting_range[1]):
                tmp_tile_list = tileset.scan_y_bottom(i, (self.forward_edge_coord.y // tileset.tile_size.y) + 1)
                all_tiles.append(tmp_tile_list)
                # print("down i:", i)
        else:
            # print("moving up")
            for i in range(intersecting_range[0], intersecting_range[1]):
                tmp_tile_list = tileset.scan_y_top(i, (self.forward_edge_coord.y // tileset.tile_size.y) - 1)
                all_tiles.append(tmp_tile_list)
                # print("top i:", i)
        return all_tiles

    def find_closest_x(self, tiles_to_check, normal):
        # print(tiles_to_check)
        """

        @type tiles_to_check: list
        @type normal: int
        @return:
        """
        distance_from_self = 1000000
        closest = None
        for i in tiles_to_check:
            for tmp_tile in i:
                if abs(tmp_tile.rect.centerx - self.rect.centerx) < distance_from_self:
                    closest = tmp_tile
                    distance_from_self = abs(tmp_tile.rect.centerx - self.rect.centerx)
        # print("CLOSEST:", closest, distance_from_self)
        if closest is not None:
            closest_img = pygame.Surface((closest.rect.width, closest.rect.height))
            closest_img.fill((0, 100, 255))
            self.debug_screen.blit(closest_img, (closest.rect.x, closest.rect.y))
        return closest

    def find_closest_y(self, tiles_to_check, normal):
        # print(tiles_to_check)
        """

        @type tiles_to_check: list
        @type normal: int
        @return:
        """
        distance_from_self = 1000000
        closest = None
        for i in tiles_to_check:
            for tmp_tile in i:
                if abs(tmp_tile.rect.centery - self.rect.centery) < distance_from_self:
                    closest = tmp_tile
                    distance_from_self = abs(tmp_tile.rect.centery - self.rect.centery)

        # print("CLOSEST:", closest, distance_from_self)
        if closest is not None:
            closest_img = pygame.Surface((closest.rect.width, closest.rect.height))
            closest_img.fill((0, 100, 255))
            self.debug_screen.blit(closest_img, (closest.rect.x, closest.rect.y))
        return closest

    def react_x(self, close_tile):
        """

        @type close_tile: Prototype.Tile
        """
        # print(close_tile.rect, self.rect.right)
        if self.normal.x > 0:
            if (self.rect.right + self.velocity.x) <= close_tile.rect.left:
                # print("going right and not past close_rect")
                self.rect.right += self.velocity.x
            else:
                self.rect.right = close_tile.rect.left
        else:
            if (self.rect.left + self.velocity.x) >= close_tile.rect.right:
                # print("going left and not past close_rect")
                self.rect.left += self.velocity.x
            else:
                self.rect.left = close_tile.rect.right

    def react_y(self, close_tile):
        """

        @type close_tile: Prototype.Tile
        """
        # print(close_tile.rect.top, "my bottom:", self.rect.bottom)
        if self.normal.y > 0:
            if (self.rect.bottom + self.velocity.y) <= close_tile.rect.top:
                # print("going down and not past close_tile")
                self.rect.bottom += self.velocity.y
            else:
                self.rect.bottom = close_tile.rect.top
        else:
            if (self.rect.top + self.velocity.y) >= close_tile.rect.bottom:
                self.rect.top += self.velocity.y
            else:
                self.rect.top = close_tile.rect.bottom

    def draw(self, screen):
        """

        @type screen: pygame.Surface
        """
        screen.blit(self.image, (self.rect.x, self.rect.y))


def get_intersecting_x(rect1, rect2):
    """

    @param rect2:
    @param rect1:
    @return:
    """
    # tile_left = self.rect.left // tileset.tile_size.x
    # tile_left = math.floor(rect1.left / rect2.width)
    tile_left = math.floor(rect1.left / rect2.width)
    # tile_right = self.rect.right // tileset.tile_size.x
    tile_right = math.ceil(rect1.right / rect2.height/2)
    intersecting_range = (tile_left, tile_right)
    return intersecting_range

def get_intersecting_y(rect1, rect2):
    """

    @param rect2:
    @param rect1:
    @return:
    """
    # tile_top = self.rect.top // tileset.tile_size.y
    tile_top = math.floor(rect1.top / rect2.width*2)
    # tile_bottom = self.rect.bottom // tileset.tile_size.y
    ### tile_bottom = math.ceil(rect1.bottom / rect2.height
    tile_bottom = math.ceil(rect1.bottom / rect2.height)
    intersecting_range = (tile_top, tile_bottom)
    return intersecting_range

def main():
    """

    The main() is where the main game loop is.
    First initialize stuff then run main game loop.
    """
    screen = pygame.display.set_mode((800, 640))
    clock = pygame.time.Clock()

    tw_1 = 64
    th_1 = 32
    my_tiles_1 = [[1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                  [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]
    tile_size_1 = Vector2(tw_1, th_1)
    tileset_1 = TileSet(my_tiles_1, screen, tile_size_1)

    tw_2 = 64
    th_2 = 64
    my_tiles_2 = [[0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0],
                  [0, 1, 1, 0, 0, 0]]

    tile_size_2 = Vector2(tw_2, th_2)
    tileset_2 = TileSet(my_tiles_2, screen, tile_size_2)

    tileset_group = pygame.sprite.Group()

    # player = Player(32, 32, 32, 64, (255, 255, 255), screen)
    player = Player(tw_1, th_1, 20, 50, (0, 255, 0), screen)
    moving_platform_1 = MovingPlatform(100, 20, (1 * tile_size_1.x, 15 * tile_size_1.y),
                                      (5 * tile_size_1.x, 6 * tile_size_1.y), (150, 50, 255))
    moving_platform_2 = MovingPlatform(32, 32, (1 * tile_size_1.x, 15 * tile_size_1.y),
                                      (15 * tile_size_1.x, 16 * tile_size_1.y), (100, 0, 0))
    platforms_group = pygame.sprite.Group()
    platforms_group.add(moving_platform_1)
    platforms_group.add(moving_platform_2)

    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT or e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            player.velocity.y -= 4
        if keys[pygame.K_DOWN]:
            player.velocity.y += 4
        if keys[pygame.K_LEFT]:
            player.velocity.x -= 4
        if keys[pygame.K_RIGHT]:
            player.velocity.x += 4

        screen.fill((10, 10, 10))
        screen.blit(tileset_1.image, (0, 0))
        # screen.blit(tileset_2.image, (0, 0))
        platforms_group.update()
        platforms_group.draw(screen)
        player.update(tileset_1, platforms_group)
        player.draw(screen)
        pygame.display.update()
        clock.tick(FPS)


if __name__ == "__main__":
    main()
