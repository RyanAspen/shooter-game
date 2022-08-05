# Imports
import pygame

from entities.pixel_entity import PixelEntity

# Custom data types
point = list[int]

# Global constants
size = 20


class TargetEntity(PixelEntity):

    """
    TargetEntity is a PixelEntity that is destroyed once shot and doesn't do anything else
    """

    def __init__(self, spawn_point: point):
        self.time_until_delete = 5
        super().__init__(
            spawn_point=spawn_point,
            starting_frame_key="Normal",
            name="Target Entity",
            initial_speed=[0, 0],
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
        else:
            self.time_until_delete -= 1
            if self.time_until_delete <= 0:
                self.should_delete = True
        self.draw(window)
