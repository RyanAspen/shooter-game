from scenes.basic_scene import BasicScene
from scenes.enemy_scene import EnemyScene
from scenes.particle_scene import ParticleScene
from scenes.projectile_scene import ProjectileScene
from screen import Screen
from scenes.target_scene import TargetScene

scenes = [EnemyScene()]

screen = Screen(scenes)

while True:
    screen.update()
