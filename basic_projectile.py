import pygame
from entity_creation_request import EntityCreationRequest
from moving_entity import MovingEntity
from pixel_frame import PixelFrame
from typing import Optional

point = list[int]

size = 10


class BasicProjectile(MovingEntity):

    """
    PlayerEntity is an entity that is controlled by user input
    """

    def __init__(self, spawn_point: point):
        self.explosion_time = 0
        self.explosion_stage = 0
        self.counting_down = False

        visual_rects_normal = [
            (pygame.Rect(0, 0, size, size * 2), pygame.Color(0, 255, 0)),
            (pygame.Rect(0, size * 2, size, size * 3), pygame.Color(255, 0, 0)),
        ]
        hitboxes_normal = [pygame.Rect(0, 0, size * 2, size * 2)]
        frame_normal = PixelFrame(
            visual_rects=visual_rects_normal, hitboxes=hitboxes_normal
        )

        visual_rects_exploding_1 = [
            (pygame.Rect(0, 0, size * 5, size * 5), pygame.Color(255, 100, 0)),
            (
                pygame.Rect(size, size, size * 3, size * 3),
                pygame.Color(255, 255, 0),
            ),
        ]
        hitboxes_exploding_1 = []  # type: list[pygame.Rect]
        frame_exploding_1 = PixelFrame(
            visual_rects=visual_rects_exploding_1, hitboxes=hitboxes_exploding_1
        )

        visual_rects_exploding_2 = [
            (pygame.Rect(0, 0, size * 7, size * 7), pygame.Color(255, 100, 0)),
            (pygame.Rect(size, size, size * 5, size * 5), pygame.Color(255, 255, 0)),
        ]
        hitboxes_exploding_2 = []  # type: list[pygame.Rect]
        frame_exploding_2 = PixelFrame(
            visual_rects=visual_rects_exploding_2, hitboxes=hitboxes_exploding_2
        )

        visual_rects_exploding_3 = [
            (pygame.Rect(0, 0, size * 9, size * 9), pygame.Color(255, 100, 0)),
            (pygame.Rect(size, size, size * 7, size * 7), pygame.Color(255, 255, 0)),
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
            name="Basic Projectile",
            initial_speed=[0, -8],
            layer_priority=2,
        )

    def update(
        self,
        window: pygame.Surface,
        events: list[pygame.event.Event],
        collisions: list[str],
    ) -> tuple[bool, Optional[EntityCreationRequest]]:
        should_delete = False
        if self.current_point[1] < 0:

            should_delete = True
        if self.explosion_stage == 0 and self.is_colliding_with_name(
            collisions, "Basic Entity"
        ):
            self.counting_down = True
        if self.counting_down:
            self.change_speed_absolute([0, 0])
            if self.explosion_time <= 0:
                if self.explosion_stage >= 3:
                    should_delete = True
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
        super().update(window, events, collisions)
        return should_delete, None
