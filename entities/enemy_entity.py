# Imports
import helpers.constants as constants
import pygame

from helpers.entity_creation_request import EntityCreationRequest
from helpers.pixel_frame import PixelFrame
from entities.pixel_entity import PixelEntity

# Custom data types
point = list[int]

# Global constants
shoot_interval = 40
size = 40
wait_until_delete = 20


class EnemyEntity(PixelEntity):

    """
    EnemyEntity is a PixelEntity that moves from left to right and shoots EnemyProjectiles
    """

    def __init__(self, spawn_point: point):
        self.shoot_timer = shoot_interval

        visual_rects_1 = [(pygame.Rect(0, 0, size, size), pygame.Color(120, 120, 255))]
        hitboxes_1 = [pygame.Rect(0, 0, size, size)]
        frame_1 = PixelFrame(visual_rects=visual_rects_1, hitboxes=hitboxes_1)
        visual_rects_2 = [
            (pygame.Rect(0, 0, size, size), pygame.Color(0, 0, 155)),
        ]
        hitboxes_2 = [pygame.Rect(0, 0, size, size)]
        frame_2 = PixelFrame(visual_rects=visual_rects_2, hitboxes=hitboxes_2)
        frame_dict = {"Normal": frame_1, "Hit": frame_2}
        self.timer_to_delete = wait_until_delete
        super().__init__(
            frame_dict=frame_dict,
            spawn_point=spawn_point,
            starting_frame_key="Normal",
            name="Enemy Entity",
            initial_speed=[2, 0],
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

        if self.current_point[0] < 100:
            self.change_speed_absolute([2, 0])
        elif self.current_point[0] > constants.width - 100:
            self.change_speed_absolute([-2, 0])

        if self.shoot_timer <= 0:
            self.shoot_timer = shoot_interval
            projectile_spawn_point = self.current_point.copy()
            projectile_spawn_point[0] += size / 2
            projectile_spawn_point[1] += size
            self.entity_creation_request = EntityCreationRequest(
                "Enemy Projectile", projectile_spawn_point
            )
        else:
            self.shoot_timer -= 1
            self.entity_creation_request = None

        self.move_relative(self.speed)
        self.handle_attributes(window, events, collisions)
        self.draw(window)
