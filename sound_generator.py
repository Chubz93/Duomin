#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# import pygame.midi as midi
from scipy.io import wavfile
import time
import pyaudio
import numpy as np


def sound_from_coordinate(coord):


    # relative to bottom left corner of frame as origin
    if coord[1] == '0' and coord[3] == '0':
        note = "piano-C4.wav"
        fs, data = wavfile.read(note)
        stream = pyaudio.PyAudio().open(
            rate=fs,
            channels=len(data.shape),
            format=pyaudio.paInt16,
            output=True,
        )

        stream.write(data.tobytes())
        stream.stop_stream()        
        time.sleep(1)
        stream.close()
        pyaudio.PyAudio.terminate

    # add way to average x and y and scale to some relative note
    #  







if __name__ == "__main__":
    try:
        while True:
            print("Enter coordinate pair, (x,y)")
            coord = input()
            
            print("Outputting sound")
            sound_from_coordinate(coord)
    
    except KeyboardInterrupt:
        print("Stopping...")

