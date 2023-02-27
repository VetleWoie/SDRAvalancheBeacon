import numpy as np
from scipy import signal
from matplotlib import pyplot as plt
import sys
from utils import snr

if __name__ == "__main__":
    datafolder = sys.argv[1]

    fig, ax = plt.subplots(2,2)
    alpha = np.fromfile(f"{datafolder}/alpha.bin",dtype=np.complex64)
    beta = np.fromfile(f"{datafolder}/beta.bin",dtype=np.complex64)

    fig.suptitle(sys.argv[2])

    
    spec, freqs, t, im = ax[0][0].specgram(alpha,NFFT=8192,Fs=768e3,Fc=457e3,noverlap=2048, window=signal.windows.flattop(8192))
    ax[0][0].set_title("Spectogram Alpha")
    ax[0][0].set_ylabel("frequency/hz")
    ax[0][0].set_xticklabels([])
    db_spec = 10*np.log10(spec)
    signaltonoise = np.array([snr(f, 8192//2, 20,20,"dbm") for f in db_spec.T])
    ax[0][1].plot(t,signaltonoise)
    ax[0][1].set_title("SNR Alpha")
    ax[0][1].set_ylabel("db")
    ax[0][1].set_xticklabels([])

    spec, freqs, t, im = ax[1][0].specgram(beta,NFFT=8192,Fs=768e3,Fc=457e3,noverlap=2048, window=signal.windows.flattop(8192))
    ax[1][0].set_title("Spectogram Beta")
    ax[1][0].set_ylabel("frequency/hz")
    ax[1][0].set_xlabel("time/s")
    db_spec = 10*np.log10(spec)
    signaltonoise = np.array([snr(f, 8192//2, 20,20,"dbm") for f in db_spec.T])
    ax[1][1].plot(t,signaltonoise)
    ax[1][1].set_title("SNR Beta")
    ax[1][1].set_ylabel("db")
    ax[1][1].set_xlabel("time/s")
    
    if len(sys.argv) > 3:
        plt.savefig(sys.argv[3],bbox_inches='tight')
    plt.show()

