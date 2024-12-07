import mutagen
import os

from .logger import Logger
from .default_config import LOG_PATH


def process_number_total(num_tot: str, cut='/'):
    if not num_tot or num_tot == 'NULL':
        return 'NULL', 'NULL'

    splited = num_tot.split(cut)
    if len(splited) == 1 or not splited[1]:
        return int(splited[0]), 'NULL'
    else:
        return int(splited[0]), int(splited[1])


class Track:
    def __init__(self, path):
        self.logger = Logger('Track', LOG_PATH)
        self.path = path
        self.mfile = mutagen.File(path)
        self.tags = self.mfile.tags
        _, ext = os.path.splitext(self.path)
        if ext == ".mp3":
            self.format = 'mp3'
            self._process_tag = self._process_ID3v2
            self._extract_tags_mp3()
        elif ext == ".flac":
            self.format = 'flac'
            self._process_tag = self._process_FLAC
            self._extract_tags_flac()
        else:
            raise TypeError('unsupported format!')

    def _extract_tags_mp3(self):
        self.title = self._extract_tag('TIT2', not_null=True)
        self.album = self._extract_tag('TALB', not_null=True)
        self.artist = self._extract_tag('TPE1', not_null=True)
        self.album_artist = self._extract_tag('TPE1', not_null=True)
        year = self._extract_tag('TDRC', not_null=True).year
        self.date = year
        self.genre = self._extract_tag('TCON', not_null=True)
        self.duration = round(self.mfile.info.length, 2)
        track_num = self._extract_tag('TRCK', not_null=True)
        self.track_number, self.total_tracks = process_number_total(track_num)
        self.disc_number, self.total_discs = 'NULL', 'NULL'

    def _extract_tags_flac(self):
        self.title = self._extract_tag('TITLE', not_null=True)
        self.album = self._extract_tag('ALBUM', not_null=True)
        self.artist = self._extract_tag('ARTIST', not_null=True)
        self.album_artist = self._extract_tag('ALBUMARTIST', not_null=True)
        self.date = self._extract_tag('DATE', not_null=True)
        self.genre = self._extract_tag('GENRE', not_null=True)
        self.duration = round(self.mfile.info.length, 2)
        self.track_number = self._extract_tag('TRACKNUMBER', not_null=True)
        if self.track_number != 'NULL':
            self.track_number = int(self.track_number)
        self.total_tracks = self._extract_tag('TRACKTOTAL', not_null=True)
        if self.total_tracks != 'NULL':
            self.total_tracks = int(self.total_tracks)
        discknum = self._extract_tag('DISCNUMBER', not_null=True)
        self.disc_number, self.total_discs = process_number_total(discknum)

    def _process_ID3v2(self, tag: str):
        return tag.text[0]

    def _process_FLAC(self, tag: str):
        return tag[0]

    def _extract_tag(self, tag_frame: str, not_null: False):
        tag = self.tags.get(tag_frame)
        if tag:
            return self._process_tag(tag)
        elif not_null:
            self.logger.warning(f'{self.path:s}, {tag_frame:s} NOT FOUND! '
                                + 'return NULL')
        return 'NULL'
