class Peak:
    def __init__(self, left_min_extrema, max_extrema, right_min_extrema):
        self.left_min_extrema = left_min_extrema
        self.max_extrema = max_extrema
        self.right_min_extrema = right_min_extrema
        self.ampl = max(abs(left_min_extrema.y - max_extrema.y), abs(right_min_extrema.y - max_extrema.y))
        self.time_of = max_extrema.x
        self.duration = right_min_extrema.x - left_min_extrema.x

    def __repr__(self):
        return f"{self.time_of} {self.left_min_extrema}, {self.max_extrema}, {self.right_min_extrema}\n"

    def is_good(self, threshold_y):
        return abs(self.left_min_extrema.y - self.max_extrema.y) > threshold_y \
               and abs(self.right_min_extrema.y - self.max_extrema.y) > threshold_y