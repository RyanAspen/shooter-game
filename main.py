"""
TODO: 
- Add standard entity attributes that can be added to entities
   * Rigid_body -> cannot overlap with any other entity with Rigid Body
   * Constrained_to_screen -> bounces off of edges of the screen
   * Destroyed_off_screen -> destroys itself after leaving the screen
   * Gravity -> experiences gravity downwards

- Make entity_collision_manager more efficient (collidelist() or similar)
- Make drawing more efficient?
"""

from basic_scene import BasicScene
from projectile_scene import ProjectileScene
from screen import Screen

scenes = [ProjectileScene(), BasicScene()]

screen = Screen(scenes)

while True:
    screen.update()
