import numpy as np
import sounddevice as sd

# Parameters
R = 1e3    # Resistance (2.2 kΩ)
C = 10e-9    # Capacitance (10 nF)
Is = 2.52e-9 # Saturation current (2.52 nA)
Vt = 45.3e-3 # Thermal voltage (45.3 mV)

def diode_clipper(V, Vo, dt):
    def f(V, Vo):
        return (Is / C) * (np.exp((V - Vo) / Vt) - 1) + (V - Vo) / (R * C)

    k1 = f(V, Vo)
    k2 = f(V, Vo + 0.5 * dt * k1)
    k3 = f(V, Vo + 0.5 * dt * k2)
    k4 = f(V, Vo + dt * k3)

    return Vo + (dt / 6) * (k1 + 2 * k2 + 2 * k3 + k4)

def audio_callback(indata, outdata, frames, time, status):
    if status:
        print(status)

    V = indata[:, 0]
    Vo = np.zeros_like(V)

    for i in range(len(V)):
        if i == 0:
            Vo[i] = diode_clipper(V[i], 0, 1 / sample_rate)
        else:
            Vo[i] = diode_clipper(V[i], Vo[i - 1], 1 / sample_rate)

    outdata[:] = Vo.reshape(-1, 1)

# Audio settings
sample_rate = 44100
block_size = 128

# Open audio stream
with sd.Stream(callback=audio_callback, channels=1, samplerate=sample_rate,
               blocksize=block_size):
    print('Processing audio. Press Enter to stop.')
    input()

print('Audio processing finished.')