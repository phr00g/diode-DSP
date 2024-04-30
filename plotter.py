import numpy as np
import soundfile as sf
import matplotlib.pyplot as plt

def tanh_distortion(x, gain):
    return np.tanh(gain * x)

def lowpass_filter(x, cutoff, fs):
    b = cutoff / (cutoff + fs)
    y = np.zeros_like(x)
    y[0] = b * x[0]
    for n in range(1, len(x)):
        y[n] = b * x[n] + (1 - b) * y[n-1]
    return y

def process_audio(input_file, output_file, gain, tone, volume):
    # Load the input audio file
    audio, fs = sf.read(input_file)

    # Apply distortion
    distorted = tanh_distortion(audio, gain)

    # Apply tone control
    filtered = lowpass_filter(distorted, tone, fs)

    # Adjust output volume
    output = volume * filtered

    time = len(audio)/fs
    t = np.linspace(0,time,len(audio))
    
    # Save the output audio file
    sf.write(output_file, output, fs)
    return audio, t,output

# Example usage
input_file = 'clean.wav'
output_file = 'distorted.wav'
gain = 100.0
tone = 2000.0
volume = 0.5

audio , times,out = process_audio(input_file, output_file, gain, tone, volume)
analogue, sff  = sf.read('analogue.wav')
analogue = analogue * 2


#plt.plot(times,out,label ='tanh dist')
#plt.plot(times,audio,label='clean')
plt.plot(times,analogue,label='analoge (gain amplified)')
#plt.legend()
plt.xlim(0,0.04)



plt.show()


