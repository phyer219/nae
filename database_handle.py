import os
import sqlite3
from contextlib import contextmanager
from .tag_handle import MusicItem
from .logger import Logger


class NaeDatabase:
    CREATE_TRACKS_TABLE = '''
                    CREATE TABLE tracks
                    (track_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    album TEXT NOT NULL,
                    album_id INTEGER,
                    artist text,
                    duration FLOAT,
                    album_artist text,
                    date text,
                    genre text,
                    path text,
                    FOREIGN KEY (album_id) REFERENCES albums (album_id))
                    '''
    CREATE_ALBUMS_TABLE = '''
                    CREATE TABLE albums
                    (album_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL)
                    '''
    INSERT_ALBUM_QUERY = """
                INSERT INTO albums
                (title)
                VALUES(?)"""
    SELECT_ALBUM_QUERY = """
                SELECT album_id, title FROM albums
                WHERE title=?"""
    INSERT_TRACK_QUERY = """
                INSERT INTO tracks
                (title, album, album_id, artist, duration, album_artist,
                 date, genre, path)
                VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)
                """
    logger = Logger(log_name='NaeDatabase')

    def __init__(self, database_dir, database_name):
        self.db_path = os.path.join(database_dir, database_name)
        self.logger.info(f"base directory: {os.path.abspath(database_dir)}")
        self.logger.info(f"database path: {self.db_path}")
        self._init_db()

    @contextmanager
    def connect_db(self):
        conn = sqlite3.connect(self.db_path)
        try:
            yield conn
        except Exception as e:
            self.logger.error(e)
            conn.rollback()
        finally:
            conn.close()

    def _init_db(self):
        if not os.path.exists(self.db_path):
            self.logger.info(f"creating database: {self.db_path}")
            self._create_db()

    def _create_db(self):
        with self.connect_db() as conn:
            c = conn.cursor()
            c.execute(self.CREATE_TRACKS_TABLE)
            c.execute(self.CREATE_ALBUMS_TABLE)
            conn.commit()

    def db_insert_album(self, album: str):
        with self.connect_db() as conn:
            c = conn.cursor()
            c.execute(self.INSERT_ALBUM_QUERY, (album,))
            conn.commit()

    def db_select_album(self, cursor, album: str):
        cursor.execute(self.SELECT_ALBUM_QUERY, (album,))
        result = cursor.fetchone()
        return result

    def db_select_tracks_from_albums(self, album_id: int):
        with self.connect_db() as conn:
            c = conn.cursor()
            c.execute("""
                    SELECT title FROM albums WHERE album_id=?
                    """, (album_id,))
            album = {'title': c.fetchall()[0]}
            c.execute("""
                    SELECT title FROM tracks WHERE album_id=?
                    """, (album_id,))
            album['tracks'] = c.fetchall()
        return album

    def db_insert_track(self, track: MusicItem):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        album_id = self.db_select_album(c, track.album)
        if album_id:
            album_id = album_id[0]
        else:
            self.db_insert_album(track.album)
            album_id = self.db_select_album(c, track.album)[0]

        c.execute(self.INSERT_TRACK_QUERY,
                     (track.title,
                      track.album,
                      album_id,
                      track.artist,
                      track.duration,
                      track.album_artist,
                      track.date,
                      track.genre,
                      track.path))
        conn.commit()
        conn.close()

    def getall(self):
        with self.connect_db() as conn:
            c = conn.cursor()
            items = [{'title': row[0], 'album': row[1], 'artist': row[2],
                    'path': row[3], 'duration': row[4]}
                    for row in c.execute("""SELECT title, album, artist,
                                                    path, duration
                                            FROM
                                            tracks ORDER BY title""")]
        return items
