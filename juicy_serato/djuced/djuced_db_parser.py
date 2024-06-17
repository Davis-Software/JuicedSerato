from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .djuiced_db_models import DJuicedTrackModel, DJuicedTrackCueModel


class DJucedDBParser:
    def __init__(self, db_path: str):
        self.db_path = db_path

    def __enter__(self):
        self.engine = create_engine(f"sqlite:///{self.db_path}")
        self.session = sessionmaker(bind=self.engine)()

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()

    @property
    def track_count(self):
        return self.session.query(DJuicedTrackModel).count()

    @property
    def cue_count(self):
        return self.session.query(DJuicedTrackCueModel).count()

    def list_tracks(self):
        return self.session.query(DJuicedTrackModel).all()

    def list_cues(self):
        return self.session.query(DJuicedTrackCueModel).all()
