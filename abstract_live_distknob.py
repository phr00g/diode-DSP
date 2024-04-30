import sounddevice as sd
import numpy as np
import tkinter as tk


# Set up the audio stream parameters
samplerate = 88200 # Sample rate of 88200 Hz
blocksize = 128
device = 'Focusrite USB ASIO' # Replace with the name of your Focusrite Solo ASIO driver

# Global variable to store the gain value
gain = 1.0

def tanh_distortion(x, gain):
    return np.tanh(gain * x)

def callback(indata, outdata, frames, time, status):
    if status:
        print(status)
    V = indata[:, 1] # Use the second input channel
    Vo = np.zeros_like(V)
    for i in range(len(V)):
        Vo[i] = tanh_distortion(V[i], gain)
    outdata[:] = Vo.reshape(-1, 1) # Output to both channels for stereo output

def update_gain(val):
    global gain
    gain = float(val)

# Create the main window
window = tk.Tk()
window.title("Guitar Distortion")

# Create the gain slider
gain_slider = tk.Scale(window, from_=1, to=100, orient=tk.HORIZONTAL, length=200, resolution=1, command=update_gain)
gain_slider.set(1)
gain_slider.pack()

# Start the audio stream
stream = sd.Stream(device=(device, device), samplerate=samplerate, blocksize=blocksize, channels=2, callback=callback)
stream.start()

# Run the Tkinter event loop
window.mainloop()

# Stop the audio stream
stream.stop()
stream.close()