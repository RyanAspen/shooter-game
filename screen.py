import random
import sys
import time
import pygame
from basic_entity import BasicEntity
from basic_projectile import BasicProjectile
from entity_collision_manager import EntityCollisionManager
from entity_creation_request import EntityCreationRequest
from pixel_entity import PixelEntity
from player_entity import PlayerEntity


class Screen:
    def __init__(self, width, height, base_color):
        pygame.init()
        size = width, height
        self.window = pygame.display.set_mode(size)
        self.base_color = base_color

        self.entities = list()

        # Initial Entity Setup
        for _ in range(25):
            spawn_point = [random.randint(0, width), random.randint(0, height)]
            entity = BasicEntity(spawn_point)
            self.entities.append(entity)
            entity.spawn()

        player = PlayerEntity([width / 2, height / 2])
        self.entities.append(player)
        player.spawn()

        self.entities = sort_entities_by_layer_priority(self.entities)

        # Add entities that care about collisions here
        self.collision_manager = EntityCollisionManager(self.entities)

    def update(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                sys.exit()

        self.window.fill(self.base_color)

        collisions = self.collision_manager.update_collisions()

        for entity in self.entities:
            if entity.id in collisions:
                entity_collisions = collisions[entity.id]
            else:
                entity_collisions = []
            should_delete, entity_creation_request = entity.update(
                self.window, events, entity_collisions
            )
            if should_delete:
                self.remove_entity(entity)
            if entity_creation_request is not None:
                self.process_entity_creation_request(entity_creation_request)

        pygame.display.flip()  # Use .update instead for more optimization
        time.sleep(0.01)

    def process_entity_creation_request(self, request: EntityCreationRequest):
        if request.name == "Basic Projectile":
            self.add_entity(BasicProjectile(request.spawn_point))
        elif request.name == "Basic Entity":
            self.add_entity(BasicEntity(request.spawn_point))
        elif request.name == "Player Entity":
            self.add_entity(PlayerEntity(request.spawn_point))

    def add_entity(self, entity: PixelEntity):
        self.entities.append(entity)
        self.entities = sort_entities_by_layer_priority(self.entities)
        self.collision_manager.add_entity(entity)
        entity.spawn()

    def remove_entity(self, entity: PixelEntity):
        self.entities.remove(entity)


def sort_entities_by_layer_priority(entities: list[PixelEntity]):
    entities.sort(key=lambda x: x.layer_priority)
    return entities
