import random
import sys, pygame
import time
from basic_entity import BasicEntity
from entity_collision_manager import EntityCollisionManager, are_colliding, are_different
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

collision_manager = EntityCollisionManager()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    window.fill(black)

    collision_manager.update_collisions()

    for entity in entities:
        entity.update(window)

    pygame.display.flip() #Use .update instead for more optimization
    #time.sleep(0.05)