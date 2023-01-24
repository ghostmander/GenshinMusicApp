import pyautogui
import pydirectinput
import time
import ctypes
import sys
from pick import pick
import transcriber as tr
pydirectinput.PAUSE = 0.0


def inputParser(inp):
    return [i.split('-') if len(i) > 1 else [i] for i in inp.split()]


def is_admin():
    return ctypes.windll.shell32.IsUserAnAdmin()


if is_admin():
    # Code of your program here
    songs = tr.songSheet

    option, index = pick(list(songs.keys()), "Select a song",
                         indicator="->", default_index=0)

    print(f"Playing {songs[option]['Name']} in 2 seconds...")
    time.sleep(2)

    song = songs[option]
    bpm = song["BPM"]
    for i in tr.songParser(song["notes"]):
        if isinstance(i, int):
            time.sleep(i/16 * bpm/240)
            continue
        pydirectinput.press(i)

else:
    # Re-run the program with admin rights
    ctypes.windll.shell32.ShellExecuteW(
        None, "runas", sys.executable, " ".join(sys.argv), None, 1)
