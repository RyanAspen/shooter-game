import math
import random

import pygame
from basic_entity import BasicEntity
import constants
from particle import Particle
from scene import Scene

speed = 50


class ParticleScene(Scene):
    def __init__(self):
        background_color = pygame.Color(0, 20, 200)
        particle_dict = dict()
        for time in range(1, speed * 10 + 2, speed):
            particle_dict[time] = get_particles(300)
        super().__init__(particle_dict=particle_dict, background_color=background_color)


def get_particles(count) -> list[Particle]:
    particles = []  # type: list[Particle]
    random_position = [
        random.randint(100, constants.width - 100),
        random.randint(100, constants.height - 100),
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
