import pygame
from pixel_entity import PixelEntity


class Scene:

    """
    A Scene contains, among other things, a dictionary where each key is a frame number and each value
    is a list of entities that should be spawned at the corresponding frame number.
    """

    def __init__(
        self, entity_dict: dict[int, list[PixelEntity]], background_color: pygame.Color
    ):
        self.entity_dict = entity_dict
        self.duration = max(self.entity_dict.keys())
        self.time_elapsed = 0
        self.background_color = background_color

    def update_entities_to_spawn(self):
        if self.time_elapsed <= self.duration:
            if self.time_elapsed in self.entity_dict:
                entities = self.entity_dict[self.time_elapsed]
            else:
                entities = []
            self.time_elapsed += 1
            still_active = True
        else:
            entities = []
            still_active = False
        return entities, still_active

    def is_complete(self):
        return self.time_elapsed > self.duration
