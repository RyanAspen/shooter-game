point = list[int, int]


class EntityCreationRequest:
    def __init__(self, name: str, spawn_point: point):
        self.name = name
        self.spawn_point = [spawn_point[0], spawn_point[1]]
