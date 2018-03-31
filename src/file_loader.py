import os
import pygame


class FileLoader:

    def get_files(self):
        files = []
        directory = "../samples"

        for file in os.listdir(directory):
            _, ext = os.path.splitext(file)
            ext = ext.lower()
            if ext in ['.png', '.jpg', '.jpeg', '.gif', '.bmp']:
                files.append(os.path.join(directory, file))

        return files

    def load_image(self, image_path):
        print("Loading " + image_path)
        return pygame.image.load(image_path).convert(24)


