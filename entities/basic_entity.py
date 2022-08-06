# Imports
import random
import pygame

from entities.pixel_entity import PixelEntity

# Custom data types
point = list[int]

# Global constants
size = 20
wait_until_delete = 5


class BasicEntity(PixelEntity):

    """
    BasicEntity is a PixelEntity that is just a white square with no other PixelFrames
    """

    def __init__(self, spawn_point: point):
        self.timer_to_delete = wait_until_delete
        speed_left = 0
        speed_top = 0
        while speed_left == 0 or speed_top == 0:
            speed_left = random.randint(-5, 5)
            speed_top = random.randint(-5, 5)
        initial_speed = [speed_left, speed_top]
        super().__init__(
            spawn_point=spawn_point,
            starting_frame_key="Normal",
            name="Basic Entity",
            initial_speed=initial_speed,
            layer_priority=0,
        )

    def update(
        self,
        window: pygame.Surface,
        events: list[pygame.event.Event] = [],
        collisions: list[tuple[str, point]] = [],
    ):
        if self.current_frame_key == "Normal":
            if self.is_colliding_with_name(collisions, "Basic Projectile"):
                self.change_frame("Hit")
                self.change_speed_absolute([0, 0])
        elif self.timer_to_delete > 0:
            self.timer_to_delete -= 1
        else:
            self.should_delete = True

        self.move_relative(self.speed)
        self.handle_attributes(window, events, collisions)
        self.draw(window)
