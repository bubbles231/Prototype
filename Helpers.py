#!/usr/bin/env python3
# coding=utf-8
from Geometry.Vector2 import Vector2
import math
import pygame


def intersecting_rows(rect1, rect2):
    """

    @param rect2:
    @param rect1:
    @return:
    """
    tile_left = math.floor(rect1.left / rect2.width)
    tile_right = math.ceil(rect1.right / rect2.width)
    intersecting_range = (tile_left, tile_right)
    return intersecting_range


def intersecting_columns(rect1, rect2):
    """

    @param rect2:
    @param rect1:
    @return:
    """
    tile_top = math.floor(rect1.top / rect2.height)
    tile_bottom = math.ceil(rect1.bottom / rect2.height)
    intersecting_range = (tile_top, tile_bottom)
    return intersecting_range


def scan_for_tiles_x(tileset, entity):
    """

    @param entity:
    @type tileset: Prototype.TileSet
    """
    all_tiles = []
    intersecting_range = intersecting_columns(entity.rect, tileset.tile_array[0, 0].rect)
    # print("range x", intersecting_range)
    if entity.normal.x > 0:
        for i in range(intersecting_range[0], intersecting_range[1]):
            tmp_tile_list = tileset.scan_x_right(i, (entity.forward_edge_coord.x // tileset.tile_size.x) + 1, entity)
            all_tiles.extend(tmp_tile_list)
    else:
        for i in range(intersecting_range[0], intersecting_range[1]):
            tmp_tile_list = tileset.scan_x_left(i, (entity.forward_edge_coord.x // tileset.tile_size.x) - 1, entity)
            all_tiles.extend(tmp_tile_list)

    if on_slope_tile(entity, tileset):
        for i in range(0, len(all_tiles)):
            for bad_tile in tileset.not_considered_tiles:
                try:
                    if all_tiles[i] == bad_tile:
                        del(all_tiles[i])
                except IndexError:
                    # print("index error: all_tiles[i]")
                    pass  # TODO: This is an ugly hack fix it later

    return all_tiles


def scan_for_tiles_y(tileset, entity):
    """

    @param entity:
    @type tileset: Prototype.TileSet
    """
    all_tiles = []
    intersecting_range = intersecting_rows(entity.rect, tileset.tile_array[0, 0].rect)
    # print("range y", intersecting_range)
    if entity.normal.y > 0:
        for i in range(intersecting_range[0], intersecting_range[1]):
            tmp_tile_list = tileset.scan_y_bottom(i, (entity.forward_edge_coord.y // tileset.tile_size.y) + 1, entity)
            all_tiles.extend(tmp_tile_list)
    else:
        for i in range(intersecting_range[0], intersecting_range[1]):
            tmp_tile_list = tileset.scan_y_top(i, (entity.forward_edge_coord.y // tileset.tile_size.y) - 1, entity)
            all_tiles.extend(tmp_tile_list)
    if on_slope_tile(entity, tileset):
        for i in range(0, len(all_tiles)):
            for bad_tile in tileset.not_considered_tiles:
                try:
                    if all_tiles[i] == bad_tile:
                        del(all_tiles[i])
                except IndexError:
                    # print("index error: all_tiles[i]")
                    pass  # TODO: This is an ugly hack fix it later
    return all_tiles


def closest_tile_x(tiles_to_check, entity):
    """

    @param entity:
    @type tiles_to_check: list
    @return:
    """
    distance_from_self = 1000000
    closest = None
    for tmp_tile in tiles_to_check:
            if abs(tmp_tile.rect.centerx - entity.rect.centerx) < distance_from_self:
                closest = tmp_tile
                distance_from_self = abs(tmp_tile.rect.centerx - entity.rect.centerx)
    if closest is not None:
        closest_img = pygame.Surface((closest.rect.width, closest.rect.height))
        closest_img.fill((0, 100, 255))
        entity.debug_screen.blit(closest_img, (closest.rect.x, closest.rect.y))
    return closest


def closest_tile_y(tiles_to_check, entity):
    """
    @param entity:
    @type tiles_to_check: list
    @return:
    """
    distance_from_self = 1000000
    closest = None
    for tmp_tile in tiles_to_check:
            if abs(tmp_tile.rect.centery - entity.rect.centery) < distance_from_self:
                closest = tmp_tile
                distance_from_self = abs(tmp_tile.rect.centery - entity.rect.centery)
    if closest is not None:
        closest_img = pygame.Surface((closest.rect.width, closest.rect.height))
        closest_img.fill((0, 100, 255))
        entity.debug_screen.blit(closest_img, (closest.rect.x, closest.rect.y))
    return closest


def closest_from_list_x(close_tile_list, entity):
    """

    @param close_tile_list:
    @param entity:
    @return:
    """
    distance_from_self = 1000000
    closest = None
    for tmp_tile in close_tile_list:
        if tmp_tile is not None:
            if entity.normal.x > 0:
                if abs(tmp_tile.rect.left - entity.rect.right) < distance_from_self:
                    closest = tmp_tile
                    distance_from_self = abs(tmp_tile.rect.left - entity.rect.right)
            else:
                if abs(tmp_tile.rect.right - entity.rect.left) < distance_from_self:
                    closest = tmp_tile
                    distance_from_self = abs(tmp_tile.rect.right - entity.rect.left)
            if tmp_tile.slope:
                slope_tile = touching_slope_tile(entity, tmp_tile)
                if slope_tile is not None:
                    closest = slope_tile

    if closest is not None:
        closest_img = pygame.Surface((closest.rect.width, closest.rect.height))
        closest_img.fill((50, 50, 50))
        entity.debug_screen.blit(closest_img, (closest.rect.x, closest.rect.y))
    return closest


def closest_from_list_y(close_tile_list, entity):
    """

    @param close_tile_list:
    @param entity:
    @return:
    """
    distance_from_self = 1000000
    closest = None
    for tmp_tile in close_tile_list:
        if tmp_tile is not None:
            if entity.normal.y > 0:
                if abs(tmp_tile.rect.top - entity.rect.bottom) < distance_from_self:
                    closest = tmp_tile
                    distance_from_self = abs(tmp_tile.rect.top - entity.rect.bottom)
            else:
                if abs(tmp_tile.rect.bottom - entity.rect.top) < distance_from_self:
                    closest = tmp_tile
                    distance_from_self = abs(tmp_tile.rect.bottom - entity.rect.top)
            if tmp_tile.slope:
                slope_tile = touching_slope_tile(entity, tmp_tile)
                if slope_tile is not None:
                    closest = slope_tile

    if closest is not None:
        closest_img = pygame.Surface((closest.rect.width, closest.rect.height))
        closest_img.fill((100, 100, 100))
        entity.debug_screen.blit(closest_img, (closest.rect.x, closest.rect.y))
    return closest


def touching_slope_tile(entity, slope_tile):
    intersecting_range = intersecting_rows(entity.rect, slope_tile.rect)
    for i in range(intersecting_range[0], intersecting_range[1]):
        if slope_tile.tile_coords.x == i:
            return slope_tile
    return None


def on_slope_tile(entity, tileset):
    intersecting_range = intersecting_rows(entity.rect, tileset.tile_array[0, 0].rect)
    bottom_y = math.floor(entity.rect.bottom / tileset.tile_size.x)
    for i in range(intersecting_range[0], intersecting_range[1]):
        try:
            tmp_tile = tileset.tile_array[i, bottom_y]
            if tmp_tile.slope is True and tmp_tile.floor_y.x != 0 and tmp_tile.floor_y.y != 0:
                return True
        except KeyError:
            print("on_slope_tile: KeyError out of tileset bounds")
    return False


def collide_platform_x(platform, entities):
    """

    @param platform:
    @param entities:
    """
    for e in entities:
        if pygame.sprite.collide_rect(platform, e):
            if platform.normal.x > 0 and platform.rect.x < e.rect.x and platform.rect.right >= e.rect.left:
                e.rect.left = platform.rect.right
            if platform.normal.x < 0 and platform.rect.x > e.rect.x and platform.rect.left <= e.rect.right:
                e.rect.right = platform.rect.left


def collide_platform_y(platform, entities):
    """

    @param platform:
    @param entities:
    """
    for e in entities:
        if pygame.sprite.collide_rect(platform, e):
            if platform.normal.y > 0 and platform.rect.bottom > e.rect.top and platform.rect.x <= \
                    e.rect.y and e.rect.left > platform.rect.left and e.rect.right < platform.rect.right:
                e.rect.top = platform.rect.bottom
            if platform.normal.y < 0 and platform.rect.top < e.rect.bottom and platform.rect.x >= \
                    e.rect.y and e.rect.left > platform.rect.left and e.rect.right < platform.rect.right:
                e.rect.bottom = platform.rect.top


def scan_for_platforms_x(entity, platform_group):
    """

    @param entity:
    @param platform_group:
    @return:
    """
    platform_list = []
    for platform in platform_group:
        if platform.rect.width >= entity.rect.width:
            if platform.rect.left <= entity.rect.left <= platform.rect.right or \
                    platform.rect.left <= entity.rect.right <= platform.rect.right:
                if entity.normal.y > 0 and platform.rect.top >= entity.rect.bottom or \
                        entity.normal.y < 0 and platform.rect.bottom <= entity.rect.top:
                    platform_list.append(platform)
        else:
            if entity.rect.left <= platform.rect.left <= entity.rect.right or \
                    entity.rect.left <= platform.rect.right <= entity.rect.right:
                if entity.normal.y > 0 and platform.rect.top >= entity.rect.bottom or \
                        entity.normal.x < 0 and platform.rect.bottom <= entity.rect.top:
                    platform_list.append(platform)
                platform_list.append(platform)
    return platform_list


def scan_for_platforms_y(entity, platform_group):
    """

    @param entity:
    @param platform_group:
    @return:
    """
    platform_list = []
    for platform in platform_group:
        if platform.rect.height >= entity.rect.height:
            if platform.rect.top <= entity.rect.top <= platform.rect.bottom or \
                    platform.rect.top <= entity.rect.bottom <= platform.rect.bottom:
                if entity.normal.x > 0 and platform.rect.left >= entity.rect.right or \
                        entity.normal.x < 0 and platform.rect.right <= entity.rect.left:
                    platform_list.append(platform)
        else:
            if entity.rect.top <= platform.rect.top <= entity.rect.bottom or \
                    entity.rect.top <= platform.rect.bottom <= entity.rect.bottom:
                if entity.normal.x > 0 and platform.rect.left >= entity.rect.right or \
                        entity.normal.x < 0 and platform.rect.right <= entity.rect.left:
                    platform_list.append(platform)
    return platform_list


class Camera(object):
    def __init__(self, camera_func=None, width=None, height=None):
        if camera_func == "complex":
            self.camera_func = self.complex_camera
        elif camera_func == "simple":
            self.camera_func = self.simple_camera
        elif camera_func == "debug":
            self.camera_func = self.debug_camera
        else:
            print("no camera func defined")
        if width is not None and height is not None:
            self.state = pygame.Rect(0, 0, width, height)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target, screen_size):
        self.state = self.camera_func(self.state, target.rect, screen_size)

    @staticmethod
    def debug_camera(camera, target_rect, screen_size):
        return pygame.Rect(0, 0, screen_size.x, screen_size.y)

    @staticmethod
    def simple_camera(camera, target_rect, screen_size):
        l, t, _, _ = target_rect
        _, _, w, h = camera
        return pygame.Rect(-l + screen_size.x / 2, -t + screen_size.y / 2, w, h)

    @staticmethod
    def complex_camera(camera, target_rect, screen_size):
        l, t, _, _ = target_rect
        _, _, w, h = camera
        l, t, _, _ = -l + screen_size.x / 2, -t + screen_size.y / 2, w, h

        l = min(0, l)                                     # stop scrolling at the left edge
        l = max(-(camera.width - screen_size.x), l)       # stop scrolling at the right edge
        t = max(-(camera.height - screen_size.y), t)      # stop scrolling at the bottom
        t = min(0, t)                                     # stop scrolling at the top
        return pygame.Rect(l, t, w, h)


class BackgroundManager(object):

    def __init__(self, background_path, parallax):
        self.background = pygame.image.load(background_path)
        self.background_rect = self.background.get_rect()
        self.parallax = parallax
        self.position = Vector2(0, 0)

    def update(self, camera, tileset):
        self.position.x = (-(camera.state.left / self.parallax) // self.background_rect.width) \
            * self.background_rect.width
        self.position.y = (tileset.map_size.y * tileset.tile_size.y - self.background_rect.height)
        # give parallax effect
        self.position.x += camera.state.left / self.parallax
        self.position.y += camera.state.top

    def draw(self, screen, screen_size):
        screen.blit(self.background, (self.position.x, self.position.y + 32))
        copies = (screen_size.x // self.background_rect.width) + 1
        while copies > 0:
            self.position.x += self.background_rect.width
            screen.blit(self.background, (self.position.x, self.position.y + 32))
            copies -= 1
