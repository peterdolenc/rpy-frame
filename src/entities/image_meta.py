from datetime import datetime


class ImageMeta:

    def __init__(self, full_path):
        self.full_path = full_path
        self.dominant_colors = None
        self.date: datetime = None
        self.caption = None

    def sort_key(self):
        return self.date if self.date is not None else self.full_path

