# Imports
import pygame

from entity_creation_request import EntityCreationRequest
from pixel_frame import PixelFrame
from pixel_entity import PixelEntity
from typing import Optional

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
        visual_rects_1 = [
            (pygame.Rect(0, 0, size * 5, size * 5), pygame.Color(0, 0, 0)),
            (pygame.Rect(size, size, size * 3, size * 3), pygame.Color(255, 255, 255)),
            (pygame.Rect(size * 2, size * 2, size, size), pygame.Color(255, 0, 0)),
        ]
        hitboxes_1 = [pygame.Rect(0, 0, size * 5, size * 5)]
        frame_1 = PixelFrame(visual_rects=visual_rects_1, hitboxes=hitboxes_1)
        visual_rects_2 = [
            (pygame.Rect(0, 0, size * 5, size * 5), pygame.Color(255, 255, 0)),
        ]
        hitboxes_2 = []  # type: list[pygame.Rect]
        frame_2 = PixelFrame(visual_rects=visual_rects_2, hitboxes=hitboxes_2)
        frame_dict = {"Normal": frame_1, "Hit": frame_2}
        super().__init__(
            frame_dict=frame_dict,
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
