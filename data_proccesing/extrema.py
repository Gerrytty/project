class Extrema:
    def __init__(self, x, y, clazz):
        self.x = x
        self.y = y
        self.clazz = clazz

    def __repr__(self):
        return f"{self.x} {self.y} {self.clazz}"