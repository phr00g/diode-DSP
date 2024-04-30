import sounddevice as sd
import numpy as np

# Set up the audio stream parameters
samplerate = 88200
blocksize = 128
device = 'Focusrite USB ASIO'  # Replace with the name of your Focusrite Solo ASIO driver

# Define the callback function for audio processing
def callback(indata, outdata, frames, time, status):
    if status:
        print(status)
    outdata[:] = indata

# Open the audio stream
with sd.Stream(device=(device, device),
               samplerate=samplerate, blocksize=blocksize,
               channels=1, callback=callback):
    print("Listening to guitar input. Press Enter to stop.")
    input()

print("Audio processing finished.")