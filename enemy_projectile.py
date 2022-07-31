from typing import Optional
import pygame
from entity_creation_request import EntityCreationRequest
from pixel_entity import PixelEntity
from pixel_frame import PixelFrame
import constants

point = list[int]

size = 5


class EnemyProjectile(PixelEntity):

    """
    PlayerEntity is an entity that is controlled by user input
    """

    def __init__(self, spawn_point: point):
        self.explosion_time = 0
        self.explosion_stage = 0
        self.counting_down = False

        visual_rects_normal = [
            (pygame.Rect(0, 0, size, size * 2), pygame.Color(255, 255, 0)),
            (pygame.Rect(0, size * 2, size, size * 3), pygame.Color(200, 0, 0)),
        ]
        hitboxes_normal = [pygame.Rect(0, 0, size * 2, size * 2)]
        frame_normal = PixelFrame(
            visual_rects=visual_rects_normal, hitboxes=hitboxes_normal
        )

        visual_rects_exploding_1 = [
            (pygame.Rect(0, 0, size * 5, size * 5), pygame.Color(0, 100, 255)),
            (
                pygame.Rect(size, size, size * 3, size * 3),
                pygame.Color(0, 255, 255),
            ),
        ]
        hitboxes_exploding_1 = []  # type: list[pygame.Rect]
        frame_exploding_1 = PixelFrame(
            visual_rects=visual_rects_exploding_1, hitboxes=hitboxes_exploding_1
        )

        visual_rects_exploding_2 = [
            (pygame.Rect(0, 0, size * 7, size * 7), pygame.Color(0, 100, 255)),
            (pygame.Rect(size, size, size * 5, size * 5), pygame.Color(0, 255, 255)),
        ]
        hitboxes_exploding_2 = []  # type: list[pygame.Rect]
        frame_exploding_2 = PixelFrame(
            visual_rects=visual_rects_exploding_2, hitboxes=hitboxes_exploding_2
        )

        visual_rects_exploding_3 = [
            (pygame.Rect(0, 0, size * 9, size * 9), pygame.Color(0, 100, 255)),
            (pygame.Rect(size, size, size * 7, size * 7), pygame.Color(0, 255, 255)),
        ]
        hitboxes_exploding_3 = []  # type: list[pygame.Rect]
        frame_exploding_3 = PixelFrame(
            visual_rects=visual_rects_exploding_3, hitboxes=hitboxes_exploding_3
        )

        frame_dict = {
            "Normal": frame_normal,
            "Exploding/1": frame_exploding_1,
            "Exploding/2": frame_exploding_2,
            "Exploding/3": frame_exploding_3,
        }

        super().__init__(
            frame_dict=frame_dict,
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
        collisions: list[tuple[str, point, point]],
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
                        self.change_frame("Exploding/1")
                    elif self.explosion_stage == 2:
                        self.change_frame("Exploding/2")
                    else:
                        self.change_frame("Exploding/3")
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
