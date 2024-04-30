import numpy as np
import matplotlib.pyplot as plt

# Distortion parameters
R = 2.2  # Resistance (2.2 kΩ)
C = 10  # Capacitance (10 nF)
Is = 2.52  # Saturation current (2.52 nA)
Vt = 45.3  # Thermal voltage (45.3 mV)

def diode_clipper(V, Vo, dt):
    def f(V, Vo):
        return ((V - Vo) / (R * C)) - (2 * (Is / C)) * np.sinh(Vo / Vt)

    k1 = f(V, Vo)
    k2 = f(V, Vo + 0.5 * dt * k1)
    k3 = f(V, Vo + 0.5 * dt * k2)
    k4 = f(V, Vo + dt * k3)
    return Vo + (dt / 6) * (k1 + 2 * k2 + 2 * k3 + k4)

# Generate a sine wave
samplerate = 44100  # Sample rate of 44100 Hz
duration = 0.1  # Duration of the sine wave in seconds
t = np.linspace(0, duration, int(samplerate * duration), endpoint=False)
freq = 440  # Frequency of the sine wave (440 Hz)
amplitude = 1  # Amplitude of the sine wave
sine_wave = amplitude * np.sin(2 * np.pi * freq * t)

# Apply diode clipping to the sine wave
distorted_sine = np.zeros_like(sine_wave)
dt = 1 / samplerate
for i in range(len(sine_wave)):
    if i == 0:
        distorted_sine[i] = diode_clipper(sine_wave[i], 0, dt)
    else:
        distorted_sine[i] = diode_clipper(sine_wave[i], distorted_sine[i - 1], dt)

# Plot the original and distorted sine waves
plt.figure(figsize=(10, 4))
plt.plot(t, sine_wave, label='Original Sine Wave')
plt.plot(t, distorted_sine, label='Distorted Sine Wave')
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')
plt.title('Diode Clipping Distortion on a Sine Wave')
plt.legend()
plt.tight_layout()
plt.show()