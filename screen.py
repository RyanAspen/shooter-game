import os
from typing import TypeVar
import constants
import sys
import time
import pygame
from basic_entity import BasicEntity
from basic_projectile import BasicProjectile
from enemy_projectile import EnemyProjectile
from entity_collision_manager import EntityCollisionManager
from entity_creation_request import EntityCreationRequest
from particle import Particle
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
        self.particles = []  # type: list[Particle]

        self.scenes = scenes

        self.age = 0

        self.active_scene = None

        self.debug_file_name = "performance_data.txt"
        if os.path.exists(os.path.join(os.getcwd(), self.debug_file_name)):
            os.remove(os.path.join(os.getcwd(), self.debug_file_name))
        self.debug_file = open(os.path.join(os.getcwd(), self.debug_file_name), "w")

        self.debug_file.write("Beginning of debug\n")

        player = PlayerEntity([int(constants.width / 2), int(constants.height - 20)])
        self.entities.append(player)
        player.spawn()

        # Add entities that care about collisions here
        self.collision_manager = EntityCollisionManager()
        for entity in self.entities:
            if not entity.attribute_db.has_attribute(entity.name, "no_interact"):
                self.collision_manager.add_entity(entity)

    def activate_scene(self):
        if len(self.scenes) > 0:
            self.active_scene = self.scenes[0]
            self.scenes = self.scenes[1:]

    def update(self):
        self.age += 1
        time_begin = time.time()
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                sys.exit()
        time_events_end = time.time()
        if (
            len(self.scenes) > 0
            and self.active_scene is not None
            and self.active_scene.is_complete()
        ):
            self.active_scene = None

        if self.are_no_enemies() and len(self.scenes) > 0 and self.active_scene is None:
            self.activate_scene()

        self.window.fill(self.active_scene.background_color)

        time_collisions_begin = time.time()
        collisions = self.collision_manager.update_collisions()
        time_collisions_end = time.time()

        new_entities, scene_active = self.active_scene.update_entities_to_spawn()
        new_particles, _ = self.active_scene.update_particles_to_spawn()
        self.add_entities(new_entities)
        self.add_particles(new_particles)
        time_begin_logic = time.time()
        for entity in self.entities:
            old_point = entity.current_point.copy()

            if entity.id in collisions:
                entity_collisions = collisions[entity.id]
            else:
                entity_collisions = []
            entity.update(self.window, events, entity_collisions)
            if entity.should_delete:
                self.remove_entity(entity)
            if entity.entity_creation_request is not None:
                self.process_entity_creation_request(entity.entity_creation_request)

            entity.previous_point = old_point

        for particle in self.particles:
            if particle.update(self.window):
                self.remove_particle(particle)

        time_end_logic = time.time()
        pygame.display.flip()  # Use .update instead for more optimization
        time_end = time.time()
        time.sleep(0.01)

        update_debug_string = "Update #" + str(self.age) + "\n"
        update_debug_string += "Full update time = " + str(time_end - time_begin) + "\n"
        update_debug_string += (
            "Logic update time = " + str(time_end_logic - time_begin) + "\n"
        )
        update_debug_string += (
            "For loop update time = " + str(time_end_logic - time_begin_logic) + "\n"
        )
        update_debug_string += (
            "Events handling update time = " + str(time_events_end - time_begin) + "\n"
        )
        update_debug_string += (
            "Collisions handling update time = "
            + str(time_collisions_end - time_collisions_begin)
            + "\n"
        )
        self.debug_file.write(update_debug_string)

    def process_entity_creation_request(self, request: EntityCreationRequest):
        if request.name == "Basic Projectile":
            self.add_entity(BasicProjectile(request.spawn_point))
        elif request.name == "Basic Entity":
            self.add_entity(BasicEntity(request.spawn_point))
        elif request.name == "Player Entity":
            self.add_entity(PlayerEntity(request.spawn_point))
        elif request.name == "Enemy Projectile":
            self.add_entity(EnemyProjectile(request.spawn_point))

    def add_entity(self, entity: E):
        self.entities.append(entity)
        self.entities = sort_entities_by_layer_priority(self.entities)
        if not entity.attribute_db.has_attribute(entity.name, "no_interact"):
            self.collision_manager.add_entity(entity)
        entity.spawn()

    def add_entities(self, entities: list[E]):
        self.entities += entities
        self.entities = sort_entities_by_layer_priority(self.entities)
        for entity in entities:
            if not entity.attribute_db.has_attribute(entity.name, "no_interact"):
                self.collision_manager.add_entity(entity)
            entity.spawn()

    def add_particle(self, particle: Particle):
        self.particles.append(particle)

    def add_particles(self, particles: list[Particle]):
        for particle in particles:
            self.particles.append(particle)

    def remove_particle(self, particle: Particle):
        self.particles.remove(particle)

    def remove_entity(self, entity: PixelEntity):
        self.entities.remove(entity)
        self.collision_manager.remove_entity(entity)

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
