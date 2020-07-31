import keyboard
import time
import json
from PIL import ImageGrab 
from win32gui import GetWindowText, GetForegroundWindow

def load_json(path):
    try:
        with open(path) as json_file:
            parsed_json = json.load(json_file)
            return parsed_json
    except FileNotFoundError:
        return None
    except json.decoder.JSONDecodeError:
        return -1

def write_json(path, todump):
    with open(path, 'w') as fp:
        json.dump(todump, fp)

class ScreenBox:
    def __init__(self, bbox, maxRangeExtrema):
        self.bbox = bbox
        self.maxRangeExtrema = maxRangeExtrema
        self.inRange = False

        temp = True

        for x in maxRangeExtrema:
            if x[0] != x[1]:
                temp = False
                break
        
        self.noDiffInExtrema = temp
    
    def compareTuples(self, value):
        if self.noDiffInExtrema:
            return value == self.maxRangeExtrema

        for x in range(3):
            res = (self.maxRangeExtrema[x][0] <= value[x][0]) and (value[x][1] <= self.maxRangeExtrema[x][1])
            if not res:
                return False
    
        return True

    def check(self):
         img = ImageGrab.grab(self.bbox)
         extrema = img.getextrema()
         return self.compareTuples(extrema)

class Counter:
    def __init__(self, bboxHPLeft, bboxHPRight, bboxHUD, jsonPath, TemName):
        self.jsonPath = jsonPath
        self.TemName = TemName

        self.HpColor = ((134, 134), (194, 194), (73, 73))
        self.HudColor = ((60, 60), (232, 232), (234, 234))

        self.FoundLeft = False
        self.FoundRight = False
        self.FoundHud = False

        self.ScreenBoxLeft = ScreenBox(bboxHPLeft, self.HpColor)
        self.ScreenBoxRight = ScreenBox(bboxHPRight, self.HpColor)
        self.ScreenBoxHUD = ScreenBox(bboxHUD, self.HudColor)

        self.loadJson()
        self.sessionCount = 0

    def changeCount(self, value):
        cur = int(self.json[self.TemName])
        cur += value
        self.sessionCount += value
        self.json[self.TemName] = str(cur)
        print(f"Seen: {cur} ({self.sessionCount} this session)")

    def loadJson(self):
        self.json = load_json(self.jsonPath)
        if (self.json == None):
            self.json = {}

        if (self.TemName not in self.json):
            self.json[self.TemName] = "0"

        print(f"You've seen {self.json[self.TemName]} {self.TemName} so far")

    def writeJson(self):
        write_json(self.jsonPath, self.json)

    def check(self):
        if not self.FoundLeft and self.ScreenBoxLeft.check():
            self.FoundLeft = True
            print("Found left!")
        
        if not self.FoundRight and self.ScreenBoxRight.check():
            self.FoundRight = True
            print("Found right!")

        self.FoundHud = self.ScreenBoxHUD.check()

        if (self.FoundLeft or self.FoundRight) and self.FoundHud:
            inc = 0
            if (self.FoundLeft):
                inc += 1
            if (self.FoundRight):
                inc += 1
            self.changeCount(inc)

            self.FoundRight = False
            self.FoundLeft = False


# doExit = False
# forceChange = 0
# 
# def on_press_reaction(event):
#     global doExit
#     global forceChange
#     if event.name == '9':
#         print("cya")
#         doExit = True
#     if event.name == '[':
#         forceChange -= 1
#     if event.name == ']':
#         forceChange += 1
# 
if __name__ == "__main__":
#     keyboard.on_press(on_press_reaction)
#     print("TAPI started directly")
# 
#     # 1440p
#     counter = Counter((1600, 91, 1646, 94), (2137, 164, 2241, 168), (2489, 126, 2504, 164), "./ECount.json", "Paharo")
# 
#     # 1080p
#     # counter = Counter((1201, 68, 1213, 71), (1602, 123, 1613, 126), (1874, 146, 1882, 157), "./ECount.json", "Paharo")
# 
#     while not doExit:
#         counter.check()
# 
#         if (forceChange != 0):
#             counter.changeCount(forceChange)
#             forceChange = 0
# 
#         time.sleep(0.2)
#     
#     counter.writeJson()
    print("TAPI is not supposed to be launched directly!")