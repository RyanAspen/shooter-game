# Imports
import constants as constants
import pygame

from entities.pixel_entity import PixelEntity

# Custom data types
point = list[int]

# Global constants
size = 5


class EnemyProjectile(PixelEntity):

    """
    PlayerEntity is an entity that is controlled by user input
    """

    def __init__(self, spawn_point: point):
        self.explosion_time = 0
        self.explosion_stage = 0
        self.counting_down = False
        super().__init__(
            spawn_point=spawn_point,
            starting_frame_key="Normal",
            name="Enemy Projectile",
            initial_speed=[0, 5],
            layer_priority=2,
        )

    def update(
        self,
        window: pygame.Surface,
        events: list[pygame.event.Event],
        collisions: list[tuple[str, point]],
    ):
        if self.current_point[1] > constants.height:
            self.should_delete = True
        if self.explosion_stage == 0 and self.is_colliding_with_name(
            collisions, "Player Entity"
        ):
            self.counting_down = True
        if self.counting_down:
            self.change_speed_absolute([0, 0])
            if self.explosion_time <= 0:
                if self.explosion_stage >= 3:
                    self.should_delete = True
                else:
                    self.explosion_stage += 1
                    self.explosion_time = 10
                    if self.explosion_stage == 1:
                        self.change_frame("Exploding-1")
                    elif self.explosion_stage == 2:
                        self.change_frame("Exploding-2")
                    else:
                        self.change_frame("Exploding-3")
            else:
                self.explosion_time -= 1

        self.move_relative(self.speed)
        new_should_delete, new_entity_creation_request = self.handle_attributes(
            window, events, collisions
        )
        if new_should_delete:
            self.should_delete = True
        if new_entity_creation_request is not None:
            self.entity_creation_request = new_entity_creation_request
        self.draw(window)
