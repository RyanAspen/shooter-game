import random
import sys
import time
import pygame
from basic_entity import BasicEntity
from entity_collision_manager import EntityCollisionManager
from player_entity import PlayerEntity


class Screen:
    def __init__(self, width, height, base_color):
        pygame.init()
        size = width, height
        self.window = pygame.display.set_mode(size)
        self.base_color = base_color

        self.entities = list()

        # Initial Entity Setup
        for _ in range(500):
            spawn_point = [random.randint(0, width), random.randint(0, height)]
            entity = BasicEntity(spawn_point)
            self.entities.append(entity)
            entity.spawn()

        player = PlayerEntity([width / 2, height / 2])
        self.entities.append(player)
        player.spawn()

        # Add entities that care about collisions here
        self.collision_manager = EntityCollisionManager()

    def update(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                sys.exit()

        self.window.fill(self.base_color)

        self.collision_manager.update_collisions()

        for entity in self.entities:
            entity.update(self.window, events)

        pygame.display.flip()  # Use .update instead for more optimization
        time.sleep(0.01)
