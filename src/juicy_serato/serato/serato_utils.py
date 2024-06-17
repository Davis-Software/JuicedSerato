from .serato_structs import UnknownEntry, BpmLockEntry, ColorEntry, CueEntry, LoopEntry, FlipEntry


def read_bytes(fp):
    for x in iter(lambda: fp.read(1), b''):
        if x == b'\00':
            break
        yield x


def get_entry_type(entry_name):
    entry_type = UnknownEntry
    for entry_cls in (BpmLockEntry, ColorEntry, CueEntry, LoopEntry, FlipEntry):
        if entry_cls.NAME == entry_name:
            entry_type = entry_cls
            break
    return entry_type
