import sounddevice as sd
import numpy as np

# Distortion parameters
R = 2.2e3    # Resistance (2.2 kΩ) 2.2e3
C = 10e-9    # Capacitance (10 nF)
Is = 2.52e-9 # Saturation current (2.52 nA)
Vt = 45.3e-2 # Thermal voltage (45.3 mV) 45.3e-3 #i like this value instead

# Set up the audio stream parameters
samplerate = 88200  # Sample rate of 88200 Hz
blocksize = 128
device = 'Focusrite USB ASIO'  # Replace with the name of your Focusrite Solo ASIO driver



def diode_clipper(V, Vo, dt): # using RK4 O(4n)
    def f(V, Vo):
        return ((V - Vo) / (R * C)) - (2 * (Is / C)) * np.sinh(Vo / Vt)

    k1 = f(V, Vo)
    k2 = f(V, Vo + 0.5 * dt * k1)
    k3 = f(V, Vo + 0.5 * dt * k2)
    k4 = f(V, Vo + dt * k3)

    return Vo + (dt / 6) * (k1 + 2 * k2 + 2 * k3 + k4)


# Define the callback function for audio processing
def callback(indata, outdata, frames, time, status):
    if status:
        print(status)

    V = indata[:, 1]  # Use the second input channel
    Vo = np.zeros_like(V)

    for i in range(len(V)):
        if i == 0:
            Vo[i] = diode_clipper(V[i], 0, 1 / samplerate) #init condition f(0) = 0 becuase we need something 
        else:
            Vo[i] = diode_clipper(V[i], Vo[i - 1], 1 / samplerate) #when past init condition

    outdata[:] = Vo.reshape(-1, 1)  # Output to both channels for stereo output

# Open the audio stream
with sd.Stream(device=(device, device),
               samplerate=samplerate, blocksize=blocksize,
               channels=2, callback=callback):  # Use 2 channels
    print("Listening to guitar input with distortion. Press Enter to stop.")
    input()

print("Audio processing finished.")