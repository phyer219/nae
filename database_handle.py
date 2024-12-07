import os
import sqlite3
from contextlib import contextmanager
from .tag_handle import Track
from .logger import Logger


class NaeDatabase:
    CREATE_TRACKS_TABLE = '''
                    CREATE TABLE tracks
                    (track_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT,
                    album_id INTEGER,
                    artist_id INTEGER,
                    duration REAL,
                    track_number INTEGER,
                    album_artist_id INTEGER,
                    date TEXT,
                    genre TEXT,
                    total_tracks INTEGER,
                    path TEXT NOT NULL,
                    disc_number INTEGER,
                    total_discs INTEGER,
                    FOREIGN KEY (album_id) REFERENCES albums (album_id),
                    FOREIGN KEY (artist_id) REFERENCES artists (artist_id),
                    FOREIGN KEY (album_artist_id)
                                REFERENCES artists (artist_id))
                    '''
    CREATE_ALBUMS_TABLE = '''
                    CREATE TABLE albums
                    (album_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL)
                    '''
    CREATE_ARTISTS_TABLE = '''
                    CREATE TABLE artists
                    (artist_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL)
                    '''
    INSERT_ALBUM_QUERY = '''
                INSERT INTO albums
                (title)
                VALUES(?)'''
    INSERT_ARTIST_QUERY = '''
                INSERT INTO artists
                (name)
                VALUES(?)'''
    SELECT_ALBUM_ID_QUERY = """
                SELECT album_id FROM albums
                WHERE title=?"""
    SELECT_ARTIST_ID_QUERY = """
                SELECT artist_id FROM artists
                WHERE name=?"""
    INSERT_TRACK_QUERY = """
                INSERT INTO tracks
                (title, album_id, artist_id, duration, track_number,
                total_tracks, disc_number, total_discs, album_artist_id,
                date, genre, path)
                VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
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
            raise e
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
            c.execute(self.CREATE_ARTISTS_TABLE)
            conn.commit()

    def db_insert_album(self, album: str):
        with self.connect_db() as conn:
            c = conn.cursor()
            c.execute(self.INSERT_ALBUM_QUERY, (album,))
            conn.commit()

    def db_insert_artist(self, name: str):
        with self.connect_db() as conn:
            c = conn.cursor()
            c.execute(self.INSERT_ARTIST_QUERY, (name,))
            conn.commit()

    def get_album_id(self, cursor, album: str):
        cursor.execute(self.SELECT_ALBUM_ID_QUERY, (album,))
        result = cursor.fetchone()
        return result

    def get_artist_id(self, cursor, name: str):
        cursor.execute(self.SELECT_ARTIST_ID_QUERY, (name,))
        result = cursor.fetchone()
        return result

    def db_insert_track(self, track: Track):
        with self.connect_db() as conn:
            c = conn.cursor()

            album_id = self.get_album_id(c, track.album)
            if album_id:
                album_id = album_id[0]
            else:
                self.db_insert_album(track.album)
                album_id = self.get_album_id(c, track.album)[0]

            artist_id = self.get_artist_id(c, track.artist)
            if artist_id:
                artist_id = artist_id[0]
            else:
                self.db_insert_artist(track.artist)
                artist_id = self.get_artist_id(c, track.artist)[0]

            album_artist_id = self.get_artist_id(c, track.album_artist)
            if album_artist_id:
                album_artist_id = album_artist_id[0]
            else:
                self.db_insert_artist(track.album_artist)
                album_artist_id = self.get_artist_id(c, track.album_artist)[0]

            c.execute(self.INSERT_TRACK_QUERY,
                      (track.title,
                       album_id,
                       artist_id,
                       track.duration,
                       track.track_number,
                       track.total_tracks,
                       track.disc_number,
                       track.total_discs,
                       album_artist_id,
                       track.date,
                       track.genre,
                       track.path))
            conn.commit()

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
