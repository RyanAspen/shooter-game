import pygame
from pixel_entity import PixelEntity
from pixel_frame import PixelFrame

point = tuple[int, int]

class BasicEntity(PixelEntity):

    """
    BasicEntity is a PixelEntity that is just a white square with no other PixelFrames
    """
    def __init__(self, spawn_point : point):
        visual_rects = [
            (pygame.Rect(0,0,20,20), pygame.Color(255,255,255))
        ]
        hitboxes = [
            pygame.Rect(0,0,20,20)
        ]
        frame = PixelFrame(visual_rects = visual_rects, hitboxes = hitboxes)
        frame_dict = {
            "Normal" : frame
        }
        super().__init__(frame_dict, spawn_point, "Normal")