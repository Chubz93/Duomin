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
import pyaudio

sampling_rate = 2500
wavetable_size = 64
sine_table = wavetable_synth.generate_wavetable(wavetable_size, np.sin)

def generate_note(frequency, gain):
    # Create a mono synth
    synth = Voice(sampling_rate, gain=gain)
    ### Sine generation ###
    # Add an oscillator
    synth.oscillators += [
        WavetableOscillator(
            sine_table,
            sampling_rate,
            LinearInterpolator())]
    # Synthesize sound
    sine = synth.synthesize(frequency, duration_seconds=0.01)
    # Save the output
    note = sd.play(sine,sampling_rate)
    return note

def sound_from_coordinate(coord):
    if coord == None:
        pass
    # relative to bottom left corner of frame as origin
    else:
        freq_scale = 2**(600/coord[0])
        gain_scale = map(   )
        generate_note(256*freq_scale, )



    # add way to average x and y and scale to some relative note
     


