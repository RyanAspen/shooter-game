import pygame
from entity_creation_request import EntityCreationRequest
from pixel_entity import PixelEntity
from pixel_frame import PixelFrame

speed = list[int]
point = list[int]


class MovingEntity(PixelEntity):
    def __init__(
        self,
        frame_dict: dict[str, PixelFrame],
        spawn_point: point,
        starting_frame_key: str,
        name: str,
        initial_speed: speed,
        layer_priority: int,
    ):
        super().__init__(
            frame_dict=frame_dict,
            spawn_point=spawn_point,
            starting_frame_key=starting_frame_key,
            name=name,
            layer_priority=layer_priority,
        )
        self.speed = initial_speed

    def update(
        self,
        window: pygame.Surface,
        events: list[pygame.event.Event],
        collisions: list[str],
    ):
        self.move_relative(self.speed)
        super().update(window, events, collisions)

    def change_speed_relative(self, speed_change):
        self.speed[0] += speed_change[0]
        self.speed[1] += speed_change[1]

    def change_speed_absolute(self, new_speed):
        self.speed[0] = new_speed[0]
        self.speed[1] = new_speed[1]
