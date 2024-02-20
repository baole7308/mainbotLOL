import os
import cv2 as cv
import pyautogui
import numpy as np
from yolo import Bot
import pynput
os.chdir(os.path.dirname(os.path.abspath(__file__)))
bot = Bot("LOL.pt")
exit = False
def on_press(key):
    global exit
    try:
        if key.char == 'm':
            print('move')
            bot.move()
        elif key.char == 'j':
            print('set priorty')
            bot.set_priority()
        elif key.char == 'k':
            exit = True
    except AttributeError:  
        pass
listener = pynput.keyboard.Listener(on_press=on_press)
listener.start()
print("Current schedule: ", bot.schedule)
while True:
    screen = np.array(pyautogui.screenshot())
    frame = cv.cvtColor(screen, cv.COLOR_BGR2RGB)
    xyxy, classes = bot.get_rectangles(frame)
    bot.farm(xyxy, classes) 
    if exit:
        cv.destroyAllWindows()
        listener.stop()
        break
print('exit')