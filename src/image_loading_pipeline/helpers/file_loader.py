import os
import stat
from typing import List
import pygame


class FileLoader:

    def load_image(image_path: str) -> pygame.Surface:
        print("Loading " + image_path)
        return pygame.image.load(image_path).convert(24)

    def get_files_from_directory(path: str) -> List[str]:
        files = []
        for file in os.listdir(path):
            file_path = os.path.join(path, file)
            file_mode = os.stat(file_path)[stat.ST_MODE]
            if stat.S_ISDIR(file_mode):
                files.extend(FileLoader.get_files_from_directory(file_path))
            elif stat.S_ISREG(file_mode):
                _, ext = os.path.splitext(file)
                if ext.lower() in ['.png', '.jpg', '.jpeg', '.gif', '.bmp']:
                    files.append(file_path)
        return files




