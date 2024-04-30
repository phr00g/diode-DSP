import sounddevice as sd
import numpy as np
from scipy.optimize import fsolve

# Distortion parameters
R = 2.2e3    # Resistance (2.2 kΩ)
C = 10e-9    # Capacitance (10 nF)
Is = 2.52e-9 # Saturation current (2.52 nA)
Vt = 45.3e-3 # Thermal voltage (45.3 mV)

# Set up the audio stream parameters
samplerate = 88200  # Sample rate of 88200 Hz
blocksize = 128
device = 'Focusrite USB ASIO'  # Replace with the name of your Focusrite Solo ASIO driver

def diode_clipper(V, Vo, dt):
    def f(Vo_new):
        return Vo_new - Vo - dt * (((V - Vo_new) / (R * C)) - (2 * (Is / C)) * np.sinh(Vo_new / Vt))

    return fsolve(f, Vo)[0]

# Define the callback function for audio processing
def callback(indata, outdata, frames, time, status):
    if status:
        print(status)

    V = indata[:, 1]  # Use the second input channel
    Vo = np.zeros_like(V)

    for i in range(len(V)):
        if i == 0:
            Vo[i] = diode_clipper(V[i], 0, 1 / samplerate)
        else:
            Vo[i] = diode_clipper(V[i], Vo[i - 1], 1 / samplerate)

    outdata[:] = Vo.reshape(-1, 1)  # Output to both channels for stereo output

# Open the audio stream
with sd.Stream(device=(device, device),
               samplerate=samplerate, blocksize=blocksize,
               channels=2, callback=callback):  # Use 2 channels
    print("Listening to guitar input with distortion. Press Enter to stop.")
    input()

print("Audio processing finished.")