import numpy as np
from scipy import signal
from matplotlib import pyplot as plt
import sys

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
    
if __name__ == "__main__":
    datafolder = sys.argv[1]

    fig, ax = plt.subplots(2,2)
    alpha = np.fromfile(f"{datafolder}/alpha.bin",dtype=np.complex64)
    beta = np.fromfile(f"{datafolder}/beta.bin",dtype=np.complex64)

    
    spec, freqs, t, im = ax[0][0].specgram(alpha,NFFT=8192,Fs=768.1e3,Fc=457e3,noverlap=2048)
    ax[0][0].set_title("Spectogram Alpha")
    ax[0][0].set_ylabel("frequency/hz")
    ax[0][0].set_xlabel("time/s")
    db_spec = 10*np.log10(spec)
    signaltonoise = np.array([snr(f, 8192//2, 20,20,"dbm") for f in db_spec.T])
    ax[0][1].plot(t,signaltonoise)
    ax[0][1].set_title("SNR Alpha")
    ax[0][1].set_ylabel("db")
    ax[0][1].set_xlabel("time/s")

    spec, freqs, t, im = ax[1][0].specgram(beta,NFFT=8192,Fs=768.1e3,Fc=457e3,noverlap=2048)
    ax[1][0].set_title("Spectogram Beta")
    ax[1][0].set_ylabel("frequency/hz")
    ax[1][0].set_xlabel("time/s")
    db_spec = 10*np.log10(spec)
    signaltonoise = np.array([snr(f, 8192//2, 20,20,"dbm") for f in db_spec.T])
    ax[1][1].plot(t,signaltonoise)
    ax[1][1].set_title("SNR Beta")
    ax[1][1].set_ylabel("db")
    ax[1][1].set_xlabel("time/s")
    
    plt.show()

