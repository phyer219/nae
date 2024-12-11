import os
import shutil
from .tag_handle import Track
from .database_handle import NaeDatabase
from .default_config import NaeConfig
from .logger import Logger
from .util import make_dir_exist


class FileHandle:
    supported_media_type = ('mp3', 'flac')

    def __init__(self, media_path_to_import,
                 keep_original_file: bool, link: bool,
                 handle_files: bool,
                 database: NaeDatabase,
                 config: NaeConfig):
        self.config = config
        self.logger = Logger('File Handle', log_file=config.LOG_PATH)
        self.media_path_to_import = media_path_to_import
        self.keep_original_file = keep_original_file
        self.link = link
        self.handle_files = handle_files
        self.db = database

    def scan_media(self):
        for dirpath, dirnames, filenames in os.walk(self.media_path_to_import):
            for f in filenames:
                if f.endswith(self.supported_media_type):
                    yield os.path.join(dirpath, f)
                else:
                    self.logger.warning(f'unsupported file type: {f}')

    def gen_new_path(self, track: Track) -> str:
        return os.path.join(self.config.MEDIA_LIBRARY_PATH,
                            track.album_artist.replace('/', '_'),
                            track.album.replace('/', '_'),
                            f"{track.track_number}. {track.title.replace(r'/', '_')}.{track.format}")

    def transfer_file(self, original_path: str, new_path: str):
        make_dir_exist(dest=new_path)
        if self.keep_original_file:
            if self.link:
                os.link(original_path, new_path)
                self.logger.info(f'create link for file: {original_path} >> {new_path}')
            else:
                shutil.copy(original_path, new_path)
                self.logger.info(f'copy file: {original_path} >> {new_path}')
        else:
            shutil.move(original_path, new_path)
            self.logger.info(f'move file: {original_path} >> {new_path}')

    def process_track_file(self, track):
        if self.handle_files:
            new_path = self.gen_new_path(track=track)
            if os.path.exists(new_path):
                new_path = os.path.splitext(new_path)[0]
                new_path += '_copy' + f'.{track.format}'
                self.logger.warning(f'duplicate file: {new_path}')
            self.transfer_file(original_path=track.path, new_path=new_path)
            track.path = new_path

    def import_media(self, test=True):
        self.logger.info('Start import media')
        for i, f in enumerate(self.scan_media()):
            self.logger.info(f'Find {i+1: >5} media: {f}')
            track = Track(f, config=self.config)
            if not test:
                self.process_track_file(track)
                self.db.db_insert_track(track)
        self.logger.info('Finished import media!')
