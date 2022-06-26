class Extrema:
    def __init__(self, x, y, clazz, step):
        self.x = x * step
        self.y = y
        self.clazz = clazz

    def __repr__(self):
        return f"x={self.x} y={self.y} class={self.clazz}"
