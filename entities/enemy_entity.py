# Imports
from typing import Optional
import constants as constants
import pygame

from entity_creation_request import EntityCreationRequest
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
        self.timer_to_delete = wait_until_delete
        super().__init__(
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

        if self.current_point[0] < 100:
            self.change_speed_absolute([2, 0])
        elif self.current_point[0] > constants.width - 100:
            self.change_speed_absolute([-2, 0])

        if self.shoot_timer <= 0:
            self.shoot_timer = shoot_interval
            projectile_spawn_point = self.current_point.copy()
            projectile_spawn_point[0] += int(size / 2)
            projectile_spawn_point[1] += size
            self.entity_creation_request = EntityCreationRequest(
                "Enemy Projectile", projectile_spawn_point
            )  # type: Optional[EntityCreationRequest]
        else:
            self.shoot_timer -= 1
            self.entity_creation_request = None

        self.move_relative(self.speed)
        self.handle_attributes(window, events, collisions)
        self.draw(window)
