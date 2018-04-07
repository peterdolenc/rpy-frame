import os
import string
import stat
import pygame


class FileLoader:

    def get_files(self):
        directory = "../samples"
        return self.get_files_from_directory(directory)

    def get_files_from_directory(self, path: string):
        files = []
        for file in os.listdir(path):
            file_path = os.path.join(path, file)
            file_mode = os.stat(file_path)[stat.ST_MODE]
            if stat.S_ISDIR(file_mode):
                files.extend(self.get_files_from_directory(file_path))
            elif stat.S_ISREG(file_mode):
                _, ext = os.path.splitext(file)
                if ext.lower() in ['.png', '.jpg', '.jpeg', '.gif', '.bmp']:
                    files.append(file_path)
        return files

    def load_image(self, image_path: string):
        print("Loading " + image_path)
        return pygame.image.load(image_path).convert(24)


