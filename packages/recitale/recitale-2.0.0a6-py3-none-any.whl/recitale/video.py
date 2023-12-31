import logging
import shlex
import subprocess
import urllib.parse

from json import dumps as json_dumps
from json import loads as json_loads
from pathlib import Path
from zlib import crc32

from .utils import remove_superficial_options


logger = logging.getLogger("recitale." + __name__)


class VideoCommon:
    def __get_infos(self):
        if VideoFactory.global_options["binary"] == "ffmpeg":
            binary = "ffprobe"
        else:
            binary = "avprobe"
        command = (
            binary
            + " -v error -select_streams v:0 -show_entries stream=width,height "
            + " -show_entries format=duration "
            + " -print_format json=compact=1 "
            + shlex.quote(str(self.filepath))
        )
        out = subprocess.check_output(shlex.split(command))
        infos = json_loads(out)
        self.size = infos["streams"][0]["width"], infos["streams"][0]["height"]
        self.dur = float(infos["format"]["duration"])

    @property
    def duration(self):
        if not hasattr(self, "dur"):
            self.__get_infos()

        return self.dur

    @property
    def ratio(self):
        # Calling ffprobe is expensive so do it lazily and only once
        if not hasattr(self, "size"):
            self.__get_infos()

        width, height = self.size
        return width / height


class Thumbnail(VideoCommon):
    suffix = ".jpg"

    def __init__(self, base_filepath, base_id, size):
        self.filepath = self.__filepath(base_filepath, base_id, size)
        self.size = size

    def __filepath(self, base_filepath, base_id, size):
        p = Path(base_filepath)
        width, height = size
        suffix = "-{base_id}-{width}x{height}{suffix}".format(
            base_id=base_id,
            width=width if width else "",
            height=height if height else "",
            suffix=self.suffix,
        )

        return p.parent / (p.stem + suffix)


class Reencode(Thumbnail):
    def __init__(self, base_filepath, base_id, size, extension):
        self.suffix = "." + extension
        super().__init__(base_filepath, base_id, size)


class BaseVideo(VideoCommon):
    def __init__(self, options, global_options):
        self.thumbnails = dict()
        self.reencodes = dict()
        self.options = global_options.copy()
        self.options.update(options)
        self.filepath = self.options["name"]
        self.options = remove_superficial_options(self.options)
        self.chksum_opt = crc32(
            bytes(json_dumps(self.options, sort_keys=True), "utf-8")
        )

    def _add_reencode(self, reencode):
        return self.reencodes.setdefault(reencode.filepath, reencode)

    def reencode(self, size):
        reencode = Reencode(
            self.filepath, self.chksum_opt, size, self.options["extension"]
        )
        return urllib.parse.quote(self._add_reencode(reencode).filepath.name)

    def _add_thumbnail(self, thumbnail):
        return self.thumbnails.setdefault(thumbnail.filepath, thumbnail)

    def thumbnail(self, size):
        thumbnail = Thumbnail(self.filepath, self.chksum_opt, size)
        return urllib.parse.quote(self._add_thumbnail(thumbnail).filepath.name)


# TODO: add support for looking into parent directories (name: ../other_gallery/pic.jpg)
class VideoFactory:
    base_vids = dict()
    global_options = dict()

    @classmethod
    def get(cls, path, video):
        vid = video.copy()
        # To resolve paths with .. in them, we need to resolve the path first and then
        # find the relative path to the source (current) directory.
        vid["name"] = Path(path).joinpath(vid["name"]).resolve().relative_to(Path.cwd())
        bvid = BaseVideo(vid, cls.global_options)
        return cls.base_vids.setdefault(bvid.filepath / str(bvid.chksum_opt), bvid)
