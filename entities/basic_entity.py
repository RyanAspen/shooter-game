# Imports
import random
import pygame

from entities.pixel_entity import PixelEntity
from helpers.pixel_frame import PixelFrame

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
        visual_rects_1 = [(pygame.Rect(0, 0, size, size), pygame.Color(255, 255, 255))]
        hitboxes_1 = [pygame.Rect(0, 0, size, size)]
        frame_1 = PixelFrame(visual_rects=visual_rects_1, hitboxes=hitboxes_1)
        visual_rects_2 = [
            (pygame.Rect(0, 0, size, size), pygame.Color(0, 0, 255)),
        ]
        hitboxes_2 = [pygame.Rect(0, 0, size, size)]
        frame_2 = PixelFrame(visual_rects=visual_rects_2, hitboxes=hitboxes_2)
        frame_dict = {"Normal": frame_1, "Hit": frame_2}
        self.timer_to_delete = wait_until_delete
        speed_left = 0
        speed_top = 0
        while speed_left == 0 or speed_top == 0:
            speed_left = random.randint(-5, 5)
            speed_top = random.randint(-5, 5)
        initial_speed = [speed_left, speed_top]
        super().__init__(
            frame_dict=frame_dict,
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
        collisions: list[tuple[str, point, point]] = [],
    ):
        if self.current_frame_key == "Normal":
            if self.is_colliding_with_name(collisions, "Basic Projectile"):
                self.change_frame("Hit")
        elif self.timer_to_delete > 0:
            self.timer_to_delete -= 1
        else:
            self.should_delete = True

        self.move_relative(self.speed)
        self.handle_attributes(window, events, collisions)
        self.draw(window)