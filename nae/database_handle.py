import os
from .tag_handle import TrackFile
from .logger import Logger
from .default_config import NaeConfig
from sqlalchemy import (create_engine, Column, Integer, String, Float,
                        ForeignKey, UniqueConstraint, and_)
from sqlalchemy.orm import (declarative_base, relationship, sessionmaker,
                            joinedload)


Base = declarative_base()


class Artist(Base):
    __tablename__ = 'artists'
    artist_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)

    albums = relationship('Album', back_populates='album_artist')
    tracks = relationship('Track', back_populates='artist',
                          foreign_keys='Track.artist_id')


class Album(Base):
    __tablename__ = 'albums'
    album_id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    album_artist_id = Column(Integer, ForeignKey('artists.artist_id'),
                             nullable=False)

    tracks = relationship('Track', back_populates='album')
    album_artist = relationship('Artist', back_populates='albums')

    __table_args__ = (UniqueConstraint('album_artist_id', 'title',
                                       name='uq_artist_album_title'),)


class Track(Base):
    __tablename__ = 'tracks'
    track_id: int = Column(Integer, primary_key=True, autoincrement=True)
    title: str = Column(String, nullable=False)
    album_id: int = Column(Integer, ForeignKey('albums.album_id'))
    artist_id: int = Column(Integer, ForeignKey('artists.artist_id'))
    duration: float = Column(Float)
    track_number: int = Column(Integer)
    album_artist_id: int = Column(Integer, ForeignKey('artists.artist_id'))
    date: str = Column(String)
    genre: str = Column(String)
    total_tracks: int = Column(Integer)
    path: str = Column(String, nullable=False)
    disc_number: int = Column(Integer)
    total_discs: int = Column(Integer)

    album = relationship('Album', back_populates='tracks')
    artist = relationship('Artist', back_populates='tracks',
                               foreign_keys=[artist_id])


class NaeDatabase:
    def __init__(self, config: NaeConfig):
        self.db_path = os.path.join(config.DATABASE_DIR, config.DATABASE_NAME)

        self.logger = Logger(log_name='NaeDatabase', log_file=config.LOG_PATH)

        self.engine = create_engine(f"sqlite:///{self.db_path}", echo=True)
        self.Session = sessionmaker(bind=self.engine)
        self._init_db()

    def _init_db(self):
        Base.metadata.create_all(self.engine)
        self.logger.info(f"database path: {self.db_path}")

    def insert_artist(self, name):
        with self.Session() as session:
            try:
                artist = Artist(name=name)
                session.add(artist)
                session.commit()
                return artist
            except Exception as e:
                session.rollback()
                raise e

    def insert_album(self, title, album_artist):

        with self.Session() as session:
            album_artist_id = session.query(Artist).filter_by(
                name=album_artist).first().artist_id
            if not album_artist_id:
                album_artist_id = self.insert_artist(album_artist).artist_id
            try:
                album = Album(title=title, album_artist_id=album_artist_id)
                session.add(album)
                session.commit()
                return album
            except Exception as e:
                session.rollback()
                raise e

    def insert_track(self, track_file: TrackFile):
        with self.Session() as session:
            try:
                session.add(self.track_file_to_orm(track_file, session))
                session.commit()
            except Exception as e:
                session.rollback()
                raise e

    def track_file_to_orm(self, tf: TrackFile, session):
        artist = session.query(Artist).filter_by(
            name=tf.artist).first()
        if not artist:
            artist = self.insert_artist(name=tf.artist)
            artist = session.merge(artist)
        artist_id = artist.artist_id

        album_artist = session.query(Artist).filter_by(
            name=tf.album_artist).first()
        if not album_artist:
            album_artist = self.insert_artist(tf.album_artist)
            album_artist = session.merge(album_artist)
        album_artist_id = album_artist.artist_id

        album = session.query(Album).filter(and_(
            Album.title == tf.album,
            Album.album_artist.has(Artist.name == tf.album_artist))).first()
        if not album:
            album = self.insert_album(title=tf.album,
                                      album_artist=tf.album_artist)
            album = session.merge(album)
        album_id = album.album_id
        return Track(title=tf.title,
                     album_id=album_id,
                     artist_id=artist_id,
                     album_artist_id=album_artist_id,
                     duration=tf.duration,
                     track_number=tf.track_number,
                     total_tracks=tf.total_tracks,
                     disc_number=tf.disc_number,
                     total_discs=tf.total_discs,
                     date=tf.date,
                     genre=tf.genre,
                     path=tf.path)

    def get_all_tracks(self, number_cut=100):
        with self.Session() as session:
            tracks = session.query(Track).options(
                joinedload(Track.artist),
                joinedload(Track.album)
            ).order_by(Track.title).limit(number_cut).all()
        return tracks
