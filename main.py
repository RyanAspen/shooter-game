import pygame
from screen import Screen

screen = Screen(800, 800, pygame.Color(100, 100, 200))

while True:
    screen.update()
