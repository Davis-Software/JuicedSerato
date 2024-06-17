import os
import io
import base64
import struct

from mutagen import File
from mutagen.id3 import GEOB, error

from .serato_utils import get_entry_type, read_bytes


class SeratoDBParser:
    FMT_VERSION = 'BB'

    def __init__(self, audio_file: str):
        assert os.path.exists(audio_file), "The audio file does not exist!"

        self.audio_file = audio_file
        self._changes_made = False

        self._data = None

    def __enter__(self):
        self.audio = File(self.audio_file)

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if not self._changes_made:
            return
        self.audio.save()

    def _read_audio_file(self):
        if self._data is None:
            self._data = dict()

        for key, tag in self.audio.tags.items():
            if not isinstance(tag, GEOB):
                continue

            if not key.startswith("GEOB:Serato ") or tag.mime != "application/octet-stream":
                continue

            tag_name = key.split(" ")[1].lower()
            self._data[tag_name] = tag.data

        return self._data

    def _parse_markers(self, data: bytes):
        version_len = struct.calcsize(self.FMT_VERSION)
        version = struct.unpack(self.FMT_VERSION, data[:version_len])
        assert version == (0x01, 0x01)

        b64data = data[version_len:data.index(b'\x00', version_len)].replace(b'\n', b'')
        padding = b'A==' if len(b64data) % 4 == 1 else (b'=' * (-len(b64data) % 4))
        payload = base64.b64decode(b64data + padding)
        fp = io.BytesIO(payload)
        assert struct.unpack(self.FMT_VERSION, fp.read(2)) == (0x01, 0x01)
        while True:
            entry_name = b''.join(read_bytes(fp)).decode('utf-8')
            if not entry_name:
                break
            entry_len = struct.unpack('>I', fp.read(4))[0]
            assert entry_len > 0

            entry_type = get_entry_type(entry_name)
            yield entry_type.load(fp.read(entry_len))

    def _dump_markers(self, parsed_data: list):
        version = struct.pack(self.FMT_VERSION, 0x01, 0x01)

        contents = [version]
        for entry in parsed_data:
            if entry.NAME is None:
                contents.append(entry.dump())
            else:
                data = entry.dump()
                contents.append(b''.join((
                    entry.NAME.encode('utf-8'),
                    b'\x00',
                    struct.pack('>I', (len(data))),
                    data,
                )))

        payload = b''.join(contents)
        payload_base64 = bytearray(base64.b64encode(payload).replace(b'=', b'A'))

        i = 72
        while i < len(payload_base64):
            payload_base64.insert(i, 0x0A)
            i += 73

        data = version
        data += payload_base64
        return data.ljust(470, b'\x00')

    def get_markers(self):
        data = self._data or self._read_audio_file()
        data = data.get("markers2")
        assert data, "No markers found!"

        return list(
            self._parse_markers(data)
        )

    def set_markers(self, markers: list):
        data = self._dump_markers(markers)
        frame = GEOB(
            encoding=3,
            mime="application/octet-stream",
            desc="Serato Markers2",
            data=data
        )

        if "GEOB:Serato Markers_" in self.audio.tags:
            self.audio.tags.pop("GEOB:Serato Markers_")
        if "GEOB:Serato Markers2" in self.audio.tags:
            self.audio.tags.pop("GEOB:Serato Markers2")

        try:
            self.audio.tags["GEOB:Serato Markers2"] = frame
        except error:
            self.audio.add_tags()
            self.audio.tags["GEOB:Serato Markers2"] = frame

        self._changes_made = True
