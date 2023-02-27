import numpy as np
from matplotlib import pyplot as plt
import utils
import sys
from scipy import signal

if __name__=="__main__":
    alpha_avg_power = []
    beta_avg_power = []
    alpha_max_power = []
    for i in range(1,6):
        alpha = np.fromfile(f"{sys.argv[1]}/0d@{i}mr70cmd/alpha.bin",dtype=np.complex64)
        beta = np.fromfile(f"{sys.argv[1]}/0d@{i}mr70cmd/beta.bin",dtype=np.complex64)

        alpha_spec, alpha_freqs, alpha_t = utils.spectogram(alpha, NFFT=8192,Fs=768e3,Fc=457e3, noverlap=2048,  window=signal.windows.flattop(8192))
        beta_spec, beta_freqs, beta_t = utils.spectogram(beta, NFFT=8192,Fs=768e3,Fc=457e3, noverlap=2048,  window=signal.windows.flattop(8192))

        alpha_snr = np.array([utils.snr(f, 8192//2, 20,20,"linear") for f in alpha_spec.T])
        beta_snr = np.array([utils.snr(f, 8192//2, 20,20,"linear") for f in beta_spec.T])

        alpha_avg_power.append(utils.get_avarage_peak_power(alpha_snr,15))
        alpha_max_power.append(np.max(alpha_snr))
        beta_avg_power.append(utils.get_avarage_peak_power(beta_snr,7))

    M = 10e4
    r = np.linspace(1, 5, 100)    
    estimate = 10*np.log10(M*1/(r**6))
    plt.plot(r,estimate, label="Estimated signal power $\\frac{M}{r^6}$")
    plt.scatter(np.arange(1,6), alpha_avg_power, label="Alpha antenna avarage peak power")
    plt.scatter(np.arange(1,6), alpha_max_power, label="Alpha antenna max peak power")
    plt.scatter(np.arange(1,6), beta_avg_power, label="Beta antenna measurements")
    plt.savefig("distance.png")
    plt.title("Estimated signal power with measured signal power")
    plt.xlabel("distance/m")
    plt.ylabel("SNR/Db")
    plt.legend()
    plt.show()