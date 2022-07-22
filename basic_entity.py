import pygame
from pixel_entity import PixelEntity
from pixel_frame import PixelFrame

point = tuple[int, int]

size = 10

class BasicEntity(PixelEntity):

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
        super().__init__(frame_dict, spawn_point, "Normal", "Basic Entity")