import os
import shutil
from .tag_handle import TrackFile
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

    def gen_new_path(self, tf: TrackFile) -> str:
        file_name = f"{tf.disc_number}-{tf.track_number}. "
        file_name += f"{tf.title.replace(r'/', '_')}.{tf.format}"
        return os.path.join(
            self.config.MEDIA_LIBRARY_PATH,
            tf.album_artist.replace('/', '_'),
            tf.album.replace('/', '_'),
            file_name)

    def transfer_file(self, original_path: str, new_path: str):
        make_dir_exist(dest=new_path)
        if self.keep_original_file:
            if self.link:
                os.link(original_path, new_path)
                self.logger.info(
                    f'create link for file: {original_path} >> {new_path}')
            else:
                shutil.copy(original_path, new_path)
                self.logger.info(f'copy file: {original_path} >> {new_path}')
        else:
            shutil.move(original_path, new_path)
            self.logger.info(f'move file: {original_path} >> {new_path}')

    def process_track_file(self, track_file):
        if self.handle_files:
            new_path = self.gen_new_path(tf=track_file)
            if os.path.exists(new_path):
                new_path = os.path.splitext(new_path)[0]
                new_path += '_copy' + f'.{track_file.format}'
                self.logger.warning(f'duplicate file: {new_path}')
            self.transfer_file(original_path=track_file.path,
                               new_path=new_path)
            track_file.path = new_path

    def import_media(self, test=True):
        self.logger.info('Start import media')
        for i, f in enumerate(self.scan_media()):
            self.logger.info(f'Find {i+1: >5} media: {f}')
            track_file = TrackFile(f, config=self.config)
            if not test:
                self.process_track_file(track_file)
                self.db.insert_track(track_file)
        self.logger.info('Finished import media!')
