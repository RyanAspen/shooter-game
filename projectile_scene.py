import random

import pygame
import constants
from enemy_projectile import EnemyProjectile
from pixel_entity import PixelEntity
from scene import Scene

speed = 100


class ProjectileScene(Scene):
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
