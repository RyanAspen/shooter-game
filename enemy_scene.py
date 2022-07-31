import math
import random

import pygame
import constants
from enemy_entity import EnemyEntity
from pixel_entity import PixelEntity
from scene import Scene

speed = 100


class EnemyScene(Scene):
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
