import os


class EntityVisualCreator:
    """
    EntityVisualCreator is a class that takes .jpeg pixel maps and creates
    visual representations of entities that work with pygame
    """

    def __init__(self):
        self.entity_visuals_folder = os.path.join(os.getcwd(), "data", "entity_visuals")
        if not os.path.exists(self.entity_visuals_folder):
            os.mkdir(self.entity_visuals_folder)
