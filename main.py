from basic_scene import BasicScene
from projectile_scene import ProjectileScene
from screen import Screen

scenes = [ProjectileScene(), BasicScene()]

screen = Screen(scenes)

while True:
    screen.update()
