import mutagen
import os

bas_dir = './test_media'
files = os.listdir(bas_dir)


class MusicItem:
    def __init__(self, path):
        mfile = mutagen.File(path)
        self.tags = mfile.tags
        print(type(mfile))
        if isinstance(mfile, mutagen.mp3.MP3):
            self._get_tag_mp3()
        elif isinstance(mfile, mutagen.flac.FLAC):
            self._get_tag_flac()

    def _get_tag_mp3(self):
        self.title = self.tags['TIT2'].text[0]
        self.album = self.tags['TALB'].text[0]
        self.artist = self.tags['TPE1'].text[0]
        self.album_artist = self.tags['TPE2'].text[0]
        year = self.tags['TDRC'].text[0].year
        self.date = year
        self.genre = self.tags['TCON'].text[0]

    def _get_tag_flac(self):
        self.title = self.tags['TITLE'][0]
        self.album = self.tags['ALBUM'][0]
        self.artist = self.tags['ARTIST'][0]
        self.album_artist = self.tags['ALBUMARTIST'][0]
        self.date = self.tags['DATE'][0]
        self.genre = self.tags['GENRE'][0]


for f in files:
    mfile = mutagen.File(os.path.join(bas_dir, f))
    ii = MusicItem(os.path.join(bas_dir, f))
    mfile.info.pprint()
