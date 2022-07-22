import random
import sys, pygame
import time
from basic_entity import BasicEntity
from entity_collision_manager import EntityCollisionManager, are_colliding, are_different
from player_entity import PlayerEntity
pygame.init()

size = width, height = 800, 600
black = 0, 0, 0

window = pygame.display.set_mode(size)


entities = list()

for x in range(500):
    spawn_point = [
        random.randint(0, width),
        random.randint(0, height)
    ]
    entity = BasicEntity(spawn_point)
    entities.append(entity)
    entity.spawn()

player = PlayerEntity([400,300])
entities.append(player)
player.spawn()

collision_manager = EntityCollisionManager()

while True:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT: sys.exit()

    window.fill(black)

    collision_manager.update_collisions()

    for entity in entities:
        entity.update(window, events)

    pygame.display.flip() #Use .update instead for more optimization
    time.sleep(0.01)