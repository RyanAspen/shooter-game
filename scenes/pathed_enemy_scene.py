# Imports
import constants as constants
import pygame
import random

from entities.pathed_enemy_entity import PathedEnemyEntity
from entities.pixel_entity import PixelEntity
from scenes.scene import Scene

# Custom data types

# Global constants
speed = 100


class PathedEnemyScene(Scene):

    """
    PathedEnemyScene is a scene which spawns several entities that take a set path and shoot projectiles that
    can destroy the player. The entities can be destroyed by the player's projectiles.
    """

    def __init__(self):
        background_color = pygame.Color(0, 20, 100)
        entity_dict = dict()
        for time in range(1):  # , speed * 5 + 2, speed):
            entity_dict[time] = get_enemy_wave()
        super().__init__(entity_dict=entity_dict, background_color=background_color)


def get_enemy_wave() -> list[PixelEntity]:
    entities = []  # type: list[PixelEntity]
    for index in range(6):
        offset = index * 100 + 100
        path_x = [
            offset + 200,
            offset,
            offset + 200,
            offset,
            offset + 200,
            offset,
        ]
        path_y = [70, 120, 170, 220, 270, 320]
        path = []
        for a in range(len(path_x)):
            path.append([path_x[a], path_y[a]])
        spawn_point = [offset, 20]
        entity = PathedEnemyEntity(spawn_point, path)
        entities.append(entity)
    return entities
