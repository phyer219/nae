import mutagen


class MusicItem:
    def __init__(self, path):
        self.path = path
        mfile = mutagen.File(path)
        self.tags = mfile.tags
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
