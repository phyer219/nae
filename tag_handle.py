import mutagen
import os

from .logger import Logger
from .default_config import LOG_PATH


def process_number_total(num_tot: str, cut='/'):
    if not num_tot:
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
            # self.mfile = ID3(self.path)
            # self.tags = self.mfile.tags
            self._get_tag_mp3()
        elif ext == ".flac":
            self.format = 'flac'
            # self.mfile = FLAC(self.path)
            # self.tags = self.mfile.tags
            self._get_tag_flac()
        else:
            raise TypeError('unsupported format!')

    def _get_tag_mp3(self):
        self.title = self.tags['TIT2'].text[0]
        self.album = self.tags['TALB'].text[0]
        self.artist = self.tags['TPE1'].text[0]

        album_artist = getattr(self.tags, 'TPE2', '')
        if album_artist:
            self.album_artist = album_artist.text[0]
        else:
            self.album_artist = self.artist

        year = self.tags['TDRC'].text[0].year
        self.date = year
        self.genre = self.tags['TCON'].text[0]
        self.duration = round(self.mfile.info.length, 2)
        track_num = self.tags['TRCK'].text[0]
        self.track_number, self.total_tracks = process_number_total(track_num)

        discknum = self.tags.get('TRCK')
        if discknum:
            discknum = discknum.text[0]
        self.disc_number, self.total_discs = process_number_total(discknum)

    def _get_tag_flac(self):
        self.title = self.tags['TITLE'][0]
        self.album = self.tags['ALBUM'][0]
        self.artist = self.tags['ARTIST'][0]
        self.album_artist = self.tags['ALBUMARTIST'][0]
        self.date = self.tags['DATE'][0]
        self.genre = self.tags['GENRE'][0]
        self.duration = round(self.mfile.info.length, 2)
        self.track_number = int(self.tags['TRACKNUMBER'][0])

        total_tracks = self.tags.get('TRACKTOTAL')
        if total_tracks:
            self.total_tracks = int(total_tracks[0])
        else:
            self.total_tracks = 'NULL'

        discknum = self.tags.get('DISCNUMBER', [''])[0]
        self.disc_number, self.total_discs = process_number_total(discknum)

    # def _process_ID3v2(self, tag: str):
    #     return tag.text[0]
    # def _process_FLAC(self, tag:str):
    #     return tag[]

    # def _get_ID3v2_and_warning(self, tag: str, not_null: False):
    #     tag = self.tags.get(tag)
    #     if tag:
    #         return tag.text[0]
    #     elif not_null:
    #         self.logger.warning(f'{tag:s} NOT FOUND! return null')
    #     return 'NULL'
