# Imports
import constants as constants
import pygame
import random

from entities.enemy_projectile import EnemyProjectile
from entities.pixel_entity import PixelEntity
from scenes.scene import Scene

# Custom data types

# Global constants
speed = 100


class ProjectileScene(Scene):

    """
    ProjectileScene is a scene which spawns several sets of projectiles which fall from the
    top of the screen that can destroy the player.
    """

    def __init__(self):
        background_color = pygame.Color(110, 130, 0)
        entity_dict = dict()
        for time in range(0, speed * 5 + 1, speed):
            entity_dict[time] = get_enemy_projectile_entities(10)
        super().__init__(entity_dict=entity_dict, background_color=background_color)


def get_enemy_projectile_entities(count) -> list[PixelEntity]:
    entities = []  # type: list[PixelEntity]
    for _ in range(count):
        spawn_point = [random.randint(0, constants.width), 0]
        entity = EnemyProjectile(spawn_point)
        entities.append(entity)
    return entities
