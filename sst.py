import numpy as np
import cv2
import pyautogui
import win32con
import win32gui
import time
def sstmain():

    screenShotfolderName = 'Attendance Image'
    attendaceCheckingImageFile = screenShotfolderName+'/ss1.jpg'
    
    #minimizing Window
    Minimize = win32gui.GetForegroundWindow()
    win32gui.ShowWindow(Minimize, win32con.SW_MINIMIZE)
    
    #taking SS
    time.sleep(3)
    image = pyautogui.screenshot()
    image = cv2.cvtColor(np.array(image),cv2.COLOR_RGB2BGR)
    cv2.imwrite(attendaceCheckingImageFile, image)
#check=sstmain()