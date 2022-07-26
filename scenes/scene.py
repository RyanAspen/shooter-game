# Imports
import pygame

from entities.pixel_entity import PixelEntity
from particles.particle import Particle

# Custom data types

# Global constants


class Scene:

    """
    Scene is a class that stores information on when and where to spawn
    various entities and particles.
    """

    def __init__(
        self,
        background_color: pygame.Color,
        entity_dict: dict[int, list[PixelEntity]] = {},
        particle_dict: dict[int, list[Particle]] = {},
    ):
        self.entity_dict = entity_dict
        self.particle_dict = particle_dict
        if len(self.entity_dict) == 0 and len(self.particle_dict) == 0:
            self.duration = 0
        elif len(self.entity_dict) == 0:
            self.duration = max(self.particle_dict.keys())
        elif len(self.particle_dict) == 0:
            self.duration = max(self.entity_dict.keys())
        else:
            self.duration = max(
                max(self.entity_dict.keys()), max(self.particle_dict.keys())
            )
        self.time_elapsed = 0
        self.background_color = background_color

    def update_entities_to_spawn(self) -> tuple[list[PixelEntity], bool]:
        if self.time_elapsed <= self.duration:
            if self.time_elapsed in self.entity_dict:
                entities = self.entity_dict[self.time_elapsed]
            else:
                entities = []
            self.time_elapsed += 1
            still_active = True
        else:
            entities = []
            still_active = False
        return entities, still_active

    def update_particles_to_spawn(self) -> tuple[list[Particle], bool]:
        if self.time_elapsed <= self.duration:
            if self.time_elapsed in self.particle_dict:
                particles = self.particle_dict[self.time_elapsed]
            else:
                particles = []
            still_active = True
        else:
            particles = []
            still_active = False
        return particles, still_active

    def is_complete(self) -> bool:
        return self.time_elapsed > self.duration
