import random
import pygame
from moving_entity import MovingEntity
from pixel_frame import PixelFrame

point = list[int, int]

size = 10

class BasicEntity(MovingEntity):

    """
    BasicEntity is a PixelEntity that is just a white square with no other PixelFrames
    """
    def __init__(self, spawn_point : point):
        visual_rects_1 = [
            (pygame.Rect(0,0,size,size), pygame.Color(255,255,255))
        ]
        hitboxes_1 = [
            pygame.Rect(0,0,size,size)
        ]
        frame_1 = PixelFrame(visual_rects = visual_rects_1, hitboxes = hitboxes_1)
        visual_rects_2 = [
            (pygame.Rect(0,0,size,size), pygame.Color(0,0,255)),
        ]
        hitboxes_2 = [
            pygame.Rect(0,0,size,size)
        ]
        frame_2 = PixelFrame(visual_rects = visual_rects_2, hitboxes = hitboxes_2)
        frame_dict = {
            "Normal" : frame_1,
            "Hit" : frame_2
        }
        speed_left = 0
        speed_top = 0
        while speed_left == 0 or speed_top == 0:
            speed_left = random.randint(-3, 3)
            speed_top = random.randint(-3, 3)
        initial_speed = [speed_left, speed_top]
        super().__init__(frame_dict, spawn_point, "Normal", "Basic Entity", initial_speed)

    def update(self, window : pygame.Surface):
        width = window.get_width()
        height = window.get_height()
        new_speed = self.speed
        if self.current_point[0] < 0:
            new_speed[0] = abs(self.speed[0])
        elif self.current_point[0] > width:
            new_speed[0]= -abs(self.speed[0])
        if self.current_point[1] < 0:
            new_speed[1] = abs(self.speed[1])
        elif self.current_point[1] > height:
            new_speed[1] = -abs(self.speed[1])
        self.change_speed_absolute(new_speed)
        super().update(window)