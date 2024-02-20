import pyautogui
from ultralytics import YOLO
import time 
import keyboard
class Bot:
    screenshot = None
    yoloModel = None
    priority_list=[[0,1],[2],[3],[4],[5,6],[7,8]]
    priority = [0,1]
    x2=[1700,1616,1577,1721,1740,1618]
    y2=[925,855,845,957,996,894]
    schedule = 0
    def __init__(self, model_file_path):
        # load model
        self.yoloModel = YOLO(model_file_path)
        # config
        self.yoloModel.overrides['conf'] = 0.8  # NMS confidence threshold
        self.yoloModel.overrides['iou'] = 0.5  # NMS IoU threshold
        self.yoloModel.overrides['agnostic_nms'] = False  # NMS class-agnostic
        self.yoloModel.overrides['max_det'] = 100  # maximum number of detections per image
    def get_rectangles(self, screenshot):
        results = self.yoloModel.predict(screenshot, verbose = False)
        # Get the all the positions from the result
        for i in results:
            xyxy = i.boxes.xyxy.cpu().numpy()
            classes = i.boxes.cls.cpu().numpy()
        return xyxy, classes
    def confirm_mob(self,classes):
        for i in range(len(classes)):
            if classes[i] in self.priority:  
                return i
    def set_priority(self):
        if (self.schedule == 5):
            self.schedule = 0
        else:
            self.schedule = self.schedule + 1
        tempList = self.priority_list.copy()
        self.priority = []
        self.priority = tempList.pop(self.schedule)
       
        print(f"Current schedule: {self.schedule}") 
    
    def farm(self, xyxy, classes):
        (a,b)=xyxy.shape
        if a>0:
            temp = self.confirm_mob(classes)
            if temp is None:
                pass
            else:
                center_x = xyxy[temp][0] + (xyxy[temp][2]-xyxy[temp][0])/2
                center_y = xyxy[temp][1] + (xyxy[temp][3]-xyxy[temp][1])/2
                x = int(center_x)
                y = int(center_y)
                pyautogui.moveTo(x,y,0.1,pyautogui.easeInQuad)
                pyautogui.click(button='right',clicks=1)
                pyautogui.mouseUp(button='right')
                time.sleep(2)
                keyboard.press('q')
                keyboard.release('q') 
    def move(self):
        pyautogui.moveTo(self.x2[self.schedule],self.y2[self.schedule],0,pyautogui.easeInQuad)
        pyautogui.mouseDown(button='right') 
        pyautogui.mouseUp(button='right') 