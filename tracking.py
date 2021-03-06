#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cv2
from cv2 import findContours
from cv2 import RETR_EXTERNAL
from cv2 import CHAIN_APPROX_SIMPLE
import numpy as np
import imutils
from imutils.video import VideoStream
import time
import argparse
from collections import deque
import sound_generator
import sounddevice as sd
from sound_generator import generate_note


ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video",
    help="path to the (optional) video file")
ap.add_argument("-b", "--buffer", type=int, default=30,
    help="max buffer size")
args = vars(ap.parse_args())

greenL = (29, 86, 6)
greenU = (64, 255, 255)
pts = deque(maxlen=args["buffer"])

if not args.get("video", False):
    vs = VideoStream(src=1).start()

else:
    vs = cv2.VideoCapture(args["video"])
    
# allow the camera or video file to warm up   
time.sleep(2.0)

freq_array = np.zeros((1,), dtype=np.float32)
start = time.time()
while True:
    # grab the current frame
    frame = vs.read()
    frame = cv2.flip(frame, 1)
    # handle the frame from VideoCapture or VideoStream
    frame = frame[1] if args.get("video", False) else frame
    # if we are viewing a video and we did not grab a frame,
    # then we have reached the end of the video
    if frame is None:
        break
    # resize the frame, blur it, and convert it to the HSV
    # color space
    frame = imutils.resize(frame, width=600)
    blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
    # construct a mask for the color "green", then perform
    # a series of dilations and erosions to remove any small
    # blobs left in the mask
    mask = cv2.inRange(hsv, greenL, greenU)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    #finding the countours
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
    cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    center = None
        # only proceed if at least one contour was found
    if len(cnts) > 0:
        # find the largest contour in the mask, then use
        # it to compute the minimum enclosing circle and
        # centroid
        c = max(cnts, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
        # only proceed if the radius meets a minimum size
        if radius > 10:
            # draw the circle and centroid on the frame,
            # then update the list of tracked points
            cv2.circle(frame, (int(x), int(y)), int(radius),
                (0, 255, 255), 2)
            cv2.circle(frame, center, 5, (0, 0, 255), -1)
    # update the points queue
    pts.appendleft(center)

        # loop over the set of tracked points
    for i in range(1, len(pts)):
        # if either of the tracked points are None, ignore
        # them
        if pts[i - 1] is None or pts[i] is None:
            continue
        # otherwise, compute the thickness of the line and
        # draw the connecting lines
        thickness = int(np.sqrt(args["buffer"] / float(i + 1)) * 2.5)
        cv2.line(frame, pts[i - 1], pts[i], (0, 0, 255), thickness)

 
    # show the frame to our screen
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF
    # if the 'q' key is pressed, stop the loop
    if key == ord("q"):
        break
# if we are not using a video file, stop the camera video stream

if not args.get("video", False):
    vs.stop()
# otherwise, release the camera
else:
    vs.release()

stop = time.time()
cv2.destroyAllWindows()
signal = generate_note(None,-10, duration=5.0)
sd.play(signal)
# close all windows


