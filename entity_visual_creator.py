# Imports
import constants
import os
import pygame

# Custom data types
visual_info = pygame.Surface
hitbox_info = list[pygame.Rect]
scaling_info = tuple[int]
frame_info = tuple[visual_info, scaling_info, hitbox_info]
entity_info = dict[str, frame_info]
entities_dict = dict[str, entity_info]


class EntityVisualCreator:
    """
    EntityVisualCreator is a class that takes .jpeg pixel maps and creates
    visual representations of entities that work with pygame
    """

    def __init__(self):
        pygame.init()
        pygame.display.set_mode(constants.size)
        self.entity_visuals_folder = os.path.join(os.getcwd(), "data", "entity_visuals")
        if not os.path.exists(self.entity_visuals_folder):
            os.mkdir(self.entity_visuals_folder)
        self.image_dict = dict()  # type: entities_dict
        for entity_name in os.listdir(self.entity_visuals_folder):
            entity_information = dict()  # type: entity_info
            for entity_frame_name in os.listdir(
                os.path.join(self.entity_visuals_folder, entity_name)
            ):
                entity_img = pygame.image.load(
                    os.path.join(
                        self.entity_visuals_folder,
                        entity_name,
                        entity_frame_name,
                        "image.png",
                    )
                )
                entity_text_file = open(
                    os.path.join(
                        self.entity_visuals_folder,
                        entity_name,
                        entity_frame_name,
                        "dimensions.txt",
                    )
                )

                index = 0
                hitboxes = []  # type: hitbox_info
                for line in entity_text_file:
                    if index == 0:
                        # The first line holds image scaling information
                        # Format: "width height"
                        raw_scaling_info = line
                        width = int(raw_scaling_info.split()[0])
                        height = int(raw_scaling_info.split()[1])
                        entity_img = pygame.transform.scale(entity_img, (width, height))
                        entity_img = pygame.Surface.convert(entity_img)
                        scaling = (width, height)

                    else:
                        # The remaining lines holds hitbox information
                        # Format: "left top width height"
                        raw_hitbox_info = line
                        left = int(raw_hitbox_info.split()[0])
                        top = int(raw_hitbox_info.split()[1])
                        width = int(raw_hitbox_info.split()[2])
                        height = int(raw_hitbox_info.split()[3])
                        hitboxes.append(pygame.Rect(left, top, width, height))

                    index += 1

                frame_information = (entity_img, scaling, hitboxes)
                entity_information[entity_frame_name] = frame_information
            self.image_dict[entity_name] = entity_information

    def get_entity_frame_names(self, entity_name: str) -> list[str]:
        return self.image_dict[entity_name].keys()

    def get_entity_info(self, entity_name: str, frame_name: str) -> visual_info:
        return self.image_dict[entity_name][frame_name][0]

    def get_scaling_info(self, entity_name: str, frame_name: str) -> scaling_info:
        return self.image_dict[entity_name][frame_name][1]

    def get_hitbox_info(self, entity_name: str, frame_name: str) -> hitbox_info:
        hitboxes = []
        for rect in self.image_dict[entity_name][frame_name][2]:
            hitboxes.append(rect.copy())
        return hitboxes


"""
        hitboxes = []
        for rect in self.image_dict[entity_name][frame_name][0]:
            hitboxes.append(rect.copy())
        return hitboxes
"""
