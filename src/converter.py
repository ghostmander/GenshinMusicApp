"""
This file contains all conversion functions that are used to convert the song notes to the default encoding.
Currently supported encodings:
- Default
- ABC[1-5]
"""
import re


def _find_gap_string_abc15(gap_num: int) -> str:
    """
    Get a gap string for certain gap.\b
    Basically, this function will return the shortest gap string for the given gap number.\b
    Uses the same logic as a common roman numeral conversion algorithm.\b

    For Example:
    find_gap(1) -> 'l'
    find_gap(2) -> 'j'
    find_gap(5) -> 'gl'
    find_gap(32) -> 'aa'
    @param gap_num: Number of gap units
    @return: Gap string
    """
    return_str = ""
    for key, val in ((16, "a"), (12, "s"), (8, "d"), (6, "f"), (4, "g"), (3, "h"), (2, "j"), (1, "l")):
        while gap_num >= key:
            return_str += val
            gap_num -= key
    return return_str



def convert_abc15(song: str) -> str:
    """
    Converts the song notes from ABC[1-5] to the default encoding.
    :param song: Song notes in ABC[1-5] format.
    :return: Song notes in the default format.
    """
    repl_map = { "A1": 1, "A2": 2, "A3": 3, "A4": 4, "A5": 5,
                 "B1": 8, "B2": 9, "B3": 10, "B4": 11, "B5": 12,
                 "C1": 15, "C2": 16, "C3": 17, "C4": 18, "C5": 19 }

    # Remove all unknown characters.
    song =  re.sub(r'[^A-C1-5.]', '', song.upper())

    # Replace all consecutive dots with their respective gap lengths.
    song = re.sub(r'\.+', lambda x: f"{_find_gap_string_abc15(len(x.group(0)))} ", song)

    # Replace all notes with their respective key presses.
    song = re.sub(r"[A-C][1-5]", lambda x: f"{repl_map[x.group(0)]} ", song)

    # This will work too, but it's less readable.
    # song = re.sub(r"[A-C][1-5]", lambda m: f"{(ord(m.group(0)[0]) - 65) * 7 + int(m.group(0)[1])} ", song)

    return song
