# Imports
import constants as constants
import pygame
import random

from entities.basic_entity import BasicEntity
from entities.pixel_entity import PixelEntity
from scene import Scene

# Custom data types

# Global constants
speed = 1000


class BasicScene(Scene):

    """
    BasicScene is a scene which spawns a bunch of entities that bounce
    into each other and mirrors on the boundaries of the screen. They can be
    destroyed by the projectiles of the player.
    """

    def __init__(self):
        background_color = pygame.Color(0, 20, 200)
        entity_dict = dict()
        for time in range(0, speed * 5 + 1, speed):
            entity_dict[time] = get_basic_entities(25)
        super().__init__(entity_dict=entity_dict, background_color=background_color)


def get_basic_entities(count) -> list[PixelEntity]:
    entities = []  # type: list[PixelEntity]
    for _ in range(count):
        spawn_point = [
            random.randint(0, constants.width),
            random.randint(0, constants.height),
        ]
        entity = BasicEntity(spawn_point)
        entities.append(entity)
    return entities
