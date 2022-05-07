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

sampling_rate = 44110
wavetable_size = 64
sine_table = wavetable_synth.generate_wavetable(wavetable_size, np.sin)
sawtooth_table = wavetable_synth.generate_wavetable(wavetable_size, wavetable_synth.sawtooth_waveform)

def generate_note(instantaneous_frequency, gain, duration):
    # Create a mono synth
    synth = Voice(sampling_rate, gain)
    ### Sine generation ###
    # Add an oscillator
    synth.oscillators += [
        WavetableOscillator(
            sine_table,
            sampling_rate,
            LinearInterpolator()),
        # WavetableOscillator(
        #     sawtooth_table,
        #     sampling_rate,
        #     LinearInterpolator())
        ]
    
    # Synthesize sound
    # instantaneous_frequency = 256*(2**(instantaneous_frequency/600)).astype('int32')
    # lengthen = (duration*sampling_rate//len(instantaneous_frequency)) + 1
    # print(lengthen)
    # instantaneous_frequency = np.repeat(instantaneous_frequency, lengthen)
    # instantaneous_frequency = 256*(2**(instantaneous_frequency/600)).astype('float64')
    # instantaneous_frequency += np.multiply(instantaneous_frequency,
    #                                        np.random.default_rng().uniform(-0.1, 0.1, size=instantaneous_frequency.shape))
    
    # print(instantaneous_frequency.shape)
    duration = 10
    min_frequency = 200
    max_frequency = 3000

    # Calculate the base of the exponent
    base = (max_frequency / min_frequency) ** (1 /
                                               (duration // 2 * sampling_rate))

    # Calculate the exponential frequency sweep on the rising slope
    instantaneous_frequency_half = min_frequency * \
        base ** np.arange(0, duration // 2 * sampling_rate, 1)

    # Make the falling slope the reverse of the first slope
    instantaneous_frequency = np.concatenate(
        (instantaneous_frequency_half, np.flip(instantaneous_frequency_half)))

    # Add tiny oscillations around the intantaneous frequency
    instantaneous_frequency += np.multiply(instantaneous_frequency,
                                           np.random.default_rng().uniform(-0.1, 0.1, size=instantaneous_frequency.shape))

    # Synthesize on a sample-by-sample basis and output
   
    signal_with_varying_frequency = synth.synthesize(
        frequency=instantaneous_frequency, duration_seconds=duration)
    # Save the output
    return signal_with_varying_frequency

def sound_from_coordinate(coord):
    gain_scale = -10
    if coord == None:
        return generate_note(0, gain_scale)
    # relative to bottom left corner of frame as origin
    else:
        
        return generate_note(128*freq_scale, gain_scale)



    # add way to average x and y and scale to some relative note
     


