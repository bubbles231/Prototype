#!/usr/bin/env python3
# coding=utf-8

__author__ = 'bubbles231'
__version__ = '0.0.3'
__status__ = 'Prototype'
__doc__ = """ Prototype.py - A collision detection prototype for MarioQuest. Run with ./Prototype.py.

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

import sys
from Geometry.Vector2 import Vector2
from Helpers import *

FPS = 1000/15


class TileSetsContainer(object):
    """

    @type tileset_list: list
    """

    def __init__(self, tileset_list):
        self.tileset_list = tileset_list
        self.tileset_order = {}
        for ts in tileset_list:
            ts.draw()
            self.tileset_order[ts.priority] = ts

    def draw(self, screen, camera):
        """

        @type screen: pygame.Surface
        @param camera:
        """
        for i in range(len(self.tileset_order) - 1, -1, -1):
            screen.blit(self.tileset_order[i].image, camera.apply(self.tileset_order[i]))


class TileSet(object):
    """

    TileSet() stores a 2d array of Tile()s and has some other tilemap information.

    Attributes:
        self.example: An example attribute that is made up
    """

    def __init__(self, level, screen, tile_size, priority):
        self.tile_size = tile_size
        self.map_size = Vector2(len(level[0]), len(level))
        self.image = pygame.Surface((self.map_size.x * self.tile_size.x, self.map_size.y * self.tile_size.y),
                                    pygame.SRCALPHA)
        self.rect = pygame.Rect(0, 0, self.map_size.x * self.tile_size.x, self.map_size.y * self.tile_size.y)
        self.tile_array = {}
        for x in range(0, self.map_size.x):
            for y in range(0, self.map_size.y):
                self.tile_array[x, y] = self.make_tile(level[y][x], x * self.tile_size.x, y * self.tile_size.y,
                                                       self.tile_size)
        self.priority = priority

        self.debug_screen = screen  # TODO: Make a program run with a debug switch instead of automatically debugging
        self.debug_img = pygame.Surface((self.tile_size.x, self.tile_size.y))
        self.debug_img.fill((255, 0, 0))
        self.not_considered_tiles = []

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
            return Tile(tx, ty, False, tile_size.x, tile_size.y, (0, 0, 0, 0))
        elif tile_id == 1:
            return Tile(tx, ty, True, tile_size.x, tile_size.y, (150, 79, 35))
        elif tile_id == 2:
            return Tile(tx, ty, True, tile_size.x, tile_size.y, (245, 208, 0))
        elif tile_id == 3:
            return Tile(tx, ty, True, tile_size.x, tile_size.y, (0, 247, 0))
        elif tile_id == 4:
            return Tile(tx, ty, True, tile_size.x, tile_size.y, (0, 100, 0))
        elif tile_id == 5:
            return Tile(tx, ty, False, tile_size.x, tile_size.y, (248, 144, 72))
        elif tile_id == 6:
            return Tile(tx, ty, False, tile_size.x, tile_size.y, (88, 200, 255))
        elif tile_id == 7:
            return Tile(tx, ty, False, tile_size.x, tile_size.y, (128, 184, 80))
        elif tile_id == 8:
            return Tile(tx, ty, False, tile_size.x, tile_size.y, (224, 224, 224))
        elif tile_id == 9:
            return Tile(tx, ty, True, tile_size.x, tile_size.y, 'data/Tiles/Slope/Left/frame752.png', [0, 32])
        elif tile_id == 10:
            return Tile(tx, ty,  True, tile_size.x, tile_size.y, 'data/Tiles/Slope/Left/frame818.png', [0, 32])
        elif tile_id == 11:
            return Tile(tx, ty,  True, tile_size.x, tile_size.y, 'data/Tiles/Slope/Left/frame877.png', [0, 16])
        elif tile_id == 12:
            return Tile(tx, ty, True, tile_size.x, tile_size.y, 'data/Tiles/Slope/Left/frame878.png', [17, 32])
        elif tile_id == 13:
            return Tile(tx, ty, True, tile_size.x, tile_size.y, 'data/Tiles/Slope/Right/frame750.png', [32, 0])
        elif tile_id == 14:
            return Tile(tx, ty,  True, tile_size.x, tile_size.y, 'data/Tiles/Slope/Right/frame815.png', [32, 0])
        elif tile_id == 15:
            return Tile(tx, ty,  True, tile_size.x, tile_size.y, 'data/Tiles/Slope/Right/frame707.png', [16, 0])
        elif tile_id == 16:
            return Tile(tx, ty, True, tile_size.x, tile_size.y, 'data/Tiles/Slope/Right/frame706.png', [32, 17])

    def draw(self):
        """
        Add Doc
        """
        for x in range(0, self.map_size.x):
            for y in range(0, self.map_size.y):
                tmp_tile = self.tile_array[x, y]
                self.image.blit(tmp_tile.image, (tmp_tile.rect.x, tmp_tile.rect.y))

    def scan_x_right(self, y, tile_x, entity):
        """


        @param entity:
        @type y: int
        @type tile_x: int
        @return:
        """
        solid_tile_list = []
        for x in range(tile_x - 1, self.map_size.x):
            try:
                tmp_tile = self.tile_array[x, y]
                if tmp_tile.solid:
                    if tmp_tile.slope:
                        solid_tile_list.append(tmp_tile)
                        if tmp_tile.adjacent_tile == 'left':
                            self.not_considered_tiles.append(self.tile_array[x-1, y])
                            pass
                        elif tmp_tile.adjacent_tile == 'right':
                            self.not_considered_tiles.append(self.tile_array[x+1, y])
                            pass
                        self.debug_screen.blit(self.debug_img, (tmp_tile.rect.x, tmp_tile.rect.y))
                    elif not tmp_tile.slope:
                        solid_tile_list.append(tmp_tile)
                        self.debug_screen.blit(self.debug_img, (tmp_tile.rect.x, tmp_tile.rect.y))
            except KeyError:
                print("scan_y_right: KeyError out of tileset bounds")
        return solid_tile_list

    def scan_x_left(self, y, tile_x, entity):
        """


        @param entity:
        @type y: int
        @type tile_x: int
        @return:
        """
        solid_tile_list = []
        for x in range(tile_x, -1, -1):
            try:
                tmp_tile = self.tile_array[x, y]
                if tmp_tile.solid:
                    if tmp_tile.slope:
                        solid_tile_list.append(tmp_tile)
                        if tmp_tile.adjacent_tile == 'left':
                            self.not_considered_tiles.append(self.tile_array[x-1, y])
                            pass
                        elif tmp_tile.adjacent_tile == 'right':
                            self.not_considered_tiles.append(self.tile_array[x+1, y])
                            pass
                        self.debug_screen.blit(self.debug_img, (tmp_tile.rect.x, tmp_tile.rect.y))
                    elif not tmp_tile.slope:
                        solid_tile_list.append(tmp_tile)
                        self.debug_screen.blit(self.debug_img, (tmp_tile.rect.x, tmp_tile.rect.y))

            except KeyError:
                print("scan_y_left: KeyError out of tileset bounds")
        return solid_tile_list

    def scan_y_bottom(self, x, tile_y, entity):
        """


        @param entity:
        @type x: int
        @type tile_y: int
        @return:
        """
        solid_tile_list = []
        for y in range(tile_y - 1, self.map_size.y):
            try:
                tmp_tile = self.tile_array[x, y]
                if tmp_tile.solid:
                    solid_tile_list.append(tmp_tile)
                    self.debug_screen.blit(self.debug_img, (tmp_tile.rect.x, tmp_tile.rect.y))
            except KeyError:
                print("scan_y_bottom: KeyError out of tileset bounds")
        return solid_tile_list

    def scan_y_top(self, x, tile_y, entity):
        """


        @param entity:
        @type x: int
        @type tile_y: int
        @return:
        """
        solid_tile_list = []
        for y in range(tile_y, -1, -1):
            try:
                tmp_tile = self.tile_array[x, y]
                if tmp_tile.solid:
                    solid_tile_list.append(tmp_tile)
                    self.debug_screen.blit(self.debug_img, (tmp_tile.rect.x, tmp_tile.rect.y))
            except KeyError:
                print("scan_y_top: KeyError out of tileset bounds")
        return solid_tile_list


class Entity(pygame.sprite.Sprite):
    """
    Entity() is a parent class which will have Children like Player, MovingPlatform, and Tile.
    """

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)


class Tile(Entity):
    """

    @type x: int
    @type y: int
    @type solid: bool
    @type width: int
    @type height: int
    """

    def __init__(self, x, y, solid, width, height, img_path, slope_coords=None):
        Entity.__init__(self)
        self.solid = solid
        self.rect = pygame.Rect(x, y, width, height)
        self.tile_coords = Vector2(x//width, y//height)
        self.image = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        if type(img_path) is tuple:
            self.image.fill(img_path)
        elif type(img_path) is str:
            self.image = pygame.image.load(img_path).convert_alpha()

        self.slope = False
        self.floor_y = None
        self.tall_edge = None
        self.short_edge = None
        self.adjacent_tile = False
        if slope_coords is not None:
            self.floor_y = Vector2(slope_coords[0], slope_coords[1])
            if slope_coords[0] > slope_coords[1]:
                self.tall_edge = self.rect.left
                self.short_edge = self.rect.right
            elif slope_coords[0] < slope_coords[1]:
                self.tall_edge = self.rect.right
                self.short_edge = self.rect.left
            if slope_coords[0] == 0:
                self.adjacent_tile = 'left'
            elif slope_coords[1] == 0:
                self.adjacent_tile = 'right'
            self.slope = True
            if (self.floor_y.x == 0 and self.floor_y.y == 32) or (self.floor_y.x == 32 and self.floor_y.y == 0):
                self.hack_for_slope = True
            else:
                self.hack_for_slope = False


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
        self.strait = Vector2(1, 0)  # preset velocity TODO: Use tilemap to determine path and velocity.
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
        if self.rect.top <= self.range_y.x:
            self.normal.y = 1
        elif self.rect.bottom >= self.range_y.y:
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
        self.velocity = Vector2(0, 0)
        self.forward_edge_coord = Vector2()
        self.normal = Vector2(0, 0)

        self.debug_screen = screen  # TODO: Make a debug switch for the program

        self.on_ground = False
        self.jumping = False
        self.gravity = 0.9

    def update(self, platform_group, tileset_group):
        """
        @param platform_group:
        @param tileset_group
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

        if self.normal.x:
            close_tile_list = []
            possible_platforms = scan_for_platforms_y(self, platform_group)
            if possible_platforms is not []:
                for platform in possible_platforms:
                    close_tile_list.append(platform)
            for tileset in tileset_group.tileset_list:
                tiles_to_check = scan_for_tiles_x(tileset, self)
                close_tile_list.append(closest_tile_x(tiles_to_check, self))
            new_closest = closest_from_list_x(close_tile_list, self)
            if new_closest is not None:
                if not new_closest.slope:
                    self.react_x(new_closest)
                else:
                    # print("do x sloped tiles")
                    self.rect.x += self.velocity.x
                    self.react_slope_x(new_closest)
            else:
                self.rect.x += self.velocity.x
        if self.normal.y:
            close_tile_list = []
            possible_platforms = scan_for_platforms_x(self, platform_group)
            if possible_platforms is not []:
                for platform in possible_platforms:
                    close_tile_list.append(platform)
            for tileset in tileset_group.tileset_list:
                tiles_to_check = scan_for_tiles_y(tileset, self)
                close_tile_list.append(closest_tile_y(tiles_to_check, self))
            new_closest = closest_from_list_y(close_tile_list, self)
            if new_closest is not None:
                if not new_closest.slope:
                    self.react_y(new_closest)
                else:
                    # print("do y sloped tiles")
                    self.react_slope_y(new_closest)
            else:
                self.rect.y += self.velocity.y

        self.jumping = self.jumping and self.velocity.y < 0
        self.velocity.x = 0
        self.velocity.y = min(self.velocity.y + self.gravity, 15)

    def react_x(self, close_tile):
        """

        @type close_tile: Prototype.Tile
        """
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
        if self.normal.y > 0:
            if (self.rect.bottom + self.velocity.y) <= close_tile.rect.top:
                # print("going down and not past close_tile")
                self.rect.bottom += self.velocity.y
            else:
                self.rect.bottom = close_tile.rect.top
                self.on_ground = True
        else:
            if (self.rect.top + self.velocity.y) >= close_tile.rect.bottom:
                self.rect.top += self.velocity.y
            else:
                self.rect.top = close_tile.rect.bottom

    def react_slope_x(self, close_tile):
        """

        @param close_tile:
        """
        if self.normal.y >= 0:
            # print("close_tile left:", close_tile.rect.x)
            if close_tile.floor_y.x > close_tile.floor_y.y:
                t = (self.rect.centerx - close_tile.rect.x) / 32
            else:
                t = (self.rect.centerx - close_tile.rect.x) / 32
            # t = (self.rect.centerx - close_tile.rect.x) / 32
            floor_y = ((1.0 - t) * close_tile.floor_y.x + t * close_tile.floor_y.y
                       + close_tile.tile_coords.y * close_tile.rect.height) - self.rect.width
            print('react_slope_x floor_y:', floor_y)
            if (self.rect.bottom + self.velocity.y) <= floor_y:
                # print("going down and not past close_tile")
                self.rect.y += self.velocity.y
            else:
                self.rect.bottom = floor_y
                self.on_ground = True
            if self.normal.x < 0 and close_tile.hack_for_slope:
                self.rect.bottom -= 5

    def react_slope_y(self, close_tile):
        """

        @param close_tile:
        """
        if self.normal.y >= 0:
            # print("close_tile left:", close_tile.rect.x)
            if close_tile.floor_y.x > close_tile.floor_y.y:
                t = (self.rect.right - close_tile.rect.x) / 32
            else:
                t = (self.rect.left - close_tile.rect.x) / 32
            # t = (self.rect.centerx - close_tile.rect.x) / 32
            floor_y = max(close_tile.rect.top, ((1.0 - t) * close_tile.floor_y.x + t * close_tile.floor_y.y
                          + close_tile.tile_coords.y * close_tile.rect.height))
            print('react_slope_y floor_y:', floor_y)
            if (self.rect.bottom + self.velocity.y) <= floor_y:
                # print("going down and not past close_tile")
                self.rect.y += self.velocity.y
            else:
                self.rect.bottom = floor_y
                self.on_ground = True

    def draw(self, screen, camera):
        """

        @type screen: pygame.Surface
        @param camera:
        """
        screen.blit(self.image, camera.apply(self))


def main():
    """

    The main() is where the main game loop is.
    First initialize stuff then run main game loop.
    """
    blocks_background = BackgroundManager('data/Background/blocks.png', 2)
    screen_size = Vector2(800, 600)
    screen = pygame.display.set_mode((screen_size.x, screen_size.y))
    clock = pygame.time.Clock()

    tw_0 = 32
    th_0 = 32
    my_tiles_0 = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 8, 8, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 8, 8, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [1, 1,11,12, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,16,15, 1, 6, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 5, 5, 5, 8, 8, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [1, 1, 1, 1,10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,14, 1, 1, 1, 6, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 5, 5, 5, 8, 8, 8, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [1, 1, 1, 1, 1,10, 0, 0, 0, 0, 0, 0, 0, 0,14, 1, 1, 1, 1, 6, 6, 0, 0, 3, 3, 0, 7, 7, 7, 7, 7, 5, 5, 5, 8, 8, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1,10, 0, 0, 0,13, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [1, 1, 1, 1, 1, 1,10, 0, 0, 0, 0, 0, 0,14, 1, 1, 1, 1, 1, 6, 6, 0, 0, 3, 3, 0, 7, 7, 7, 7, 7, 5, 5, 7, 7, 7, 7, 7, 7, 7, 0, 0, 2, 0, 0, 0, 0, 0, 0, 1,10, 0,13, 1, 0, 1, 1,10, 0,13, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [1, 1, 1, 1, 1, 1, 1,11,12, 0, 0,16,15, 1, 1, 1, 1, 1, 1, 6, 6, 0, 0, 3, 3, 0, 7, 7, 7, 7, 7, 5, 5, 7, 7, 7, 7, 7, 7, 7, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1]]

    tile_size_0 = Vector2(tw_0, th_0)
    tileset_0 = TileSet(my_tiles_0, screen, tile_size_0, 0)

    tw_1 = 64
    th_1 = 32
    my_tiles_1 = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 3, 4, 5, 6, 7, 8, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
    tile_size_1 = Vector2(tw_1, th_1)
    tileset_1 = TileSet(my_tiles_1, screen, tile_size_1, 1)

    ts_list = [tileset_0, tileset_1]
    tileset_group = TileSetsContainer(ts_list)

    player = Player(tw_0, th_0, 20, 50, (234, 0, 0), screen)
    entity_list = [player]
    platforms_group = pygame.sprite.Group()

    camera = Camera("complex", tileset_0.map_size.x * tileset_0.tile_size.x,
                    tileset_0.map_size.y * tileset_0.tile_size.y)

    speed = False
    while True:
        speed = False
        keys = pygame.key.get_pressed()
        if keys[pygame.K_b]:
            speed = True

        for e in pygame.event.get():
            if e.type == pygame.QUIT or e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            if e.type == pygame.KEYDOWN and e.key == pygame.K_SPACE and player.on_ground:
                if speed:
                    player.velocity.y = -16
                else:
                    player.velocity.y = -14
                player.on_ground = False
                player.jumping = True
            if e.type == pygame.KEYUP and e.key == pygame.K_SPACE and not player.on_ground and \
                    player.velocity.y < 0:
                player.velocity.y = 0
                player.jumping = False

        if keys[pygame.K_LEFT]:
            if speed:
                player.velocity.x -= 5
            else:
                player.velocity.x -= 3
        if keys[pygame.K_RIGHT]:
            if speed:
                player.velocity.x += 5
            else:
                player.velocity.x += 3

        camera.update(player, screen_size)

        screen.fill((125, 199, 245))
        blocks_background.update(camera, tileset_0)
        blocks_background.draw(screen, screen_size)
        tileset_group.draw(screen, camera)
        platforms_group.update(entity_list)
        platforms_group.draw(screen)
        player.update(platforms_group, tileset_group)
        player.draw(screen, camera)
        pygame.display.update()
        clock.tick(FPS)

if __name__ == "__main__":
    print(__version__, __author__ + '\n')
    main()
