# Imports
import pygame

from entities.pixel_entity import PixelEntity
from helpers.entity_creation_request import EntityCreationRequest
from helpers.pixel_frame import PixelFrame
from typing import Optional

# Custom data types
point = list[int]

# Global constants
size = 10
speed_scale = 5


class PlayerEntity(PixelEntity):

    """
    PlayerEntity is an entity that is controlled by user input
    """

    def __init__(self, spawn_point: point):
        self.up = 0
        self.down = 0
        self.left = 0
        self.right = 0

        visual_rects_normal = [
            (pygame.Rect(0, 0, size * 3, size * 3), pygame.Color(255, 255, 255)),
            (pygame.Rect(size, size, size, size), pygame.Color(255, 0, 0)),
        ]
        hitboxes_normal = [pygame.Rect(0, 0, size * 3, size * 3)]
        frame_normal = PixelFrame(
            visual_rects=visual_rects_normal, hitboxes=hitboxes_normal
        )

        visual_rects_left = [
            (pygame.Rect(0, 0, size * 3, size * 3), pygame.Color(255, 255, 255)),
            (pygame.Rect(0, size, size, size), pygame.Color(255, 0, 0)),
        ]
        hitboxes_left = [pygame.Rect(0, 0, size * 3, size * 3)]
        frame_left = PixelFrame(visual_rects=visual_rects_left, hitboxes=hitboxes_left)

        visual_rects_right = [
            (pygame.Rect(0, 0, size * 3, size * 3), pygame.Color(255, 255, 255)),
            (pygame.Rect(size * 2, size, size, size), pygame.Color(255, 0, 0)),
        ]
        hitboxes_right = [pygame.Rect(0, 0, size * 3, size * 3)]
        frame_right = PixelFrame(
            visual_rects=visual_rects_right, hitboxes=hitboxes_right
        )

        visual_rects_up = [
            (pygame.Rect(0, 0, size * 3, size * 3), pygame.Color(255, 255, 255)),
            (pygame.Rect(size, 0, size, size), pygame.Color(255, 0, 0)),
        ]
        hitboxes_up = [pygame.Rect(0, 0, size * 3, size * 3)]
        frame_up = PixelFrame(visual_rects=visual_rects_up, hitboxes=hitboxes_up)

        visual_rects_down = [
            (pygame.Rect(0, 0, size * 3, size * 3), pygame.Color(255, 255, 255)),
            (pygame.Rect(size, size * 2, size, size), pygame.Color(255, 0, 0)),
        ]
        hitboxes_down = [pygame.Rect(0, 0, size * 3, size * 3)]
        frame_down = PixelFrame(visual_rects=visual_rects_down, hitboxes=hitboxes_down)

        visual_rects_left_down = [
            (pygame.Rect(0, 0, size * 3, size * 3), pygame.Color(255, 255, 255)),
            (pygame.Rect(0, size * 2, size, size), pygame.Color(255, 0, 0)),
        ]
        hitboxes_left_down = [pygame.Rect(0, 0, size * 3, size * 3)]
        frame_left_down = PixelFrame(
            visual_rects=visual_rects_left_down, hitboxes=hitboxes_left_down
        )

        visual_rects_left_up = [
            (pygame.Rect(0, 0, size * 3, size * 3), pygame.Color(255, 255, 255)),
            (pygame.Rect(0, 0, size, size), pygame.Color(255, 0, 0)),
        ]
        hitboxes_left_up = [pygame.Rect(0, 0, size * 3, size * 3)]
        frame_left_up = PixelFrame(
            visual_rects=visual_rects_left_up, hitboxes=hitboxes_left_up
        )

        visual_rects_right_down = [
            (pygame.Rect(0, 0, size * 3, size * 3), pygame.Color(255, 255, 255)),
            (pygame.Rect(size * 2, size * 2, size, size), pygame.Color(255, 0, 0)),
        ]
        hitboxes_right_down = [pygame.Rect(0, 0, size * 3, size * 3)]
        frame_right_down = PixelFrame(
            visual_rects=visual_rects_right_down, hitboxes=hitboxes_right_down
        )

        visual_rects_right_up = [
            (pygame.Rect(0, 0, size * 3, size * 3), pygame.Color(255, 255, 255)),
            (pygame.Rect(size * 2, 0, size, size), pygame.Color(255, 0, 0)),
        ]
        hitboxes_right_up = [pygame.Rect(0, 0, size * 3, size * 3)]
        frame_right_up = PixelFrame(
            visual_rects=visual_rects_right_up, hitboxes=hitboxes_right_up
        )

        frame_dict = {
            "Normal": frame_normal,
            "Left": frame_left,
            "Right": frame_right,
            "Up": frame_up,
            "Down": frame_down,
            "Left/Down": frame_left_down,
            "Left/Up": frame_left_up,
            "Right/Down": frame_right_down,
            "Right/Up": frame_right_up,
        }

        super().__init__(
            frame_dict=frame_dict,
            spawn_point=spawn_point,
            starting_frame_key="Normal",
            name="Player Entity",
            initial_speed=[0, 0],
            layer_priority=1,
        )

    def update(
        self,
        window: pygame.Surface,
        events: list[pygame.event.Event],
        collisions: list[tuple[str, point, point]],
    ) -> tuple[bool, Optional[EntityCreationRequest]]:
        if self.is_colliding_with_name(collisions, "Enemy Projectile"):
            should_be_deleted = True
        else:
            should_be_deleted = False
        entity_creation_request = None
        new_speed = self.speed
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    self.down = 1
                if event.key == pygame.K_UP:
                    self.up = 1
                elif event.key == pygame.K_LEFT:
                    self.left = 1
                elif event.key == pygame.K_RIGHT:
                    self.right = 1
                elif event.key == pygame.K_SPACE:
                    projectile_spawn_point = self.current_point.copy()
                    projectile_spawn_point[0] += 5
                    projectile_spawn_point[1] -= 15
                    entity_creation_request = EntityCreationRequest(
                        name="Basic Projectile", spawn_point=projectile_spawn_point
                    )

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    self.down = 0
                if event.key == pygame.K_UP:
                    self.up = 0
                elif event.key == pygame.K_LEFT:
                    self.left = 0
                elif event.key == pygame.K_RIGHT:
                    self.right = 0
        if self.up > 0 and self.down == 0:
            if self.left > 0 and self.right == 0:
                self.change_frame("Left/Up")
                new_speed = [-speed_scale, -speed_scale]
            elif self.left == 0 and self.right > 0:
                self.change_frame("Right/Up")
                new_speed = [speed_scale, -speed_scale]
            else:
                self.change_frame("Up")
                new_speed = [0, -speed_scale]
        elif self.up == 0 and self.down > 0:
            if self.left > 0 and self.right == 0:
                self.change_frame("Left/Down")
                new_speed = [-speed_scale, speed_scale]
            elif self.left == 0 and self.right > 0:
                self.change_frame("Right/Down")
                new_speed = [speed_scale, speed_scale]
            else:
                self.change_frame("Down")
                new_speed = [0, speed_scale]
        else:
            if self.left > 0 and self.right == 0:
                self.change_frame("Left")
                new_speed = [-speed_scale, 0]
            elif self.left == 0 and self.right > 0:
                self.change_frame("Right")
                new_speed = [speed_scale, 0]
            else:
                self.change_frame("Normal")
                new_speed = [0, 0]
        self.change_speed_absolute(new_speed)
        self.should_delete = should_be_deleted
        self.entity_creation_request = entity_creation_request
        self.move_relative(self.speed)
        new_should_delete, new_entity_creation_request = self.handle_attributes(
            window, events, collisions
        )
        if new_should_delete:
            self.should_delete = True
        if new_entity_creation_request is not None:
            self.entity_creation_request = new_entity_creation_request
        self.draw(window)
