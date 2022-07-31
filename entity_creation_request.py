# Custom data types
point = list[int]


class EntityCreationRequest:

    """
    EntityCreationRequest is a structure that holds all necessary information for a
    Screen object to create a new entity with in a dynamic way
    """

    def __init__(self, name: str, spawn_point: point):
        self.name = name
        self.spawn_point = [spawn_point[0], spawn_point[1]]
