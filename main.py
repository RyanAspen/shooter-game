from basic_scene import BasicScene
from enemy_scene import EnemyScene
from particle_scene import ParticleScene
from projectile_scene import ProjectileScene
from screen import Screen
from target_scene import TargetScene

scenes = [EnemyScene()]

screen = Screen(scenes)

while True:
    screen.update()
