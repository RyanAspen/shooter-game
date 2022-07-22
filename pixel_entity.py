from shutil import move
import pygame
from pixel_frame import PixelFrame

point = tuple[int, int]

class PixelEntity:

    id_counter = 1
    """
    PixelEntity contains at minimum, a set of rectangles describing the pixels of the entity,
    a set of invisible rectangles describing the hitboxes of that entity, 
    and the top-left corner of the entity when initially created
    """
    def __init__(self, frame_dict : dict[str, PixelFrame], spawn_point : point, starting_frame_key : str):
        self.frame_dict = frame_dict
        self.spawn_point = spawn_point
        self.current_point = spawn_point
        self.current_frame_key = starting_frame_key
        self.current_frame = frame_dict[starting_frame_key]
        self.id = PixelEntity.id_counter
        PixelEntity.id_counter += 1

    def spawn(self):
        for frame_key in self.frame_dict:
            if frame_key != self.current_frame_key:
                for rect, _ in self.frame_dict[frame_key].visual_rects:
                    rect.left += self.spawn_point[0]
                    rect.top += self.spawn_point[1]
                for rect in self.frame_dict[frame_key].hitboxes:
                    rect.left += self.spawn_point[0]
                    rect.top += self.spawn_point[1]

        for rect, _ in self.current_frame.visual_rects:
            rect.left += self.spawn_point[0]
            rect.top += self.spawn_point[1]

        for rect in self.current_frame.hitboxes:
            rect.left += self.spawn_point[0]
            rect.top += self.spawn_point[1]
        

    def move_relative(self, movement : tuple[int, int]):
        self.current_point[0] += movement[0]
        self.current_point[1] += movement[1]

        for frame_key in self.frame_dict:
            if frame_key != self.current_frame_key:
                for rect, _ in self.frame_dict[frame_key].visual_rects:
                    rect.left += movement[0]
                    rect.top += movement[1]
                for rect in self.frame_dict[frame_key].hitboxes:
                    rect.left += movement[0]
                    rect.top += movement[1]

        for rect, _ in self.current_frame.visual_rects:
            rect.left += movement[0]
            rect.top += movement[1]

        for rect in self.current_frame.hitboxes:
            rect.left += movement[0]
            rect.top += movement[1]

    def move_absolute(self, new_location : tuple[int, int]):
        self.diff = tuple(map(lambda i, j: j - i, new_location, self.current_point))
        self.current_point = new_location

        for frame_key in self.frame_dict:
            if frame_key != self.current_frame_key:
                for rect, _ in self.frame_dict[frame_key].visual_rects:
                    rect.left += self.diff[0]
                    rect.top += self.diff[1]
                for rect in self.frame_dict[frame_key].hitboxes:
                    rect.left += self.diff[0]
                    rect.top += self.diff[1]

        for rect, _ in self.current_frame.visual_rects:
            rect.left += self.diff[0]
            rect.top += self.diff[1]

        for rect in self.current_frame.hitboxes:
            rect.left += self.diff[0]
            rect.top += self.diff[1]
    
    def draw(self, window : pygame.Surface):
        for rect, color in self.current_frame.visual_rects:
            pygame.draw.rect(window, color, rect)

    def change_frame(self, frame_key : str):
        self.current_frame_key = frame_key
        self.current_frame = self.frame_dict[frame_key]


def are_colliding(entity_1 : PixelEntity, entity_2 : PixelEntity):
    for rect1 in entity_1.current_frame.hitboxes:
        for rect2 in entity_2.current_frame.hitboxes:
            if rect1.colliderect(rect2):
                return True
    return False

def are_different(entity_1 : PixelEntity, entity_2 : PixelEntity):
    return entity_1.id != entity_2.id