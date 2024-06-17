import os
import tqdm
import shutil

from juicy_serato.djuced.djuced_db_parser import DJucedDBParser
from juicy_serato.serato.serato_db_parser import SeratoDBParser
from juicy_serato.serato.serato_structs import CueEntry
from juicy_serato.serato.serato_mappings import get_serato_color


class SeratoJuicer(DJucedDBParser):
    def __init__(self, db_path: str):
        super().__init__(db_path)
        self.path_overrides = dict()

    def inject(self, use_tqdm: bool = True):
        iterator = tqdm.tqdm(self.list_tracks()) if use_tqdm else self.list_tracks()
        for track in iterator:
            if not track.cues or len(track.cues) == 0:
                continue

            file = self.path_overrides.get(track.id) or track.absolutepath
            if not os.path.exists(file) or not os.path.isfile(file):
                continue

            markers = list()
            skipped_first = False
            for i, cue in enumerate(track.cues):
                if i == 0 and track.cues[0].cuepos == track.cues[1].cuepos:
                    skipped_first = True
                    continue
                marker = CueEntry(field1=b"\x00", field4=b"\x00", field6=b"\x00\x00",
                                  color=get_serato_color(cue.cueColor), position=int(cue.cuepos*1000),
                                  name=cue.cuename, index=i if not skipped_first else i - 1)
                markers.append(marker)

            with SeratoDBParser(file) as parser:
                parser.set_markers(markers)

    def copy(self, location, use_tqdm: bool = True):
        if not os.path.exists(location):
            os.makedirs(location, exist_ok=True)
        if not os.path.isdir(location):
            raise NotADirectoryError(location)

        iterator = tqdm.tqdm(self.list_tracks()) if use_tqdm else self.list_tracks()
        for track in iterator:
            if not os.path.exists(track.absolutepath):
                continue

            new_file = os.path.join(location, track.filename)

            if os.path.exists(new_file):
                self.path_overrides[track.id] = new_file
                continue

            shutil.copy(track.absolutepath, str(new_file))
            self.path_overrides[track.id] = new_file
