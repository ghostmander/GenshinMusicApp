import pyautogui
import pydirectinput
import time
import ctypes
import sys
from pick import pick
pydirectinput.PAUSE = 0.01


def inputParser(inp):
    return [i.split('-') if len(i) > 1 else [i] for i in inp.split()]


def is_admin():
    return ctypes.windll.shell32.IsUserAnAdmin() or True


if is_admin():
    # Code of your program here
    songs = {
        "sweaterWeather": {
            "notes": "Q W E Q W Q E Q W Q E W E W Q W Q E W Q E H W E W Q H Q W Q H W H-H W-W-W-W-W H W-W-W-W Q W-W-W-W W Q W-W Q W E E-E-E Q Q T E E W E W E W E E E W Q H W-W-W-W-W Q-Q W-W-E-E E W . Q Q E W . Q Q W E . Q Q W W W Q Q W-W-W-W-W-W-W-W Q-Q-Q E W W W W E W Q H R E H R E Q W Q W Q W E W Q H R E H R E W W Q J J H J Q",
            "bpm": 180,
            "repeatDelay": 0.1,
            "songName": "Sweater Weather - The Neighbourhood"
        }
    }

    option, index = pick(list(songs.keys()), "Select a song",
                         indicator="->", default_index=0)

    print(f"Playing {songs[option]['songName']} in 2 seconds...")
    time.sleep(2)

    song = songs[option]
    bpm = song["bpm"]
    for keys in inputParser(song["notes"]):
        for key in keys:
            pydirectinput.press(key.lower())
            time.sleep(song["repeatDelay"])
        time.sleep((len(keys) == 1) * 60/bpm)

else:
    # Re-run the program with admin rights
    ctypes.windll.shell32.ShellExecuteW(
        None, "runas", sys.executable, " ".join(sys.argv), None, 1)
