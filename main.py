import pygame
from basic_scene import BasicScene
from screen import Screen
import constants

scenes = [BasicScene()]

screen = Screen(scenes)

while True:
    if screen.active_scene is None:
        screen.activate_scene()
    screen.update()
