import os
from .tag_handle import Track
from .database_handle import NaeDatabase
from .default_config import DATABASE_DIR, DATABASE_NAME, LOG_PATH
from .logger import Logger


def scan_media(dir):
    for dirpath, dirnames, filenames in os.walk(dir):
        for f in filenames:
            if f.endswith('.mp3') or f.endswith('.flac'):
                yield os.path.join(dirpath, f)


def import_media(dir):
    logger = Logger('import media', log_file=LOG_PATH)
    db = NaeDatabase(database_dir=DATABASE_DIR, database_name=DATABASE_NAME)
    logger.info('Start import media')
    for i, f in enumerate(scan_media(dir)):
        logger.info(f'Find {i+1: >5} media: {f}')
        db.db_insert_track(Track(f))
    logger.info(f'Finished import media!')
