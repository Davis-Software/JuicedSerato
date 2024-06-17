def get_serato_color(color_index: int):
    return {
        0: b"\x00\x00\xff",
        1: b"\x00\xff\xff",
        2: b"\x00\x80\x00",
        3: b"\x00\xff\x00",
        4: b"\xff\x00\x00",
        5: b"\xff\x00\xff",
        6: b"\xff\xff\xff",
        7: b"\xff\xa5\x00",
        8: b"\xff\xff\x00"
    }.get(color_index)
