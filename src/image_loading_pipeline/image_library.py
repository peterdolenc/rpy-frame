import random
import PIL.Image
import PIL.ExifTags
from datetime import datetime
from typing import List
from bs4 import BeautifulSoup
from entities.image_meta import ImageMeta
from image_loading_pipeline.helpers.file_loader import FileLoader
from thread_context import ThreadContext


class ImageLibrary:
    def __init__(self, thread_context: ThreadContext):
        self.settings = thread_context.settings
        self.image_metas: List[ImageMeta] = None
        self.count: int = 0

    def discover_images(self, directory: str) -> List[str]:
        images = FileLoader.get_files_from_directory(directory)
        print(f"{len(images):d} images discovered.")

        return images

    # initializes the image library by detecting metadata and sorting images
    def initialize(self):
        image_paths = self.discover_images(self.settings.media_folder)
        self.image_metas = [self.get_image_metadata(image) for image in image_paths]
        self.image_metas.sort(key=lambda im: im.sort_key())
        self.count: int = len(self.image_metas)
        print(f"{self.count:d} images parsed correctly.")

    # creates a new sequence of random length
    # sequence always provides images that are close together
    def get_sequence(self, min_len=4, max_len=8) -> List[ImageMeta]:
        sequence_len = random.randint(min_len, max_len)
        print(f"Starting a new sequence with length of {sequence_len:d}")
        first_index = random.randint(0, self.count - sequence_len)
        sequence = [
            self.image_metas[i] for i in range(first_index, first_index + sequence_len)
        ]
        random.shuffle(sequence)
        return sequence

    # reads image EXIF data
    def get_image_metadata(self, image_path: str) -> ImageMeta:
        image_meta = ImageMeta(image_path)
        img = PIL.Image.open(image_meta.full_path)
        exif_data = img.getexif()
        if exif_data is not None:
            image_meta.date = self.get_date_from_exif(exif_data)
        if image_meta.date is None:
            print("[WARNING] Cannot read date EXIF for: " + image_meta.full_path)
        image_meta.caption = self.get_xmp_title(img)

        return image_meta

    # reads XMP data from file and tries to extract the title property
    def get_xmp_title(self, img):
        try:
            for segment, content in img.applist:
                marker, body = content.split(b"\x00", 1)
                if marker == b"http://ns.adobe.com/xap/1.0/":
                    xml = BeautifulSoup(body, features="html.parser")
                    title_content = xml.find("dc:title").find("rdf:li").string
                    return title_content
        except:
            pass

    # gets a proper datetime object from exif list
    def get_date_from_exif(self, exif) -> datetime:
        std_fmt = "%Y:%m:%d %H:%M:%S.%f"
        tags = [
            (36867, 37521),  # (DateTimeOriginal, SubsecTimeOriginal)
            (36868, 37522),  # (DateTimeDigitized, SubsecTimeOriginal)
            (306, 37520),
        ]  # (DateTime, SubsecTime)
        for t in tags:
            dat_stmp = exif.get(t[0])
            sub_stmp = exif.get(t[1], 0)
            # PIL.PILLOW_VERSION >= 3.0 returns a tuple
            dat_stmp = dat_stmp[0] if type(dat_stmp) == tuple else dat_stmp
            sub_stmp = sub_stmp[0] if type(sub_stmp) == tuple else sub_stmp
            if dat_stmp != None:
                break
        if dat_stmp == None:
            return None
        full = "{}.{}".format(dat_stmp, sub_stmp)
        return datetime.strptime(full, std_fmt)
