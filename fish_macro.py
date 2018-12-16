import os
# Automatically set the user's desktop as file path
os.chdir(os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop'))
import win32com.client
import pyautogui
import cv2
import time
import random
import numpy as np

# create instance for sending keystroke to windows
shell = win32com.client.Dispatch("WScript.Shell")

# imagesearch source = github : https://github.com/drov0/python-imagesearch
def imagesearch(image, precision=0.8):
    im = pyautogui.screenshot()
    #im.save('testarea.png') usefull for debugging purposes, this will save the captured region as "testarea.png"
    img_rgb = np.array(im)
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    template = cv2.imread(image, 0)
    template.shape[::-1]

    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    if max_val < precision:
        return [-1,-1]
    return max_loc

# 1 fish per about 23 sec. fishing rod 100 = 37 min. If you miss fish, it takes 33 sec to cast again.
# https://medium.com/@martin.lees/image-recognition-for-automation-with-python-711ac617b4e5
print("[FYI #1] 100 fishing rods = about 37 minutes OR 157 fishing rods = about 1 hour")
print(" ")
number_of_fishing_rods = 999
print(" ")
print("[FYI #2] ctrl + c <- exit the program")
print(" ")
print("Running...")
print("Made by silvernine")

# counts # of caught fish
caught_fish_counter = 0
timeout_start_fishing = time.time()
for i in range(int(number_of_fishing_rods)):
    # 34 seconds timeout for failed detection case.
    timeout = 34 
    #starting time
    timeout_start = time.time()
    # Initial value to keep the while loop started
    pos_fish=[-1,-1]
    # while fish is not caught yet or under specified timeout, keep looking for the ! sign
    while (pos_fish[0]==-1) and (time.time()<(timeout_start+timeout)):
        pos_fish=imagesearch("fishcaught.png")
    # Send 'w' keystroke when fish is caught OR recast the bait if detection failed and timed out
    shell.SendKeys("w")
    # Recast the bait if detection was successful. Won't send 'w' if detection failed.
    if (time.time()-timeout_start)<timeout and i<(int(number_of_fishing_rods)-1):
        time.sleep(6) #time it takes to re-cast after pulling the bait out
        time.sleep(random.randint(15,20)/10) #add 1~2 sec random time
        shell.SendKeys("w")
        caught_fish_counter += 1
print("Done!")
print(" ")
print("You caught {} fish out of {} tries. Success rate is {}%.".format(int(caught_fish_counter),int(number_of_fishing_rods),round(int(caught_fish_counter)/int(number_of_fishing_rods)*100)))
print("It took {} minutes. Program will exit automatically in 30 seconds.".format(round((time.time()-timeout_start_fishing)/60)))
time.sleep(30)
        

