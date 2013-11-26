#!/usr/bin/env python3
# coding=utf-8
import math
import pygame

# get intersecting axis (x, y)

def intersecting_rows(rect1, rect2):
    """

    @param rect2:
    @param rect1:
    @return:
    """
    # tile_left = self.rect.left // tileset.tile_size.x
    # tile_left = math.floor(rect1.left / rect2.width)
    tile_left = math.floor(rect1.left / rect2.width)
    # tile_right = self.rect.right // tileset.tile_size.x
    tile_right = math.ceil(rect1.right / rect2.height / 2)
    intersecting_range = (tile_left, tile_right)
    return intersecting_range


def intersecting_columns(rect1, rect2):
    """

    @param rect2:
    @param rect1:
    @return:
    """
    # tile_top = self.rect.top // tileset.tile_size.y
    tile_top = math.floor(rect1.top / rect2.width * 2)
    # tile_bottom = self.rect.bottom // tileset.tile_size.y
    ### tile_bottom = math.ceil(rect1.bottom / rect2.height
    tile_bottom = math.ceil(rect1.bottom / rect2.height)
    intersecting_range = (tile_top, tile_bottom)
    return intersecting_range


# scan intersecting tiles (x, y)

def scan_for_tiles_x(tileset, entity):
    """

    @param entity:
    @type tileset: Prototype.TileSet
    """
    all_tiles = []
    intersecting_range = intersecting_columns(entity.rect, tileset.tile_array[0, 0].rect)
    print("range x", intersecting_range)
    if entity.normal.x > 0:  # moving right
        # print("moving right")
        for i in range(intersecting_range[0], intersecting_range[1]):
            tmp_tile_list = tileset.scan_x_right(i, (entity.forward_edge_coord.x // tileset.tile_size.x) + 1)
            all_tiles.append(tmp_tile_list)
            # print("right i:", i)
    else:
        # print("moving left")
        for i in range(intersecting_range[0], intersecting_range[1]):
            tmp_tile_list = tileset.scan_x_left(i, (entity.forward_edge_coord.x // tileset.tile_size.x) - 1)
            all_tiles.append(tmp_tile_list)
            # print("left i:", i)
    return all_tiles


def scan_for_tiles_y(tileset, entity):
    """

    @param entity:
    @type tileset: Prototype.TileSet
    """
    all_tiles = []
    intersecting_range = intersecting_rows(entity.rect, tileset.tile_array[0, 0].rect)
    print("range y", intersecting_range)
    if entity.normal.y > 0:
        # print("moving down")
        for i in range(intersecting_range[0], intersecting_range[1]):
            tmp_tile_list = tileset.scan_y_bottom(i, (entity.forward_edge_coord.y // tileset.tile_size.y) + 1)
            all_tiles.append(tmp_tile_list)
            # print("down i:", i)
    else:
        # print("moving up")
        for i in range(intersecting_range[0], intersecting_range[1]):
            tmp_tile_list = tileset.scan_y_top(i, (entity.forward_edge_coord.y // tileset.tile_size.y) - 1)
            all_tiles.append(tmp_tile_list)
            # print("top i:", i)
    return all_tiles


def closest_tile_x(tiles_to_check, entity):
    # print(tiles_to_check)
    """


    @param entity:
    @type tiles_to_check: list
    @return:
    """
    distance_from_self = 1000000
    closest = None
    for i in tiles_to_check:
        for tmp_tile in i:
            if abs(tmp_tile.rect.centerx - entity.rect.centerx) < distance_from_self:
                closest = tmp_tile
                distance_from_self = abs(tmp_tile.rect.centerx - entity.rect.centerx)
                # print("CLOSEST:", closest, distance_from_self)
    if closest is not None:
        closest_img = pygame.Surface((closest.rect.width, closest.rect.height))
        closest_img.fill((0, 100, 255))
        entity.debug_screen.blit(closest_img, (closest.rect.x, closest.rect.y))
    return closest


def closest_tile_y(tiles_to_check, entity):
    # print(tiles_to_check)
    """
    @param entity:
    @type tiles_to_check: list
    @return:
    """
    distance_from_self = 1000000
    closest = None
    for i in tiles_to_check:
        for tmp_tile in i:
            if abs(tmp_tile.rect.centery - entity.rect.centery) < distance_from_self:
                closest = tmp_tile
                distance_from_self = abs(tmp_tile.rect.centery - entity.rect.centery)

    # print("CLOSEST:", closest, distance_from_self)
    if closest is not None:
        closest_img = pygame.Surface((closest.rect.width, closest.rect.height))
        closest_img.fill((0, 100, 255))
        entity.debug_screen.blit(closest_img, (closest.rect.x, closest.rect.y))
    return closest


# PUT ON THE BACK BURNER, stuff for platform collisions

def intersecting_platforms_x(moving_platforms, tileset, entity):
    """


    @param entity:
    @param moving_platforms:
    @param tileset:
    @return:
    """
    closest = None
    for platform in moving_platforms:
        player_intersecting = intersecting_columns(entity.rect, tileset.tile_array[0, 0].rect)
        platform_intersecting = intersecting_columns(platform.rect, tileset.tile_array[0, 0].rect)
        if player_intersecting[0] >= platform_intersecting[0] and player_intersecting[1] <= platform_intersecting[1]:
            # print("#! player intersects !#")
            distance_from_self = 10000000
            if abs(platform.rect.centerx - entity.rect.centerx) < distance_from_self:
                closest = platform
                distance_from_self = abs(platform.rect.centerx - entity.rect.centerx)
        if closest is not None:
            if entity.normal.x > 0 and entity.rect.centerx < platform.rect.centerx:
                closest_img = pygame.Surface((closest.rect.width, closest.rect.height))
                closest_img.fill((0, 100, 255))
                entity.debug_screen.blit(closest_img, (closest.rect.x, closest.rect.y))
            elif entity.normal.x < 0 and entity.rect.centerx > platform.rect.centerx:
                closest_img = pygame.Surface((closest.rect.width, closest.rect.height))
                closest_img.fill((0, 100, 255))
                entity.debug_screen.blit(closest_img, (closest.rect.x, closest.rect.y))
    return closest


def intersecting_platforms_y(moving_platforms, tileset, entity):
    """


    @param entity:
    @param moving_platforms:
    @param tileset:
    @return:
    """
    closest = None
    for platform in moving_platforms:
        player_intersecting = intersecting_rows(entity.rect, tileset.tile_array[0, 0].rect)
        platform_intersecting = intersecting_rows(platform.rect, tileset.tile_array[0, 0].rect)
        if player_intersecting[0] >= platform_intersecting[0] and player_intersecting[1] <= platform_intersecting[1]:
            # print("#! player intersects !#")
            distance_from_self = 10000000
            if abs(platform.rect.centery - entity.rect.centery) < distance_from_self:
                closest = platform
                distance_from_self = abs(platform.rect.centery - entity.rect.centery)
        if closest is not None:
            if entity.normal.y > 0 and entity.rect.centery < platform.rect.centery:
                closest_img = pygame.Surface((closest.rect.width, closest.rect.height))
                closest_img.fill((0, 100, 255))
                entity.debug_screen.blit(closest_img, (closest.rect.x, closest.rect.y))
            elif entity.normal.y < 0 and entity.rect.centery > platform.rect.centery:
                closest_img = pygame.Surface((closest.rect.width, closest.rect.height))
                closest_img.fill((0, 100, 255))
                entity.debug_screen.blit(closest_img, (closest.rect.x, closest.rect.y))
    return closest
