import os


class ImageMeta:

    def __init__(self, full_path):
        self.full_path = full_path
        self.dominant_colors = None
        self.date = None
        self.caption = None

