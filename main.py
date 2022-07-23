import pygame
from basic_scene import BasicScene
from projectile_scene import ProjectileScene
from screen import Screen
import constants

scenes = [ProjectileScene(), BasicScene()]

screen = Screen(scenes)

while True:
    screen.update()
