import pygame

rect_color_pair = tuple[pygame.Rect, pygame.Color]


class PixelFrame:

    """
    PixelFrame is an animation frame of a PixelEntity object
    """

    def __init__(
        self, visual_rects: list[rect_color_pair], hitboxes: list[pygame.Rect]
    ):
        self.visual_rects = visual_rects
        self.hitboxes = hitboxes
