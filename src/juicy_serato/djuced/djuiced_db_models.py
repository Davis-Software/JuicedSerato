from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.sqlite import INTEGER, VARCHAR, DECIMAL, FLOAT, DATETIME, BLOB
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


Base = declarative_base()


class DJuicedTrackModel(Base):
    __tablename__ = "tracks"

    id = Column(INTEGER, primary_key=True)
    album = Column(VARCHAR(255))
    albumartist = Column(VARCHAR(255))
    artist = Column(VARCHAR(255))
    bitrate = Column(INTEGER)
    comment = Column(VARCHAR(100))
    composer = Column(VARCHAR(255))
    coverimage = Column(VARCHAR(255))
    title = Column(VARCHAR(255))
    smart_advisor = Column(INTEGER)
    bpm = Column(DECIMAL(5, 1))
    max_val_gain = Column(FLOAT)
    tracknumber = Column(INTEGER)
    drive = Column(VARCHAR(16))
    filepath = Column(VARCHAR(1024))
    filename = Column(VARCHAR(255))
    absolutepath = Column(VARCHAR(1024))
    filetype = Column(VARCHAR(16))
    key = Column(INTEGER, default=-1)
    genre = Column(VARCHAR(100))
    filesize = Column(INTEGER)
    length = Column(FLOAT)
    rating = Column(INTEGER)
    filedate = Column(DATETIME, nullable=True)
    year = Column(INTEGER)
    playcount = Column(INTEGER)
    first_played = Column(DATETIME, nullable=True)
    last_played = Column(DATETIME, nullable=True)
    first_seen = Column(DATETIME, nullable=True)
    tags_read = Column(INTEGER)
    waveform = Column(BLOB)
    danceability = Column(FLOAT)
    samplerate = Column(INTEGER)
    stores = Column(VARCHAR(1024))
    cues = relationship("DJuicedTrackCueModel", back_populates="track")

    def __repr__(self):
        return f"<DJuicedTrackModel(Id: {self.id}, title: {self.title})>"


class DJuicedTrackCueModel(Base):
    __tablename__ = "trackCues"

    id = Column(INTEGER, primary_key=True)
    trackId = Column(VARCHAR(100), ForeignKey(DJuicedTrackModel.absolutepath))
    track = relationship("DJuicedTrackModel", back_populates="cues")
    cuename = Column(VARCHAR(100))
    cuenumber = Column(INTEGER)
    cuepos = Column(DECIMAL(5, 1))
    loopLength = Column(DECIMAL(5, 1), default=0)
    cueColor = Column(INTEGER)
    isSavedLoop = Column(INTEGER)

    def __repr__(self):
        return f"<DJuicedTrackCueModel(Id: {self.id}, Name: {self.cuename}, Track: {self.track})>"
