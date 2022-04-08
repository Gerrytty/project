class Peak:
    def __init__(self, left_min_extrema, max_extrema, right_min_extrema):
        self.left_min_extrema = left_min_extrema
        self.max_extrema = max_extrema
        self.right_min_extrema = right_min_extrema

    def __repr__(self):
        return f"({self.left_min_extrema.x}, {self.left_min_extrema.y}) ({self.max_extrema.x}, {self.max_extrema.y}) ({self.right_min_extrema.x}, {self.right_min_extrema.y})"

    def is_good(self, threshold_y, threshold_x):
        # 100, 8 for gras and 0.2 ? for bio
        return abs(self.left_min_extrema.y - self.max_extrema.y) > threshold_y and abs(self.right_min_extrema.y - self.max_extrema.y) > threshold_y and abs(self.left_min_extrema.x - self.max_extrema.x) > threshold_x and abs(self.right_min_extrema.x - self.max_extrema.x) > threshold_x