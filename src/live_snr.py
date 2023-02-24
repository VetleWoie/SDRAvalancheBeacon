from sys import stdin, argv
from matplotlib import pyplot as plt
import numpy as np


def snr(spec,signal_center, signal_width, noise_width, input_type='linear'):
    signal_min = signal_center-signal_width
    signal_max = signal_center+signal_width
    signal_amp = np.max(spec[signal_min:signal_max])
    noise_amp_left = np.max(spec[signal_min-noise_width:signal_min])
    noise_amp_right = np.max(spec[signal_max:signal_max+noise_width])
    noise_amp = noise_amp_left if noise_amp_left > noise_amp_right else noise_amp_right
    if input_type == 'linear':
        return 10*np.log10(signal_amp/noise_amp)
    elif input_type == 'dbm':
        return signal_amp-noise_amp
    else:
        raise ValueError(f"Unkown input type: \"{input_type}\", has to be one of [\"dbm\", \"linear\"]")
    
if __name__=="__main__":
    fft_lenght = int(argv[1])
    plt.ion()
    fig, ax = plt.subplots(1,1)
    ax.set_yscale('log')
    ax.set_ylim(top=4)

    binary = stdin.buffer.read(fft_lenght*64)
    data = np.frombuffer(binary, dtype=np.complex64, count=fft_lenght)
    freq = np.fft.fftshift(np.abs(np.fft.fft(data)))
    signal = snr(freq, fft_lenght//2, 20,20)
    line, = ax.plot(freq)
    ax.set_title(f"SNR: {signal}db")

    while True:
        binary = stdin.buffer.read(fft_lenght*64)
        data = np.frombuffer(binary, dtype=np.complex64, count=fft_lenght)
        freq = np.fft.fftshift(np.abs(np.fft.fft(data)))
        signal = snr(freq, fft_lenght//2, 20,20)
        if signal > 7:
            print(signal)
        line.set_ydata(freq)
        fig.canvas.draw()
        fig.canvas.flush_events()
