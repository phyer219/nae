import os
import shutil
from .tag_handle import Track
from .database_handle import NaeDatabase
from .default_config import (DATABASE_DIR, DATABASE_NAME, LOG_PATH,
                             KEEP_ORIGINAL_FILE, MEDIA_LIBRARY_PATH)
from .logger import Logger


def make_dir_exist(dest):
    dest_dir = os.path.dirname(dest)
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)


def scan_media(dir: str):
    for dirpath, dirnames, filenames in os.walk(dir):
        for f in filenames:
            if f.endswith('.mp3') or f.endswith('.flac'):
                yield os.path.join(dirpath, f)


def gen_new_path(media_library_path: str, track: Track) -> str:
    return os.path.join(media_library_path,
                        track.album_artist.replace('/', '_'),
                        track.album.replace('/', '_'),
                        f"{track.track_number}. {track.title.replace(r'/', '_')}.{track.format}")


def move_files(original_path: str, new_path: str,
               keep_original_file: bool, link: bool, logger: Logger):
    make_dir_exist(dest=new_path)
    if keep_original_file:
        if link:
            os.link(original_path, new_path)
            logger.info(f'create link for file: {original_path} >> {new_path}')
        else:
            shutil.copy(original_path, new_path)
            logger.info(f'copy file: {original_path} >> {new_path}')
    else:
        shutil.move(original_path, new_path)
        logger.info(f'move file: {original_path} >> {new_path}')


def import_media(dir: str, handle_files: bool, link: bool,
                 keep_original_files=KEEP_ORIGINAL_FILE,
                 media_library_path=MEDIA_LIBRARY_PATH):
    logger = Logger('import media', log_file=LOG_PATH)
    db = NaeDatabase(database_dir=DATABASE_DIR, database_name=DATABASE_NAME)
    logger.info('Start import media')
    for i, f in enumerate(scan_media(dir)):
        logger.info(f'Find {i+1: >5} media: {f}')
        track = Track(f)
        if handle_files:
            new_path = gen_new_path(media_library_path=media_library_path,
                                    track=track)
            if os.path.exists(new_path):
                new_path = os.path.splitext(new_path)[0]
                new_path += '_copy' + f'.{track.format}'
                logger.warning(f'duplicate file: {new_path}')
            move_files(original_path=track.path, new_path=new_path,
                       keep_original_file=keep_original_files, link=link,
                       logger=logger)
            track.path = new_path
        db.db_insert_track(track)
    logger.info('Finished import media!')
