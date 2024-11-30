import os
import sqlite3
from .tag_handle import MusicItem


class NaeDatabase:
    def __init__(self, database_dir, database_name):
        self.path = os.path.join(database_dir, database_name)
        self._init_db()

    def _init_db(self):
        if not os.path.exists(self.path):
            self._create_db()

    def _create_db(self):
        conn = sqlite3.connect(self.path)
        c = conn.cursor()
        c.execute('''CREATE TABLE tracks
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
                ''')
        conn.commit()
        c.execute('''CREATE TABLE albums
                  (album_id INTEGER PRIMARY KEY AUTOINCREMENT,
                  title TEXT NOT NULL
                  )
                ''')
        conn.commit()
        conn.close()

    def db_inert_album(self, album: str):
        conn = sqlite3.connect(self.path)
        c = conn.cursor()
        c.execute("""
                INSERT INTO albums
                (title)
                VALUES(?)""", (album,))
        conn.commit()
        conn.close()

    def db_select_album(self, cursor, album: str):
        cursor.execute("""
                SELECT album_id, title FROM albums
                WHERE title=?""", (album,))
        result = cursor.fetchone()
        return result

    def db_select_tracks_from_albums(self, album_id: int):
        conn = sqlite3.connect(self.path)
        c = conn.cursor()
        c.execute("""
                  SELECT title FROM albums WHERE album_id=?
                """, (album_id,))
        album = {'title': c.fetchall()[0]}
        c.execute("""
                  SELECT title FROM tracks WHERE album_id=?
                  """, (album_id,))
        album['tracks'] = c.fetchall()
        conn.commit()
        conn.close()
        return album

    def db_insert_track(self, track: MusicItem):
        conn = sqlite3.connect(self.path)
        c = conn.cursor()
        album_id = self.db_select_album(c, track.album)
        if album_id:
            album_id = album_id[0]
        else:
            self.db_inert_album(track.album)
            album_id = self.db_select_album(c, track.album)[0]
        print('=======', type(track.duration), track.duration)

        c.execute("""
                INSERT INTO tracks
                (title, album, album_id, artist, duration, album_artist,
                 date, genre, path)
                VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (track.title,
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
        conn = sqlite3.connect(self.path)
        c = conn.cursor()
        items = [{'title': row[0], 'album': row[1], 'artist': row[2],
                  'path': row[3], 'duration': row[4]}
                 for row in c.execute("""SELECT title, album, artist,
                                                 path, duration
                                         FROM
                                           tracks ORDER BY title""")]
        conn.commit()
        conn.close()
        return items
