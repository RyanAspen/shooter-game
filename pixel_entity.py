from typing import Optional
import constants
import pygame
from attribute_database import AttributeDatabase
from entity_creation_request import EntityCreationRequest
from pixel_frame import PixelFrame

point = list[int]
speed = list[int]


class PixelEntity:

    id_counter = 1
    attribute_db = AttributeDatabase()
    """
    PixelEntity contains at minimum, a set of rectangles describing the pixels of the entity,
    a set of invisible rectangles describing the hitboxes of that entity, 
    and the top-left corner of the entity when initially created
    """

    def __init__(
        self,
        frame_dict: dict[str, PixelFrame],
        spawn_point: point,
        starting_frame_key: str,
        name: str,
        initial_speed: speed,
        layer_priority: int,
    ):
        self.frame_dict = frame_dict
        self.spawn_point = spawn_point.copy()
        self.current_point = spawn_point.copy()
        self.previous_point = spawn_point.copy()
        self.current_frame_key = starting_frame_key
        self.current_frame = frame_dict[starting_frame_key]
        self.id = PixelEntity.id_counter
        PixelEntity.id_counter += 1
        self.name = name
        self.layer_priority = layer_priority
        self.speed = initial_speed
        self.should_delete = False
        self.entity_creation_request = None
        self.frozen = False

    def spawn(self):
        for frame_key in self.frame_dict:
            if frame_key != self.current_frame_key:
                for rect, _ in self.frame_dict[frame_key].visual_rects:
                    rect.left += self.spawn_point[0]
                    rect.top += self.spawn_point[1]
                for rect in self.frame_dict[frame_key].hitboxes:
                    rect.left += self.spawn_point[0]
                    rect.top += self.spawn_point[1]

        for rect, _ in self.current_frame.visual_rects:
            rect.left += self.spawn_point[0]
            rect.top += self.spawn_point[1]

        for rect in self.current_frame.hitboxes:
            rect.left += self.spawn_point[0]
            rect.top += self.spawn_point[1]

    def move_relative(self, movement: speed):
        self.current_point[0] += movement[0]
        self.current_point[1] += movement[1]

        for frame_key in self.frame_dict:
            if frame_key != self.current_frame_key:
                for rect, _ in self.frame_dict[frame_key].visual_rects:
                    rect.left += movement[0]
                    rect.top += movement[1]
                for rect in self.frame_dict[frame_key].hitboxes:
                    rect.left += movement[0]
                    rect.top += movement[1]

        for rect, _ in self.current_frame.visual_rects:
            rect.left += movement[0]
            rect.top += movement[1]

        for rect in self.current_frame.hitboxes:
            rect.left += movement[0]
            rect.top += movement[1]

    def move_absolute(self, new_location: point):
        self.diff = tuple(map(lambda i, j: i - j, new_location, self.current_point))
        print(self.diff)
        self.move_relative(self.diff)

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

    def draw(self, window: pygame.Surface):
        for rect, color in self.current_frame.visual_rects:
            pygame.draw.rect(window, color, rect)

    def update(
        self,
        window: pygame.Surface,
        events: list[pygame.event.Event],
        collisions: list[str],
    ) -> tuple[bool, Optional[EntityCreationRequest]]:
        if self.frozen:
            self.frozen = False
        else:
            self.move_relative(self.speed)
        self.draw(window)
        return self.should_delete, self.entity_creation_request

    def handle_attributes(
        self,
        window: pygame.Surface,
        events: list[pygame.event.Event],
        collisions: list[str],
    ) -> tuple[bool, Optional[EntityCreationRequest]]:

        """
        Handles all of the general attributes in the following order:
        * Rigid_body -> cannot overlap with any other entity with Rigid Body
        * Constrained_to_screen -> bounces off of edges of the screen
        * Destroyed_off_screen -> destroys itself after leaving the screen
        * Gravity -> experiences gravity downwards
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
        collisions: list[str],
    ) -> tuple[bool, Optional[EntityCreationRequest]]:
        # cannot overlap with any other entity with Rigid Body
        # This means that if there is a collision with any other entity that also has rigid_body, revert back to the last position and reverse speed
        for collision_name in collisions:
            if PixelEntity.attribute_db.has_attribute(collision_name, "rigid_body"):
                self.revert_to_previous_position()
                self.mirror_speed()  # TODO: Might change this to more comprehensive reflection logic later
                break
        return False, None

    # TODO: Use the commented out code for new attribute "bounce_off_screen_edges"
    def handle_constrained_to_screen(
        self,
        window: pygame.Surface,
        events: list[pygame.event.Event],
        collisions: list[str],
    ) -> tuple[bool, Optional[EntityCreationRequest]]:
        # If this entity is about to leave the screen, instead reflect off the boundary
        # if (
        #    self.current_point[0] < 0
        #    or self.current_point[0] > constants.width
        #    or self.current_point[1] < 0
        #    or self.current_point[1] > constants.height
        # ):
        #    self.revert_to_previous_position()
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

    def handle_destroyed_off_screen(
        self,
        window: pygame.Surface,
        events: list[pygame.event.Event],
        collisions: list[str],
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
        collisions: list[str],
    ) -> tuple[bool, Optional[EntityCreationRequest]]:
        self.change_speed_relative((0, -1))
        return False, None

    def change_frame(self, frame_key: str):
        self.current_frame_key = frame_key
        self.current_frame = self.frame_dict[frame_key]

    def is_colliding_with_name(
        self,
        collisions: list[str],
        collision_name: str = "ALL",
    ) -> bool:
        for name in collisions:
            if collision_name == "ALL" or collision_name == name:
                return True
        return False
