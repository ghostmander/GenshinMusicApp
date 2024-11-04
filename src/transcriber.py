"""
This file transcribes the song notes to actual keys and delays that can be used to play the song.

Rules:
-> 1-21 are keys.
--> 1- 7 = [Z, X, C, V, B, N, M]
--> 8-14 = [A, S, D, F, G, H, J]
--> 5-21 = [Q, W, E, R, T, Y, U]

-> letters are spacing (in 16th of a beat [240/bpm * letter/16]):
-> Delay = (bpm / 3840 * letter)s
--> n = 25ms
--> ö = 50ms
--> l = 1 unit
--> j = 2 unit
--> h = 3 unit
--> g = 4 unit
--> f = 6 unit
--> d = 8 unit
--> s = 12 unit
--> a = 16 unit
"""
from typing import Callable, Union, Optional, List
from src.converter import convert_abc15


KEYMAP = 'zxcvbnmasdfghjqwertyu'

DELAYS = {
    "n": 0.025,
    "ö": 0.050,
    "l": 1,
    "j": 2,
    "h": 3,
    "g": 4,
    "f": 6,
    "d": 8,
    "s": 12,
    "a": 16,
}


def _get_encoding_converter(encoding: str) -> Optional[Callable[[str], str]]:
    """
    Converts the encoding to the default encoding.
    @param encoding: The encoding of the song notes.
    @type encoding: str
    @return: The conversion function.
    @rtype: ((str) -> str) | None
    """
    if encoding == "default":
        return lambda x: x
    if encoding == "ABC[1-5]":
        return convert_abc15


def _parse_key(letter: str) -> Union[str, int, float]:
    """
    Parses the key and returns the key or delay.

    @param letter: The key or delay.
    @type letter: str
    @return: The key or delay.
    @rtype: str | int | float
    """
    # Check if the letter is a key from 1-21
    if letter.isnumeric() and 1 <= int(letter) <= 21:
        return KEYMAP[int(letter)-1]

    # Check if the letter is a delay or combination of delays
    if all(l in DELAYS for l in letter):
        return sum(DELAYS[l] for l in letter)

    # If the letter is not a key or delay, print a warning and return None
    print("\033[93mWarning: \033[0mUnknown key: " + letter)


def song_parser(song_notes: str, encoding: str = "default") -> Optional[List]:
    """
    Parses the song notes and turns them into a list of keys and delays.

    @param song_notes: The notes of the song.
    @type song_notes: str
    @param encoding: The encoding of the song notes. Default is "default".
    @type encoding: str
    @return: The parsed song notes.
    @rtype: list[str | int | float] | None
    """

    # First, convert encoding to default
    conversion_fn = _get_encoding_converter(encoding)
    if conversion_fn is None:
        return
    song_notes = conversion_fn(song_notes)

    # Replace double spaces with 1 unit of delay
    song_notes = song_notes.replace("  ", " l ")

    # Get parsed keys
    parsed_keys = [_parse_key(key) for key in song_notes.split()]
    return [key for key in parsed_keys if key is not None]
