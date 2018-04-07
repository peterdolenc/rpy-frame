import os
import string
import stat
import pygame
import PIL.Image
import PIL.ExifTags
from datetime import datetime
from entities.image_meta import ImageMeta


class FileLoader:

    def get_files(self):
        directory = "../samples"
        images = self.get_files_from_directory(directory)
        print(f'{len(images):d} images discovered.')
        image_metas = [ self.get_image_metadata(image) for image in images ]
        print(f'{len(image_metas):d} images parsed correctly.')

        return image_metas


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

    def get_image_metadata(self, image_path: string):
        image_meta = ImageMeta(image_path)

        img = PIL.Image.open(image_meta.full_path)
        exif_data = img._getexif()

        if exif_data is not None:
            image_meta.date = self.get_date_from_exif(exif_data)
        if image_meta.date is None:
            print('[WARNING] Cannot read date EXIF for: '+image_meta.full_path)

        return image_meta


    def load_image(self, image_meta: ImageMeta):
        print("Loading " + image_meta.full_path)
        return pygame.image.load(image_meta.full_path).convert(24)

    def get_date_from_exif(self, exif):
        std_fmt = '%Y:%m:%d %H:%M:%S.%f'
        tags = [(36867, 37521),  # (DateTimeOriginal, SubsecTimeOriginal)
                (36868, 37522),  # (DateTimeDigitized, SubsecTimeOriginal)
                (306, 37520), ]  # (DateTime, SubsecTime)

        for t in tags:
            dat_stmp = exif.get(t[0])
            sub_stmp = exif.get(t[1], 0)

            # PIL.PILLOW_VERSION >= 3.0 returns a tuple
            dat_stmp = dat_stmp[0] if type(dat_stmp) == tuple else dat_stmp
            sub_stmp = sub_stmp[0] if type(sub_stmp) == tuple else sub_stmp
            if dat_stmp != None: break

        if dat_stmp == None: return None
        full = '{}.{}'.format(dat_stmp, sub_stmp)
        return datetime.strptime(full, std_fmt)


