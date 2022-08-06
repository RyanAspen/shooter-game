# Imports
import constants as constants
import pygame
import random

from entities.pixel_entity import PixelEntity
from entities.target_entity import TargetEntity
from scenes.scene import Scene

# Custom data types

# Global constants
speed = 1000


class TargetScene(Scene):

    """
    TargetScene is a scene which spawns several stationary targets that
    can be destroyed by the player's projectiles
    """

    def __init__(self):
        background_color = pygame.Color(0, 20, 200)
        entity_dict = dict()
        for time in range(1, speed * 3 + 2, speed):
            entity_dict[time] = get_targets(3)
        super().__init__(entity_dict=entity_dict, background_color=background_color)


def get_targets(count) -> list[PixelEntity]:
    entities = []  # type: list[PixelEntity]
    for _ in range(count):
        random_position = [
            random.randint(100, constants.width - 100),
            random.randint(100, constants.height - 100),
        ]
        entity = TargetEntity(random_position)
        entities.append(entity)
    return entities
