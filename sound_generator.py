#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# import pygame.midi as midi
import wave
from scipy.io import wavfile
import time
import numpy as np
import math
import wavetable_synth
from wavetable_synth import Voice, WavetableOscillator, LinearInterpolator
import sounddevice as sd
import soundfile as sf

def generate_note(frequency):
    sampling_rate = 44100
    wavetable_size = 64

    # Create a mono synth
    synth = Voice(sampling_rate, gain=-20)

    ### Sine generation ###
    sine_table = wavetable_synth.generate_wavetable(wavetable_size, np.sin)
    # Add an oscillator
    synth.oscillators += [
        WavetableOscillator(
            sine_table,
            sampling_rate,
            LinearInterpolator())]
    # Synthesize sound
    sine = synth.synthesize(frequency, duration_seconds=1)
    # Save the output
    note = wavetable_synth.output_wavs(sine, 'sine', sampling_rate, sine_table)
    return note

def sound_from_coordinate(coord):
    coord = (int(coord[1]), int(coord[3]))

    # relative to bottom left corner of frame as origin
    if coord[0] == 0 and coord[1] == 0:
        note = generate_note(440)
        print(note)
        data, fs = sf.read(note, dtype='float32')
        sd.play(data, fs)
        status = sd.wait()



    # add way to average x and y and scale to some relative note
     







if __name__ == "__main__":
    sound_from_coordinate("(0,0)")
    # try:
    #     while True:
    #         print("Enter coordinate pair, (x,y)")
    #         coord = input()
            
    #         print("Outputting sound")
    #         sound_from_coordinate(coord)
    
    # except KeyboardInterrupt:
    #     print("Stopping...")

