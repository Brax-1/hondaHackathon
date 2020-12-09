import os
import cv2

from lsHotword import ls
import numpy as np

import speedtest
import time
import urllib 
from urllib.request import urlopen

def is_notinternet():
    try:
        urlopen('https://www.google.com',timeout=1)
        return False
    except urllib.error.URLError as Error:
        return True

def is_internet():
    try:
        urlopen('https://www.google.com',timeout=1)
        return True
    except urllib.error.URLError as Error:
        return False

def check():
    print("function")
    if(is_internet()):
        speed = speedtest.Speedtest()
        download = speed.download()
        upload = speed.upload()
        print(f"download speed : {download}")
        print(f"upload speed : {upload}")
        return upload
    else:
        print("ohkoko")
        return 0


filename = 'help.avi'
frames_per_second = 24.0
res = '480p'

# Set resolution for the video capture
# Function adapted from https://kirr.co/0l6qmh
def change_res(cap, width, height):
    cap.set(3, width)
    cap.set(4, height)

# Standard Video Dimensions Sizes
STD_DIMENSIONS =  {
    "480p": (640, 480),
    "720p": (1280, 720),
    "1080p": (1920, 1080),
    "4k": (3840, 2160),
}


# grab resolution dimensions and set video capture to it.
def get_dims(cap, res='1080p'):
    width, height = STD_DIMENSIONS["480p"]
    if res in STD_DIMENSIONS:
        width,height = STD_DIMENSIONS[res]
    ## change the current caputre device
    ## to the resulting resolution
    change_res(cap, width, height)
    return width, height

# Video Encoding, might require additional installs
# Types of Codes: http://www.fourcc.org/codecs.php
VIDEO_TYPE = {
    'avi': cv2.VideoWriter_fourcc(*'XVID'),
    #'mp4': cv2.VideoWriter_fourcc(*'H264'),
    'mp4': cv2.VideoWriter_fourcc(*'XVID'),
}

def get_video_type(filename):
    filename, ext = os.path.splitext(filename)
    if ext in VIDEO_TYPE:
      return  VIDEO_TYPE[ext]
    return VIDEO_TYPE['avi']


flag = 0
cap = cv2.VideoCapture(0)
out = cv2.VideoWriter(filename, get_video_type(filename), frames_per_second, get_dims(cap, res))
while True:
    
    
    print("Speak:")
    ls.lsHotword_loop()
  
    print("printing speed")
    while True:
        ret, frame = cap.read()
        out.write(frame)
        cv2.imshow('frame',frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        print("run",flag)
        if(flag==0):
            print("checking")
            upload = check()
            
        
        
        if(upload > 10 and flag==0):
            print("upload")
            
            
            flag = 1
            
        
            
        
        
        # if(is_notinternet()):
   
        #     if(flag ==1):
        #         flag = 0
        #         print("reUpload",flag)
        
        
    cap.release()
    out.release()
    cv2.destroyAllWindows()
    



