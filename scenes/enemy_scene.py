# Imports
import constants as constants
import pygame
import random

from entities.enemy_entity import EnemyEntity
from entities.pixel_entity import PixelEntity
from scene import Scene

# Custom data types

# Global constants
speed = 100


class EnemyScene(Scene):

    """
    EnemyScene is a scene which spawns several entities that float at the top of
    the screen and shoots projectiles downwards toward the player. The enemy projectiles
    can destroy the player, and the player's projectiles can destroy the enemy entities.
    """

    def __init__(self):
        background_color = pygame.Color(0, 20, 200)
        entity_dict = dict()
        for time in range(1, speed * 5 + 2, speed):
            entity_dict[time] = get_enemies(1)
        super().__init__(entity_dict=entity_dict, background_color=background_color)


def get_enemies(count) -> list[PixelEntity]:
    entities = []  # type: list[PixelEntity]
    for _ in range(count):
        random_position = [random.randint(100, constants.width - 100), 30]
        entity = EnemyEntity(random_position)
        entities.append(entity)
    return entities
