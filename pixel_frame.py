# Imports
import pygame

# Custom data types


class PixelFrame:

    """
    PixelFrame is an animation frame of a PixelEntity object that also holds
    the PixelEntity's hitboxes in that frame
    """

    def __init__(
        self, image: pygame.Surface, hitboxes: list[pygame.Rect]
    ):
        self.image = image
        self.hitboxes = hitboxes
