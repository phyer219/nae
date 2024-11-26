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
        c.execute('''CREATE TABLE music_items
                (title text, album text, artist text, album_artist text,
                date text, genre text, path text)
                ''')
        conn.commit()
        conn.close()

    def db_insert(self, music_item: MusicItem):
        conn = sqlite3.connect(self.path)
        c = conn.cursor()
        c.execute("""
                INSERT INTO music_items
                VALUES(?, ?, ?, ?, ?, ?, ?)
                """, (music_item.title,
                      music_item.album,
                      music_item.artist,
                      music_item.album_artist,
                      music_item.date,
                      music_item.genre,
                      music_item.path))
        conn.commit()
        conn.close()
