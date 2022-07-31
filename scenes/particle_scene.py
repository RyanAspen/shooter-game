# Imports
import constants as constants
import math
import pygame
import random

from particles.particle import Particle
from scene import Scene

# Custom data types

# Global constants
speed = 50


class ParticleScene(Scene):

    """
    ParticleScene is a scene which spawns several bursts of white particles which
    fall downwards and fade to black.
    """

    def __init__(self):
        background_color = pygame.Color(0, 20, 200)
        particle_dict = dict()
        for time in range(1, speed * 10 + 2, speed):
            particle_dict[time] = get_particles(300)
        super().__init__(particle_dict=particle_dict, background_color=background_color)


def get_particles(count) -> list[Particle]:
    particles = []  # type: list[Particle]
    random_position = [
        (random.random() * (constants.width - 200)) + 100,
        (random.random() * (constants.height - 200)) + 100,
    ]
    for _ in range(count):
        random_dir = random.random() * math.pi * 2
        random_speed = random.random() * 3
        initial_speed = [
            math.sin(random_dir) * random_speed,
            math.cos(random_dir) * random_speed,
        ]
        particle = Particle(
            initial_position=random_position,
            initial_speed=initial_speed,
            decay_time=200,
            color=pygame.Color(255, 255, 255),
            acceleration_factor=0.99,
            intensity_change_factor=0.99,
            gravity=0.05,
        )
        particles.append(particle)
    return particles
