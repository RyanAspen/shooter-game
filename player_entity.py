import random
import pygame
from moving_entity import MovingEntity
from pixel_frame import PixelFrame

point = list[int, int]

size = 10
speed_scale = 2


class PlayerEntity(MovingEntity):

    """
    PlayerEntity is an entity that is controlled by user input
    """

    def __init__(self, spawn_point: point):
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

        frame_dict = {
            "Normal": frame_normal,
            "Left": frame_left,
            "Right": frame_right,
            "Up": frame_up,
            "Down": frame_down,
        }

        super().__init__(
            frame_dict=frame_dict,
            spawn_point=spawn_point,
            starting_frame_key="Normal",
            name="Player Entity",
            initial_speed=[0, 0],
            layer_priority=0,
        )

    def update(self, window: pygame.Surface, events: list[pygame.event.Event]):
        new_speed = self.speed
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    self.change_frame("Down")
                    new_speed = [0, speed_scale]
                elif event.key == pygame.K_UP:
                    self.change_frame("Up")
                    new_speed = [0, -speed_scale]
                elif event.key == pygame.K_LEFT:
                    self.change_frame("Left")
                    new_speed = [-speed_scale, 0]
                elif event.key == pygame.K_RIGHT:
                    self.change_frame("Right")
                    new_speed = [speed_scale, 0]
            elif event.type == pygame.KEYUP:
                self.change_frame("Normal")
                new_speed = [0, 0]
        self.change_speed_absolute(new_speed)
        super().update(window, events)
