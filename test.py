from serato.serato_db_parser import SeratoDBParser
from serato.serato_structs import CueEntry


if __name__ == '__main__':
    with SeratoDBParser("sample_files/e.mp3") as sdj_p:
        print(
            sdj_p.get_markers()
        )
        # sdj_p.set_markers([
        #     CueEntry(field1=b"\x00", field4=b"\x00", color=b"\xcc\x88\x00", field6=b"\x00\x00", index=0, position=1337, name="Test")
        # ])
