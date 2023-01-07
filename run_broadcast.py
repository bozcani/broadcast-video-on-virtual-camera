import pyvirtualcam
import numpy as np
import cv2

cap = cv2.VideoCapture("Funny Chickens.mp4")

# Check if camera opened successfully
if cap.isOpened() == False:
    AssertionError("Error opening video stream or file")

WIDTH = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
HEIGHT = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
FRAME_COUNT = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
FPS = int(cap.get(cv2.CAP_PROP_FPS))

with pyvirtualcam.Camera(width=WIDTH, height=HEIGHT, fps=FPS, device="/dev/video4") as cam:
    print(f"Using virtual camera: {cam.device}")

    while cap.isOpened():
        ret, frame = cap.read()
        if ret == True:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            cam.send(frame)
            cam.sleep_until_next_frame()
