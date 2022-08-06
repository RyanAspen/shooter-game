# Imports
import constants as constants
import pygame

from attribute_database import AttributeDatabase
from entity_creation_request import EntityCreationRequest
from entity_visual_creator import EntityVisualCreator
from pixel_frame import PixelFrame
from typing import Optional

# Custom data types
point = list[int]
speed = list[int]

# Global constants


class PixelEntity:

    id_counter = 1
    attribute_db = AttributeDatabase()
    entity_visual_info_creator = EntityVisualCreator()
    """
    PixelEntity contains at minimum, a set of rectangles describing the pixels of the entity,
    a set of invisible rectangles describing the hitboxes of that entity, 
    and the top-left corner of the entity when initially created
    """

    def __init__(
        self,
        spawn_point: point,
        starting_frame_key: str,
        name: str,
        initial_speed: speed,
        layer_priority: int,
    ):
        self.frame_dict = dict()
        for frame_name in PixelEntity.entity_visual_info_creator.get_entity_frame_names(
            name
        ):
            frame_image = PixelEntity.entity_visual_info_creator.get_entity_info(
                name, frame_name
            )
            # image_width, image_height = PixelEntity.entity_visual_info_creator.get_scaling_info(name, frame_name)
            frame_hitboxes = PixelEntity.entity_visual_info_creator.get_hitbox_info(
                name, frame_name
            )
            self.frame_dict[frame_name] = PixelFrame(frame_image, frame_hitboxes)

        self.spawn_point = spawn_point.copy()
        self.current_point = spawn_point.copy()
        self.previous_point = spawn_point.copy()
        self.current_frame_key = starting_frame_key
        self.current_frame = self.frame_dict[starting_frame_key]
        self.id = PixelEntity.id_counter
        PixelEntity.id_counter += 1
        self.name = name
        self.layer_priority = layer_priority
        self.speed = initial_speed
        self.should_delete = False
        self.entity_creation_request = None  # type: Optional[EntityCreationRequest]
        self.frozen = False

    def spawn(self):
        for frame_key in self.frame_dict:
            for rect in self.frame_dict[frame_key].hitboxes:
                rect.left += self.spawn_point[0]
                rect.top += self.spawn_point[1]

    def move_relative(self, movement: speed):
        self.current_point[0] += movement[0]
        self.current_point[1] += movement[1]

        for frame_key in self.frame_dict:
            for rect in self.frame_dict[frame_key].hitboxes:
                rect.left += movement[0]
                rect.top += movement[1]

    def move_absolute(self, new_location: point):
        diff = [0, 0]
        diff[0] = new_location[0] - self.current_point[0]
        diff[1] = new_location[1] - self.current_point[1]
        self.move_relative(diff)

    def revert_to_previous_position(self):
        self.move_absolute(self.previous_point)
        self.frozen = True

    def change_speed_relative(self, speed_change):
        self.speed[0] += speed_change[0]
        self.speed[1] += speed_change[1]

    def change_speed_absolute(self, new_speed):
        self.speed[0] = new_speed[0]
        self.speed[1] = new_speed[1]

    def mirror_speed(self):
        self.speed[0] *= -1
        self.speed[1] *= -1

    def reflect(self, collided_entity_current_point):
        # Two cases: either reflect x-axis or y-axis
        # Case 1: Reflect x-axis -> self.x
        diff = [0, 0]
        time_to_connect = [0, 0]
        diff[0] = collided_entity_current_point[0] - self.previous_point[0]
        diff[1] = collided_entity_current_point[1] - self.previous_point[1]
        time_to_connect[0] = diff[0] / self.speed[0]
        time_to_connect[1] = diff[1] / self.speed[1]
        if time_to_connect[0] > time_to_connect[1]:
            self.speed[0] = -self.speed[0]
        else:
            self.speed[1] = -self.speed[1]

    def draw(self, window: pygame.Surface):
        window.blit(
            self.current_frame.image, (self.current_point[0], self.current_point[1])
        )

    def handle_attributes(
        self,
        window: pygame.Surface,
        events: list[pygame.event.Event],
        collisions: list[tuple[str, point]],
    ) -> tuple[bool, Optional[EntityCreationRequest]]:

        """
        Handles all of the general attributes in the following order:
        * rigid_body -> cannot overlap with any other entity with Rigid Body
        * constrained_to_screen -> bounces off of edges of the screen
        * reflect_off_boundaries -> reflect off the screen edges
        * destroyed_off_screen -> destroys itself after leaving the screen
        * gravity -> experiences gravity downwards
        """

        entity_creation_request = None
        if PixelEntity.attribute_db.has_attribute(self.name, "rigid_body"):
            new_should_delete, new_entity_creation_request = self.handle_rigid_body(
                window, events, collisions
            )
            if new_entity_creation_request is not None:
                entity_creation_request = new_entity_creation_request
            if new_should_delete:
                return (True, entity_creation_request)

        if PixelEntity.attribute_db.has_attribute(self.name, "constrained_to_screen"):
            (
                new_should_delete,
                new_entity_creation_request,
            ) = self.handle_constrained_to_screen(window, events, collisions)
            if new_entity_creation_request is not None:
                entity_creation_request = new_entity_creation_request
            if new_should_delete:
                return (True, entity_creation_request)

        if PixelEntity.attribute_db.has_attribute(self.name, "reflect_off_boundaries"):
            (
                new_should_delete,
                new_entity_creation_request,
            ) = self.handle_reflect_off_boundaries(window, events, collisions)
            if new_entity_creation_request is not None:
                entity_creation_request = new_entity_creation_request
            if new_should_delete:
                return (True, entity_creation_request)

        if PixelEntity.attribute_db.has_attribute(self.name, "mirror_on_boundaries"):
            (
                new_should_delete,
                new_entity_creation_request,
            ) = self.handle_mirror_on_boundaries(window, events, collisions)
            if new_entity_creation_request is not None:
                entity_creation_request = new_entity_creation_request
            if new_should_delete:
                return (True, entity_creation_request)

        if PixelEntity.attribute_db.has_attribute(self.name, "destroyed_off_screen"):
            (
                new_should_delete,
                new_entity_creation_request,
            ) = self.handle_destroyed_off_screen(window, events, collisions)
            if new_entity_creation_request is not None:
                entity_creation_request = new_entity_creation_request
            if new_should_delete:
                return (True, entity_creation_request)

        if PixelEntity.attribute_db.has_attribute(self.name, "gravity"):
            new_should_delete, new_entity_creation_request = self.handle_gravity(
                window, events, collisions
            )
            if new_entity_creation_request is not None:
                entity_creation_request = new_entity_creation_request
            if new_should_delete:
                return (True, entity_creation_request)

        return (False, entity_creation_request)

    def handle_rigid_body(
        self,
        window: pygame.Surface,
        events: list[pygame.event.Event],
        collisions: list[tuple[str, point]],
    ) -> tuple[bool, Optional[EntityCreationRequest]]:
        # cannot overlap with any other entity with Rigid Body
        # This means that if there is a collision with any other entity that also has rigid_body, revert back to the last position and reverse speed
        for (
            collision_name,
            collision_current_point,
        ) in collisions:
            if PixelEntity.attribute_db.has_attribute(collision_name, "rigid_body"):
                self.revert_to_previous_position()
                self.reflect(collision_current_point)
                self.move_relative(self.speed)
        return False, None

    def handle_constrained_to_screen(
        self,
        window: pygame.Surface,
        events: list[pygame.event.Event],
        collisions: list[tuple[str, point]],
    ) -> tuple[bool, Optional[EntityCreationRequest]]:
        # If this entity is about to leave the screen, prevent it from doing so
        if (
            self.current_point[0] < 0
            or self.current_point[0] > constants.width
            or self.current_point[1] < 0
            or self.current_point[1] > constants.height
        ):
            self.revert_to_previous_position()

        return False, None

    def handle_reflect_off_boundaries(
        self,
        window: pygame.Surface,
        events: list[pygame.event.Event],
        collisions: list[tuple[str, point]],
    ) -> tuple[bool, Optional[EntityCreationRequest]]:
        # If this entity is about to leave the screen, instead reflect off the boundary
        new_speed = self.speed
        if self.current_point[0] < 0:
            new_speed[0] = abs(self.speed[0])
        elif self.current_point[0] > constants.width:
            new_speed[0] = -abs(self.speed[0])
        if self.current_point[1] < 0:
            new_speed[1] = abs(self.speed[1])
        elif self.current_point[1] > constants.height:
            new_speed[1] = -abs(self.speed[1])
        self.change_speed_absolute(new_speed)
        return False, None

    def handle_mirror_on_boundaries(
        self,
        window: pygame.Surface,
        events: list[pygame.event.Event],
        collisions: list[tuple[str, point]],
    ) -> tuple[bool, Optional[EntityCreationRequest]]:
        # If this entity is about to leave the screen, place it on the opposite side of the screen
        new_current_point = self.current_point.copy()
        if self.current_point[0] < 0:
            new_current_point[0] = constants.width
        elif self.current_point[0] > constants.width:
            new_current_point[0] = 0
        if self.current_point[1] < 0:
            new_current_point[1] = constants.height
        elif self.current_point[1] > constants.height:
            new_current_point[1] = 0
        self.move_absolute(new_current_point)
        return False, None

    def handle_destroyed_off_screen(
        self,
        window: pygame.Surface,
        events: list[pygame.event.Event],
        collisions: list[tuple[str, point]],
    ) -> tuple[bool, Optional[EntityCreationRequest]]:

        # If this entity is about to leave the screen, destroy it
        if (
            self.current_point[0] < 0
            or self.current_point[0] > constants.width
            or self.current_point[1] < 0
            or self.current_point[1] > constants.height
        ):
            should_delete = True
        else:
            should_delete = False

        return should_delete, None

    def handle_gravity(
        self,
        window: pygame.Surface,
        events: list[pygame.event.Event],
        collisions: list[tuple[str, point]],
        f,
    ) -> tuple[bool, Optional[EntityCreationRequest]]:
        self.change_speed_relative((0, -1))
        return False, None

    def change_frame(self, frame_key: str):
        self.current_frame_key = frame_key
        self.current_frame = self.frame_dict[frame_key]

    def is_colliding_with_name(
        self,
        collisions: list[tuple[str, point]],
        collision_name: str = "ALL",
    ) -> bool:
        for name, _ in collisions:
            if collision_name == "ALL" or collision_name == name:
                return True
        return False
