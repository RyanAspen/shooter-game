import math
from pixel_entity import PixelEntity

max_dist = 50


class EntityCollisionManager:

    """
    EntityCollisionManager is a class that continuously checks for entity collisions and outputs a set of collisions
    """

    def __init__(self, entities: list[PixelEntity] = []):
        self.entities = entities
        self.collisions = dict()

    def add_entity(self, entity: PixelEntity):
        self.entities.append(entity)

    def remove_entity(self, entity: PixelEntity):
        self.entities.remove(entity)

    # Returns a dictionary where keys are entity ids and values are lists of entity names that collide with the entity from the id
    # Run this once per frame
    def update_collisions(self):
        new_collisions = dict()
        for entity1 in self.entities:
            for entity2 in self.entities:
                if are_different(entity1, entity2):
                    if check_entities_close(entity1, entity2):
                        if are_colliding(entity1, entity2):
                            if entity1 not in new_collisions:
                                new_collisions[entity1.id] = [entity2.name]
                            else:
                                new_collisions[entity1.id].append(entity2.name)
                            if entity2 not in new_collisions:
                                new_collisions[entity2.id] = [entity1.name]
                            else:
                                new_collisions[entity2.id].append(entity1.name)
        self.collisions = new_collisions

    def is_colliding_with_name(self, entity_id: int, collision_name: str = "ALL"):
        for name in self.collisions[entity_id]:
            if collision_name == "ALL" or collision_name == name:
                return True
        return False


def check_entities_close(entity1: PixelEntity, entity2: PixelEntity):
    x_diff = entity2.current_point[0] - entity1.current_point[0]
    y_diff = entity2.current_point[1] - entity1.current_point[1]
    dist = math.sqrt(x_diff * x_diff + y_diff * y_diff)
    return dist < max_dist


def are_colliding(entity_1: PixelEntity, entity_2: PixelEntity):
    for rect1 in entity_1.current_frame.hitboxes:
        for rect2 in entity_2.current_frame.hitboxes:
            if rect1.colliderect(rect2):
                return True
    return False


def are_different(entity_1: PixelEntity, entity_2: PixelEntity):
    return entity_1.id != entity_2.id
