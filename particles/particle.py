# Imports
import helpers.constants as constants
import pygame

# Custom data types
point = list[float]
speed = list[float]


class Particle:

    """
    Particle is a very simplified entity that is a single one pixel square that
    only interacts with specific entities and disappates after a specified time.
    """

    def __init__(
        self,
        initial_position: point,
        initial_speed: speed,
        decay_time: int,
        color: pygame.Color,
        acceleration_factor: float = 1.0,
        intensity_change_factor: float = 1.0,
        gravity: float = 0.0,
    ):
        self.position = initial_position.copy()
        self.previous_position = initial_position.copy()
        self.speed = initial_speed.copy()
        self.time_left = decay_time
        self.color = color
        self.acceleration_factor = acceleration_factor
        self.intensity_change_factor = intensity_change_factor
        self.gravity = gravity

    def update(self, window: pygame.Surface) -> bool:
        self.position[0] += self.speed[0]
        self.position[1] += self.speed[1]
        self.time_left -= 1
        pygame.draw.rect(
            window,
            self.color,
            pygame.Rect(int(self.position[0]), int(self.position[1]), 1, 1),
        )
        self.speed[1] += self.gravity
        self.speed[0] *= self.acceleration_factor
        self.speed[1] *= self.acceleration_factor
        self.color = pygame.Color(
            int(self.color.r * self.intensity_change_factor),
            int(self.color.g * self.intensity_change_factor),
            int(self.color.b * self.intensity_change_factor),
        )

        return self.time_left <= 0 or (
            self.position[0] < 0
            or self.position[0] > constants.width
            or self.position[1] < 0
            or self.position[1] > constants.height
        )
