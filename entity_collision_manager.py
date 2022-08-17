# Imports
from entities.pixel_entity import PixelEntity
from typing import TypeVar

# Custom data types
E = TypeVar("E", bound=PixelEntity)
point = list[float]

# Global constants


class EntityCollisionManager:

    """
    EntityCollisionManager is a class that continuously checks for entity collisions and outputs a set of collisions
    """

    def __init__(self, entities: list[E] = []):
        self.entities = entities

    def add_entity(self, entity: E):
        self.entities.append(entity)

    def remove_entity(self, entity: E):
        self.entities.remove(entity)

    # Returns a dictionary where keys are entity ids and values are lists of entity names that collide with the entity from the id
    # Run this once per frame
    def update_collisions(self) -> dict[int, list[tuple[str, point]]]:
        new_collisions = dict()
        for entity1 in self.entities:
            for entity2 in self.entities:
                if are_colliding(entity1, entity2):
                    collision_tuple_1 = (
                        entity2.name,
                        entity2.current_point,
                    )
                    collision_tuple_2 = (
                        entity1.name,
                        entity1.current_point,
                    )
                    if entity1 not in new_collisions:
                        new_collisions[entity1.id] = [collision_tuple_1]
                    else:
                        new_collisions[entity1.id].append(collision_tuple_1)
                    if entity2 not in new_collisions:
                        new_collisions[entity2.id] = [collision_tuple_2]
                    else:
                        new_collisions[entity2.id].append(collision_tuple_2)
        return new_collisions


def are_colliding(entity_1: PixelEntity, entity_2: PixelEntity) -> bool:
    if entity_1.id == entity_2.id:
        return False

    for rect1 in entity_1.current_frame.hitboxes:
        for rect2 in entity_2.current_frame.hitboxes:
            rect1_moved = rect1.copy()
            rect1_moved.left += int(entity_1.current_point[0])
            rect1_moved.top += int(entity_1.current_point[1])

            rect2_moved = rect2.copy()
            rect2_moved.left += int(entity_2.current_point[0])
            rect2_moved.top += int(entity_2.current_point[1])

            if rect1_moved.colliderect(rect2_moved):
                return True
    return False
