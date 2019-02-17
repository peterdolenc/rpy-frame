from entities.image_fitment import ImageFitment
from entities.image_meta import ImageMeta


class PresentableImage:
    def __init__(self, meta: ImageMeta, fitment: ImageFitment):
        self.meta = meta
        self.fitment = fitment