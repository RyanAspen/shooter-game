# TODO Pathing is very bugged
from typing import Optional
import pygame
from entities.pixel_entity import PixelEntity
from entity_creation_request import EntityCreationRequest

# Custom data types
point = list[int]
path = list[point]

# Global constants
shoot_interval = 40
size = 40
movement_interval = 120
wait_until_delete = 20


class PathedEnemyEntity(PixelEntity):

    """
    PathedEnemyEntity is a PixelEntity that moves according to a predefined path and shoots EnemyProjectiles
    """

    def __init__(self, spawn_point: point, path_to_take: path):
        self.path_to_take = path_to_take
        self.point_to_reach = None
        self.shoot_timer = shoot_interval
        self.reached_end = False
        self.time_until_reached = movement_interval
        self.timer_to_delete = wait_until_delete
        super().__init__(
            spawn_point=spawn_point,
            starting_frame_key="Normal",
            name="Pathed Enemy Entity",
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
                self.change_speed_absolute([0, 0])
            if not self.reached_end and self.point_to_reach is not None:
                if (
                    self.current_point[0] == self.point_to_reach[0]
                    and self.current_point[1] == self.point_to_reach[1]
                ) or self.time_until_reached <= 0:
                    self.point_to_reach = None

            if self.point_to_reach == None:
                if len(self.path_to_take) > 0:
                    self.time_until_reached = movement_interval
                    self.point_to_reach = self.path_to_take[0]
                    self.path_to_take = self.path_to_take[1:]
                    self.change_speed_absolute(
                        self.get_speed_to_reach_position(
                            self.point_to_reach, movement_interval
                        )
                    )
                else:
                    self.reached_end = True
                    self.change_speed_absolute([0, 0])
            else:
                self.time_until_reached -= 1

            if self.shoot_timer <= 0:
                self.shoot_timer = shoot_interval
                projectile_spawn_point = self.current_point.copy()
                projectile_spawn_point[0] += size / 2
                projectile_spawn_point[1] += size
                self.entity_creation_request = EntityCreationRequest(
                    "Enemy Projectile", projectile_spawn_point
                )  # type: Optional[EntityCreationRequest]
            else:
                self.shoot_timer -= 1
                self.entity_creation_request = None

        elif self.timer_to_delete > 0:
            self.timer_to_delete -= 1
        else:
            self.should_delete = True

        # print("__________" + str(self.id))
        # print("Hitboxes = " + str(self.current_frame.hitboxes))
        # print("Current Point = " + str(self.current_point))
        # print("==========" + str(self.id))

        self.move_relative(self.speed)
        self.handle_attributes(window, events, collisions)
        self.draw(window)
