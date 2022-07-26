from typing import TypeVar
import constants
import sys
import time
import pygame
from basic_entity import BasicEntity
from basic_projectile import BasicProjectile
from entity_collision_manager import EntityCollisionManager
from entity_creation_request import EntityCreationRequest
from pixel_entity import PixelEntity
from player_entity import PlayerEntity
from scene import Scene

E = TypeVar("E", bound=PixelEntity)


class Screen:
    def __init__(self, scenes: list[Scene]):
        pygame.init()
        size = constants.width, constants.height
        self.window = pygame.display.set_mode(size)
        self.entities = []  # type: list[PixelEntity]

        self.scenes = scenes

        self.active_scene = None

        player = PlayerEntity([int(constants.width / 2), int(constants.height - 20)])
        self.entities.append(player)
        player.spawn()

        # Add entities that care about collisions here
        self.collision_manager = EntityCollisionManager(self.entities)

    def activate_scene(self):
        if len(self.scenes) > 0:
            self.active_scene = self.scenes[0]
            self.scenes = self.scenes[1:]

    def update(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                sys.exit()

        if (
            self.are_no_enemies()
            and self.active_scene is not None
            and self.active_scene.is_complete()
        ):
            self.active_scene = None

        if self.are_no_enemies() and len(self.scenes) > 0 and self.active_scene is None:
            self.activate_scene()

        if self.active_scene is None:
            return

        self.window.fill(self.active_scene.background_color)

        collisions = self.collision_manager.update_collisions()

        new_entities, scene_active = self.active_scene.update_entities_to_spawn()
        self.add_entities(new_entities)

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

    def add_entity(self, entity: E):
        self.entities.append(entity)
        self.entities = sort_entities_by_layer_priority(self.entities)
        self.collision_manager.add_entity(entity)
        entity.spawn()

    def add_entities(self, entities: list[E]):
        self.entities += entities
        self.entities = sort_entities_by_layer_priority(self.entities)
        for entity in entities:
            self.collision_manager.add_entity(entity)
            entity.spawn()

    def remove_entity(self, entity: PixelEntity):
        self.entities.remove(entity)

    def are_no_enemies(self):
        for entity in self.entities:
            if (
                entity.name == "Enemy Entity"
                or entity.name == "Enemy Projectile"
                or entity.name == "Basic Entity"
            ):
                return False
        return True


def sort_entities_by_layer_priority(entities: list[E]):
    entities.sort(key=lambda x: x.layer_priority)
    return entities
