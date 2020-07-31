from TAPI import Counter
import keyboard
from win32api import GetSystemMetrics
from win32gui import GetWindowText, GetForegroundWindow
import sys
import time

doExit = False
forceChange = 0

def on_press_reaction(event):
    global doExit
    global forceChange
    if event.name == '0':
        print("cya")
        doExit = True
    if event.name == '[':
        forceChange -= 1
    if event.name == ']':
        forceChange += 1

resolutions = {
    "2560x1440": {
        "L": (1600, 91, 1646, 94),
        "R": (2137, 164, 2241, 168),
        "H": (2489, 126, 2504, 164)
    },
    "1920x1080": {
        "L": (1201, 68, 1213, 71),
        "R": (1602, 123, 1613, 126),
        "H": (1874, 146, 1882, 157)
    }
}

if __name__ == "__main__":
    keyboard.on_press(on_press_reaction)
    print("TAPICounter Started. Press [ to force decrease count, ] to force increase count, and 0 to quit. Quitting via 0 will save the current encounter count")
    print("Getting resolution of primary monitor...")
    
    w = GetSystemMetrics(0)
    h = GetSystemMetrics(1)
    resString = f"{w}x{h}"

    if resString not in resolutions:
        print(f"Unsupported resolution. Please open an issue on github. Detected resolution: {resString}")
        sys.exit()

    print(f"Detected resolution: {resString}")

    curRes = resolutions[resString]

    usr_tem = input("\nWhich temtem are you trying to hunt?: ")

    if not usr_tem:
        usr_tem = "Undefined"

    counter = Counter(curRes["L"], curRes["R"], curRes["H"], "./ECount.json", usr_tem)

    while not doExit:
        if GetWindowText(GetForegroundWindow()) == "Temtem":
            counter.check()

        if (forceChange != 0):
            counter.changeCount(forceChange)
            forceChange = 0

        time.sleep(0.2)
    
    counter.writeJson()