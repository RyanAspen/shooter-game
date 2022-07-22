import random
import sys, pygame
import time
from basic_entity import BasicEntity
from pixel_entity import are_colliding, are_different
pygame.init()

size = width, height = 800, 600
black = 0, 0, 0

acceleration = 1.05

window = pygame.display.set_mode(size)

entity_speed_pairs = list()
for x in range(50):
    random_left = random.randint(0, width)
    random_top = random.randint(0, height)
    entity = BasicEntity([random_left,random_top])
    speed_left = 0
    speed_top = 0
    while speed_left == 0 or speed_top == 0:
        speed_left = random.randint(-3, 3)
        speed_top = random.randint(-3, 3)
    speed = [speed_left, speed_top]
    entity_speed_pair = (entity, speed)
    entity_speed_pairs.append(entity_speed_pair)

for entity, _ in entity_speed_pairs:
    entity.spawn()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    window.fill(black)

    for entity, speed in entity_speed_pairs:
        entity.move_relative(speed)
        entity_corner = entity.current_point
        if entity_corner[0] < 0 or entity_corner[0] > width:
            speed[0] = -speed[0]
        if entity_corner[1] < 0 or entity_corner[1] > height:
            speed[1] = -speed[1]
        for entity2, speed2 in entity_speed_pairs:
            if are_different(entity, entity2):
                if are_colliding(entity, entity2):
                    entity.change_frame("Hit")
                    entity2.change_frame("Hit")
                    speed[0] *= acceleration
                    speed[1] *= acceleration
                    speed2[0] *= acceleration
                    speed2[1] *= acceleration
        entity.draw(window)

    pygame.display.flip() #Use .update instead for more optimization
    #time.sleep(0.05)