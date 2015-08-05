#!/usr/bin/env python3
# coding=utf-8

__author__ = 'bubbles231'
__version__ = '0.0.3'
__status__ = 'Prototype'
__doc__ = """
Prototype.py - A collision detection prototype for MarioQuest.
Run with ./Prototype.py.

Prototype is going to try to make a reusable version of Tile Base (Smooth)

  1. It should do everything as instructed at
     http://higherorderfun.com/blog/2012/05/20/the-guide-to-implementing-2d
     -platformers/
     for Tile Base (Smooth)
  2. It will be easy to use in MarioQuest and modify to fit the game
  3. It will have the detection and resolution of collisions
  4. It will handle slopes, moving platforms, and maybe some other things

"""

import sys
from Helpers import *

FPS = 1000 / 15


class TileSetsContainer(object):
    """

    @type tileset_list: list
    """

    def __init__(self, tileset_list):
        self.tileset_list = tileset_list
        self.tileset_order = {}
        for tmp_tileset in tileset_list:
            tmp_tileset.draw()
            self.tileset_order[tmp_tileset.priority] = tmp_tileset

    def draw(self, screen, camera):
        """

        @type screen: pygame.Surface
        @param camera: Helpers.Camera
        """
        for i in range(len(self.tileset_order) - 1, -1, -1):
            screen.blit(self.tileset_order[i].image,
                        camera.apply(self.tileset_order[i]))


class TileSet(object):
    """

    @type level: list
    @type screen: pygame.Surface
    @type tile_size: Geometry.Vector2
    @type priority: int
    @param debugging: bool
    """

    def __init__(self, level, screen, tile_size, priority, debugging):
        self.size_info = dict()
        self.size_info['tile'] = tile_size
        self.size_info['map'] = Vector2(len(level[0]), len(level))

        # noinspection PyArgumentList
        self.image = pygame.Surface((self.size_info['map'].x *
                                     self.size_info['tile'].x,
                                     self.size_info['map'].y *
                                     self.size_info['tile'].y),
                                    pygame.SRCALPHA)
        self.rect = pygame.Rect(0, 0, self.size_info['map'].x *
                                self.size_info['tile'].x,
                                self.size_info['map'].y *
                                self.size_info['tile'].y)
        self.tile_array = {}
        for x in range(0, self.size_info['map'].x):
            for y in range(0, self.size_info['map'].y):
                # noinspection PyTypeChecker
                self.tile_array[x, y] = (self.make_tile
                                         (level[y][x],
                                          Vector2(
                                              x * self.size_info['tile'].x,
                                              y * self.size_info['tile'].y),
                                          self.size_info['tile']))
        self.ladder_list = []
        for x in range(0, self.size_info['map'].x):
            for y in range(0, self.size_info['map'].y):
                if (self.tile_array[x, y].tile_info['type'] == 'ladder' or
                        self.tile_array[x, y].tile_info['type'] == 'ladder_top'):  # TODO add logic for top_ladder
                    self.ladder_list.append(self.tile_array[x, y])

        self.priority = priority
        self.not_considered_tiles = []

        self.debug_screen = None
        self.debug_img = None
        if debugging:
            self.debug = True
            self.debug_init(screen)
        else:
            self.debug = False

    def debug_init(self, screen):
        """

        @param screen: pygame.Display
        """
        self.debug_screen = screen
        # noinspection PyArgumentList
        self.debug_img = pygame.Surface((self.size_info['tile'].x,
                                         self.size_info['tile'].y))
        self.debug_img.fill((255, 0, 0))

    @staticmethod
    def make_tile(tile_id, tile_position, tile_size):
        """

        @type tile_id: int
        @type tile_position: Geometry.Vector2
        @param tile_size: Geometry.Vector2
        """
        tile = None
        if tile_id == 0:
            tile = Tile(tile_position, '', tile_size, (0, 0, 0, 0))
        elif tile_id == 1:
            tile = Tile(tile_position, 'solid', tile_size, (150, 79, 35))
        elif tile_id == 2:
            tile = Tile(tile_position, 'solid', tile_size, (245, 208, 0))
        elif tile_id == 3:
            tile = Tile(tile_position, 'solid', tile_size, (0, 247, 0))
        elif tile_id == 4:
            tile = Tile(tile_position, 'solid', tile_size, (0, 100, 0))
        elif tile_id == 5:
            tile = Tile(tile_position, '', tile_size, (248, 144, 72))
        elif tile_id == 6:
            tile = Tile(tile_position, '', tile_size, (88, 200, 255))
        elif tile_id == 7:
            tile = Tile(tile_position, '', tile_size, (128, 184, 80))
        elif tile_id == 8:
            tile = Tile(tile_position, '', tile_size, (224, 224, 224))
        elif tile_id == 9:
            tile = Tile(tile_position, 'slope', tile_size,
                        'data/Tiles/Slope/Left/frame752.png', [0, 32])
        elif tile_id == 10:
            tile = Tile(tile_position, 'slope', tile_size,
                        'data/Tiles/Slope/Left/frame818.png', [0, 32])
        elif tile_id == 11:
            tile = Tile(tile_position, 'slope', tile_size,
                        'data/Tiles/Slope/Left/frame877.png', [0, 16])
        elif tile_id == 12:
            tile = Tile(tile_position, 'slope', tile_size,
                        'data/Tiles/Slope/Left/frame878.png', [17, 32])
        elif tile_id == 13:
            tile = Tile(tile_position, 'slope', tile_size,
                        'data/Tiles/Slope/Right/frame750.png', [32, 0])
        elif tile_id == 14:
            tile = Tile(tile_position, 'slope', tile_size,
                        'data/Tiles/Slope/Right/frame815.png', [32, 0])
        elif tile_id == 15:
            tile = Tile(tile_position, 'slope', tile_size,
                        'data/Tiles/Slope/Right/frame707.png', [16, 0])
        elif tile_id == 16:
            tile = Tile(tile_position, 'slope', tile_size,
                        'data/Tiles/Slope/Right/frame706.png', [32, 17])
        elif tile_id == 17:
            tile = Tile(tile_position, 'one-way', tile_size, (0, 224, 24))
        elif tile_id == 18:
            tile = Tile(tile_position, 'ladder', tile_size, (255, 255, 255))
        elif tile_id == 19:
            #  tile = Tile(tile_position, 'ladder_top', tile_size, (255, 150, 200))
            tile = Tile(tile_position, 'ladder', tile_size, (255, 255, 255))
        return tile

    def draw(self):
        """

        Draw tiles on tileset image
        """
        for x in range(0, self.size_info['map'].x):
            for y in range(0, self.size_info['map'].y):
                tmp_tile = self.tile_array[x, y]
                self.image.blit(tmp_tile.image,
                                (tmp_tile.rect.x, tmp_tile.rect.y))

    def debug_draw(self, x, y):
        """

        @param x: int
        @param y: int
        """
        self.debug_screen.blit(self.debug_img, (x, y))

    # noinspection PyUnusedLocal
    def scan_x_right(self, y, tile_x, entity):
        """

        @type y: int
        @type tile_x: int
        @type entity: Prototype.Entity
        @return: list
        """
        solid_tile_list = []
        for x in range(tile_x - 1, self.size_info['map'].x):
            try:
                tmp_tile = self.tile_array[x, y]
                if tmp_tile.tile_info['type'] != '':
                    if tmp_tile.tile_info['type'] == 'slope':
                        solid_tile_list.append(tmp_tile)
                        if tmp_tile.tile_info['adjacent_tile'] == 'left':
                            self.not_considered_tiles.append(
                                self.tile_array[x - 1, y])
                        elif tmp_tile.tile_info['adjacent_tile'] == 'right':
                            self.not_considered_tiles.append(
                                self.tile_array[x + 1, y])
                        if self.debug:
                            self.debug_draw(tmp_tile.rect.x, tmp_tile.rect.y)
                    elif tmp_tile.tile_info['type'] == 'one-way':
                        pass
                    elif tmp_tile.tile_info['type'] == 'ladder' or tmp_tile.tile_info['type'] == 'ladder_top':
                        solid_tile_list.append(tmp_tile)
                        if self.debug:
                            self.debug_draw(tmp_tile.rect.x, tmp_tile.rect.y)
                    else:
                        solid_tile_list.append(tmp_tile)
                        if self.debug:
                            self.debug_draw(tmp_tile.rect.x, tmp_tile.rect.y)
            except KeyError:
                print("scan_y_right: KeyError out of tileset bounds")
        return solid_tile_list

    # noinspection PyUnusedLocal
    def scan_x_left(self, y, tile_x, entity):
        """

        @type y: int
        @type tile_x: int
        @type entity: Prototype.Entity
        @return: list
        """
        solid_tile_list = []
        for x in range(tile_x, -1, -1):
            try:
                tmp_tile = self.tile_array[x, y]
                if tmp_tile.tile_info['type'] != '':
                    if tmp_tile.tile_info['type'] == 'slope':
                        solid_tile_list.append(tmp_tile)
                        if tmp_tile.tile_info['adjacent_tile'] == 'left':
                            self.not_considered_tiles.append(
                                self.tile_array[x - 1, y])
                        elif tmp_tile.tile_info['adjacent_tile'] == 'right':
                            self.not_considered_tiles.append(
                                self.tile_array[x + 1, y])
                        if self.debug:
                            self.debug_draw(tmp_tile.rect.x, tmp_tile.rect.y)
                    elif tmp_tile.tile_info['type'] == 'one-way':
                        pass
                    elif tmp_tile.tile_info['type'] == 'ladder' or tmp_tile.tile_info['type'] == 'ladder_top':
                        solid_tile_list.append(tmp_tile)
                        if self.debug:
                            self.debug_draw(tmp_tile.rect.x, tmp_tile.rect.y)
                    else:
                        solid_tile_list.append(tmp_tile)
                        if self.debug:
                            self.debug_draw(tmp_tile.rect.x, tmp_tile.rect.y)
            except KeyError:
                print("scan_y_left: KeyError out of tileset bounds")
        return solid_tile_list

    def scan_y_bottom(self, x, tile_y, entity):
        """

        @type x: int
        @type tile_y: int
        @type entity: Prototype.Entity
        @return: list
        """
        solid_tile_list = []
        for y in range(tile_y - 1, self.size_info['map'].y):
            try:
                tmp_tile = self.tile_array[x, y]
                if tmp_tile.tile_info['type'] != '':
                    if tmp_tile.tile_info['type'] == 'one-way':
                        if one_way_platform_checker(entity, tmp_tile):
                            solid_tile_list.append(tmp_tile)
                    elif tmp_tile.tile_info['type'] == 'ladder' or tmp_tile.tile_info['type'] == 'ladder_top':
                        solid_tile_list.append(tmp_tile)
                        if self.debug:
                            self.debug_draw(tmp_tile.rect.x, tmp_tile.rect.y)
                    else:
                        solid_tile_list.append(tmp_tile)
                        if self.debug:
                            self.debug_draw(tmp_tile.rect.x, tmp_tile.rect.y)
            except KeyError:
                print("scan_y_bottom: KeyError out of tileset bounds")
        return solid_tile_list

    def scan_y_top(self, x, tile_y, entity):
        """

        @type x: int
        @type tile_y: int
        @type entity: Prototype.Entity
        @return: list
        """
        solid_tile_list = []
        for y in range(tile_y, -1, -1):
            try:
                tmp_tile = self.tile_array[x, y]
                if tmp_tile.tile_info['type'] != '':
                    if tmp_tile.tile_info['type'] == 'one-way':
                        if one_way_platform_checker(entity, tmp_tile):
                            solid_tile_list.append(tmp_tile)
                    elif tmp_tile.tile_info['type'] == 'ladder' or tmp_tile.tile_info['type'] == 'ladder_top':
                        solid_tile_list.append(tmp_tile)
                        if self.debug:
                            self.debug_draw(tmp_tile.rect.x, tmp_tile.rect.y)
                    else:
                        solid_tile_list.append(tmp_tile)
                        if self.debug:
                            self.debug_draw(tmp_tile.rect.x, tmp_tile.rect.y)
            except KeyError:
                print("scan_y_top: KeyError out of tileset bounds")
        return solid_tile_list


class Entity(pygame.sprite.Sprite):
    """

    Entity() is a parent class which will have Children like Player,
    MovingPlatform, and Tile.
    """

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)


class Tile(Entity):
    """

    @param position: Geometry.Vector2
    @param t_type: str
    @param dimensions: Geometry.Vector2
    @param img_path: str
    @param slope_pts: list
    """

    def __init__(self, position, t_type, dimensions, img_path, slope_pts=None):
        Entity.__init__(self)
        self.rect = pygame.Rect(position.x, position.y, dimensions.x,
                                dimensions.y)
        self.tile_coords = Vector2(position.x // dimensions.x,
                                   position.y // dimensions.y)
        # noinspection PyArgumentList
        self.image = pygame.Surface((self.rect.width, self.rect.height),
                                    pygame.SRCALPHA)
        if type(img_path) is str:
            try:
                self.image = pygame.image.load(img_path).convert_alpha()
            except pygame.error:
                print("Image", img_path, "is missing!")
                self.image.fill((1, 1, 1))
        elif type(img_path) is tuple:
            self.image.fill(img_path)

        self.tile_info = {
            'type': t_type,
            'floor_y': None,
            'tall_edge': None,
            'short_edge': None,
            'adjacent_tile': False
        }

        if self.tile_info['type'] == 'slope':
            self.tile_info['floor_y'] = Vector2(slope_pts[0],
                                                slope_pts[1])
            if slope_pts[0] > slope_pts[1]:
                self.tile_info['tall_edge'] = self.rect.left
                self.tile_info['short_edge'] = self.rect.right
            elif slope_pts[0] < slope_pts[1]:
                self.tile_info['tall_edge'] = self.rect.right
                self.tile_info['short_edge'] = self.rect.left
            if slope_pts[0] == 0:
                self.tile_info['adjacent_tile'] = 'left'
            elif slope_pts[1] == 0:
                self.tile_info['adjacent_tile'] = 'right'
            if ((self.tile_info['floor_y'].x == 0 and self.tile_info['floor_y'].y == 32) or
                    (self.tile_info['floor_y'].x == 32 and self.tile_info['floor_y'].y == 0)):
                self.hack_for_slope = True
            else:
                self.hack_for_slope = False


class Player(Entity):
    """

    @type position: Geometry.Vector2
    @type dimensions: Geometry.Vector2
    @type screen: pygame.Display
    @type debugging: bool
    """

    def __init__(self, position, dimensions, screen, debugging):
        Entity.__init__(self)
        self.rect = pygame.Rect(position.x, position.y,
                                dimensions.x, dimensions.y)
        # noinspection PyArgumentList
        self.image = pygame.Surface((self.rect.width, self.rect.height))
        self.image.fill((234, 0, 0))
        self.velocity = Vector2(0, 0)
        self.forward_edge = Vector2()

        self.info = {
            'normal': Vector2(0, 0),
            'on_ground': False,
            'on_ladder': False,
            'on_top_ladder': False,
            'jumping': False,
            'hit_up': False,
            'hit_down': False,
            'hit_left': False,
            'hit_right': False,
            'hit_jump': False,
            'gravity': 0.9
        }

        self.debug_screen = None
        if debugging:
            self.debug = True
            self.debug_init(screen)
        else:
            self.debug = False

    def debug_init(self, screen):
        """

        @param screen: pygame.Display
        """
        self.debug_screen = screen

    def update(self, platform_group, tileset_group):
        """

        @param platform_group: pygame.Sprite.Group
        @param tileset_group:  Prototype.TileSetContainer
        """
        if self.velocity.x > 0:
            self.info['normal'].x = 1
            self.forward_edge.x = self.rect.right
        elif self.velocity.x < 0:
            self.info['normal'].x = -1
            self.forward_edge.x = self.rect.left
        elif self.velocity.x == 0:
            self.info['normal'].x = 0
            self.forward_edge.x = None

        if self.velocity.y > 0:
            self.info['normal'].y = 1
            self.forward_edge.y = self.rect.bottom
        elif self.velocity.y < 0:
            self.info['normal'].y = -1
            self.forward_edge.y = self.rect.top
        elif self.velocity.y == 0:
            self.info['normal'].y = 0
            self.forward_edge.y = None

        if self.info['normal'].x:
            close_tile_list = []
            possible_platforms = scan_for_platforms_y(self, platform_group)
            if possible_platforms is not []:
                for platform in possible_platforms:
                    close_tile_list.append(platform)
            for tileset in tileset_group.tileset_list:
                tiles_to_check = scan_for_tiles_x(tileset, self)
                close_tile_list.append(closest_tile_x(tiles_to_check, self))
            new_ladder_closest = closest_ladder_x(close_tile_list, self)
            new_closest = closest_from_list_x(close_tile_list, self)
            if new_closest is not None:
                if (new_closest.tile_info['type'] == 'solid' or
                        new_closest.tile_info['type'] == 'one-way'):
                    self.react_x(new_closest)
                elif new_closest.tile_info['type'] == 'slope':
                    # print("do x sloped tiles")
                    self.rect.x += self.velocity.x
                    self.react_slope_x(new_closest)
            elif new_ladder_closest is None:
                self.rect.x += self.velocity.x

            if new_ladder_closest is not None:
                self.react_ladder_x(new_ladder_closest)
        if self.info['normal'].y:
            close_tile_list = []
            possible_platforms = scan_for_platforms_x(self, platform_group)
            if possible_platforms is not []:
                for platform in possible_platforms:
                    close_tile_list.append(platform)
            for tileset in tileset_group.tileset_list:
                tiles_to_check = scan_for_tiles_y(tileset, self)
                close_tile_list.append(closest_tile_y(tiles_to_check, self))
            new_ladder_closest = closest_ladder_x(close_tile_list, self)
            new_closest = closest_from_list_y(close_tile_list, self)
            if new_closest is not None:
                if (new_closest.tile_info['type'] == 'solid' or
                        new_closest.tile_info['type'] == 'one-way'):
                    self.react_y(new_closest)
                elif new_closest.tile_info['type'] == 'slope':
                    # print("do y sloped tiles")
                    self.react_slope_y(new_closest)
            elif new_ladder_closest is None:
                self.rect.y += self.velocity.y

            if new_ladder_closest is not None:
                self.react_ladder_y(new_ladder_closest)

        self.info['jumping'] = self.info['jumping'] and self.velocity.y < 0
        self.velocity.x = 0
        # if not self.info['on_ladder']:  # Counteract this below
        self.velocity.y = min(self.velocity.y + self.info['gravity'], 15)

    def react_x(self, close_tile):
        """

        @type close_tile: Prototype.Tile
        """
        if self.info['normal'].x > 0:
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
        if self.info['normal'].y > 0:
            if (self.rect.bottom + self.velocity.y) <= close_tile.rect.top:
                # print("going down and not past close_tile")
                self.rect.bottom += self.velocity.y
            else:
                self.rect.bottom = close_tile.rect.top
                self.info['on_ground'] = True
        else:
            if (self.rect.top + self.velocity.y) >= close_tile.rect.bottom:
                self.rect.top += self.velocity.y
            else:
                self.rect.top = close_tile.rect.bottom
                self.velocity.y = 0.5

    def react_slope_x(self, close_tile):
        """

        @param close_tile: Prototype.Tile
        """
        if self.info['normal'].y >= 0:
            # print("close_tile left:", close_tile.rect.x)
            if (close_tile.tile_info['floor_y'].x >
                    close_tile.tile_info['floor_y'].y):
                t = (self.rect.centerx - close_tile.rect.x) / 32
            else:
                t = (self.rect.centerx - close_tile.rect.x) / 32
                # t = (self.rect.centerx - close_tile.rect.x) / 32
            floor_y = (((1.0 - t) * close_tile.tile_info['floor_y'].x + t *
                        close_tile.tile_info['floor_y'].y) +
                       close_tile.tile_coords.y * close_tile.rect.height -
                       self.rect.width)
            print('react_slope_x floor_y:', floor_y)
            if (self.rect.bottom + self.velocity.y) <= floor_y:
                # print("going down and not past close_tile")
                self.rect.y += self.velocity.y
            else:
                self.rect.bottom = floor_y
                self.info['on_ground'] = True
            if self.info['normal'].x < 0 and close_tile.hack_for_slope:
                self.rect.bottom -= 5

    def react_slope_y(self, close_tile):
        """

        @param close_tile: Prototype.Tile
        """
        if self.info['normal'].y >= 0:
            # print("close_tile left:", close_tile.rect.x)
            if (close_tile.tile_info['floor_y'].x >
                    close_tile.tile_info['floor_y'].y):
                t = (self.rect.right - close_tile.rect.x) / 32
            else:
                t = (self.rect.left - close_tile.rect.x) / 32
                # t = (self.rect.centerx - close_tile.rect.x) / 32
            floor_y = max(close_tile.rect.top,
                          ((1.0 - t) * close_tile.tile_info['floor_y'].x +
                           t * close_tile.tile_info['floor_y'].y +
                           close_tile.tile_coords.y * close_tile.rect.height))
            print('react_slope_y floor_y:', floor_y)
            if (self.rect.bottom + self.velocity.y) <= floor_y:
                # print("going down and not past close_tile")
                self.rect.y += self.velocity.y
            else:
                self.rect.bottom = floor_y
                self.info['on_ground'] = True

    def pre_react_ladder(self, close_tile):
        print('on_ladder: ', self.info['on_ladder'])
        print('hit_up:', self.info['hit_up'])
        print('hit_down:', self.info['hit_down'])
        print('hit_jump:', self.info['hit_jump'])
        if (self.rect.colliderect(close_tile.rect) or self.info['hit_up'] or
                self.info['hit_down']):
            self.info['on_ladder'] = True
        if self.info['on_ladder'] and self.info['hit_jump']:
            self.info['on_ladder'] = False
            self.rect.y -= 2
        if not self.rect.colliderect(close_tile.rect):
            self.info['on_ladder'] = False

    def react_ladder_x(self, close_tile):
        self.pre_react_ladder(close_tile)
        # print('make react_ladder_x')
        if self.info['on_ladder']:
            if self.info['hit_left']:
                self.rect.x -= 2
            elif self.info['hit_right']:
                self.rect.x += 2
            return
        self.rect.x += self.velocity.x

    def react_ladder_y(self, close_tile):
        self.pre_react_ladder(close_tile)
        # print('make react_ladder_y')
        if self.info['on_ladder']:
            if self.info['hit_up']:
                self.rect.y -= 2
            elif self.info['hit_down']:
                self.rect.y += 2
            return
        self.rect.y += self.velocity.y

    def draw(self, screen, camera):
        """

        @type screen: pygame.Surface
        @param camera: Helpers.Camera
        """
        screen.blit(self.image, camera.apply(self))

    def debug_draw(self, img, x, y):
        """

        @param img: pygame.Surface
        @param x: int
        @param y: int
        """
        self.debug_screen.blit(img, (x, y))


def main(debugging):
    """

    The main() is where the main game loop is.
    First initialize stuff then run main game loop.
    @param debugging: bool
    """
    blocks_background = BackgroundManager('data/Background/blocks.png', 2)
    screen_size = Vector2(800, 600)
    screen = pygame.display.set_mode((screen_size.x, screen_size.y))
    clock = pygame.time.Clock()

    my_tiles_0 = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 17, 1, 19, 1, 17, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 18, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 18, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 18, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 8, 8, 8,
         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 17, 17, 1, 17, 17, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 8, 8,
         8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 11, 12, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 16, 15, 1, 6, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 5, 5, 5, 8, 8,
         8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 1, 1, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 14, 1, 1, 1, 6, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 5, 5, 5, 8, 8,
         8, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 10, 0, 0, 0, 0, 0, 0, 0, 0, 14, 1, 1, 1, 1, 6, 6, 0, 0, 3, 3, 0, 7, 7, 7, 7, 7, 5, 5, 5, 8, 8,
         8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 10, 0, 0, 0, 13, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 1, 10, 0, 0, 0, 0, 0, 0, 14, 1, 1, 1, 1, 1, 6, 6, 0, 0, 3, 3, 0, 7, 7, 7, 7, 7, 5, 5, 7, 7, 7,
         7, 7, 7, 7, 0, 0, 2, 0, 0, 0, 0, 0, 0, 1, 10, 0, 13, 1, 0, 1, 1, 10, 0, 13, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 1, 1, 11, 12, 0, 0, 16, 15, 1, 1, 1, 1, 1, 1, 6, 6, 0, 0, 3, 3, 0, 7, 7, 7, 7, 7, 5, 5, 7, 7, 7,
         7, 7, 7, 7, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
         1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0,
         0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1]]

    tw_0 = 32
    th_0 = 32

    tile_size_0 = Vector2(tw_0, th_0)
    # noinspection PyTypeChecker
    tileset_0 = TileSet(my_tiles_0, screen, tile_size_0, 0, debugging)

    my_tiles_1 = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
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

    tw_1 = 64
    th_1 = 32
    tile_size_1 = Vector2(tw_1, th_1)
    # noinspection PyTypeChecker
    tileset_1 = TileSet(my_tiles_1, screen, tile_size_1, 1, debugging)

    ts_list = [tileset_0, tileset_1]
    tileset_group = TileSetsContainer(ts_list)

    # noinspection PyTypeChecker
    player = Player(Vector2(tw_0, th_0), Vector2(20, 50), screen, debugging)
    entity_list = [player]
    platforms_group = pygame.sprite.Group()

    camera = Camera("complex", tileset_0.size_info['map'].x *
                    tileset_0.size_info['tile'].x,
                    tileset_0.size_info['map'].y *
                    tileset_0.size_info['tile'].y)

    while True:
        speed = False
        keys = pygame.key.get_pressed()
        if keys[pygame.K_b]:
            speed = True

        for e in pygame.event.get():
            if (e.type == pygame.QUIT or e.type == pygame.KEYDOWN and
                    e.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()
            if (e.type == pygame.KEYDOWN and e.key == pygame.K_SPACE and
                    player.info['on_ground']):
                if speed:
                    player.velocity.y = -16
                else:
                    player.velocity.y = -14
                player.info['on_ground'] = False
                player.info['jumping'] = True
            if (e.type == pygame.KEYUP and e.key == pygame.K_SPACE and
                    not player.info['on_ground'] and player.velocity.y < 0):
                player.velocity.y = 0
                player.info['jumping'] = False

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
        if keys[pygame.K_UP]:
            player.info['hit_up'] = True
        else:
            player.info['hit_up'] = False
        if keys[pygame.K_DOWN]:
            player.info['hit_down'] = True
        else:
            player.info['hit_down'] = False
        if keys[pygame.K_LEFT]:
            player.info['hit_left'] = True
        else:
            player.info['hit_left'] = False
        if keys[pygame.K_RIGHT]:
            player.info['hit_right'] = True
        else:
            player.info['hit_right'] = False
        if keys[pygame.K_SPACE]:
            player.info['hit_jump'] = True
        else:
            player.info['hit_jump'] = False

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
    debug = None
    for arg in sys.argv:
        if arg == '-d' or arg == '--debug':
            debug = True
        else:
            debug = False
            # noinspection PyUnboundLocalVariable
    main(debug)
