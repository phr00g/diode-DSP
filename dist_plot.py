import numpy as np
import soundfile as sf
import matplotlib.pyplot as plt

# Distortion parameters
R = 2.2e3    # Resistance (2.2 kΩ)
C = 10e-9    # Capacitance (10 nF)
Is = 2.52e-9 # Saturation current (2.52 nA)
Vt = 45.3e-3 # Thermal voltage (45.3 mV)

def diode_clipper(V, Vo, dt):
    # using RK4 O(4n)
    def f(V, Vo):
        return ((V - Vo) / (R * C)) - (2 * (Is / C)) * np.sinh(Vo / Vt)

    k1 = f(V, Vo)
    k2 = f(V, Vo + 0.5 * dt * k1)
    k3 = f(V, Vo + 0.5 * dt * k2)
    k4 = f(V, Vo + dt * k3)
    return Vo + (dt / 6) * (k1 + 2 * k2 + 2 * k3 + k4)

# Load the prerecorded sample 'clean.wav'
clean_signal, samplerate = sf.read('clean.wav')

# Apply distortion to the clean signal
distorted_signal = np.zeros_like(clean_signal)
dt = 1 / samplerate
gain = 1.3 #NOTE ADDING GAIN ECCENTUAETS PLOT
for i in range(len(clean_signal)):
    if i == 0:
        distorted_signal[i] = diode_clipper(clean_signal[i] * gain, 0, dt)
    else:
        distorted_signal[i] = diode_clipper(clean_signal[i]*gain, distorted_signal[i - 1], dt)

# Plot the clean and distorted signals
time = np.arange(len(clean_signal)) / samplerate

plt.figure(figsize=(10, 4))
plt.plot(time, clean_signal, label='Clean Signal')
plt.plot(time, distorted_signal, label='Distorted Signal')
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')
plt.title('Diode Clipping Distortion')

plt.xlim(0.02,0.04)
plt.tight_layout()
plt.show()