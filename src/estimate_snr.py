import numpy as np
from scipy import signal


def estimate_snr(x, fs,signal_threshold,cutoff_freq,frequency_shift = None, decimation_rate=1, return_stages = False, max_deviation_noise = 2):
    N = len(x)
    stages = []

    # Might need to frequency shift the signal to DC
    if frequency_shift is not None:
        t = np.arange(N)/fs
        x = x * np.exp(2j*np.pi*frequency_shift*t)
        if return_stages:
            stages.append(x.copy())
    # Pass signal through low pass filter to remove aliasing effects when decimating
    low_pass = signal.firwin(numtaps=101, cutoff=cutoff_freq, fs=fs)
    x = np.convolve(x, low_pass, 'valid')
    if return_stages:
            stages.append(x.copy())

    # Decimate the signal to a lower sampling rate
    x = x[::decimation_rate]
    # Got to adjust sampling rate after decimation
    fs = fs // decimation_rate
    if return_stages:
            stages.append(x.copy())

    signal_power = np.abs(x)**2

    # Find symbol areas(Areas where the signal is present)
    symbol_idx = np.where(signal_power > signal_threshold)[0]
    symbols = np.split(x[symbol_idx],np.where(np.diff(symbol_idx)!=1)[0]+1)
    if len(symbols) == 0 or (len(symbols) == 1 and len(symbols[0]) == 0):
        raise Exception("No symbols found in signal, with given threshold")
    # Find noise areas(Areas where the signal is not present)
    symbol_idx = np.where(signal_power < signal_threshold)[0]
    noise = np.split(x[symbol_idx],np.where(np.diff(symbol_idx)!=1)[0]+1)
    if len(noise) == 0 or (len(noise) == 1 and len(noise[0]) == 0):
        raise Exception("No noise found in signal with given threshold")
    # Find mean power of symbols
    for symbol in symbols:
        powers = []
        N = len(symbol)
        symbol = symbol * np.hamming(N)
        PSD = np.abs(np.fft.fft(symbol) ** 2 / (fs * N))
        PSD_log = 10 * np.log10(PSD)
        powers.append(np.max(PSD_log))
    avg_symbol_power = np.mean(powers)

    # Find mean power of noice
    for noise_area in noise:
        powers = []
        N = len(noise_area)
        noise_area = noise_area * np.hamming(N)
        PSD = np.abs(np.fft.fft(noise_area) ** 2 / (fs * N))
        PSD_log = 10 * np.log10(PSD)
        #Remove outliers from noise
        noise_mean = np.mean(PSD_log)
        noise_std = np.std(PSD_log)
        distance_from_mean = np.abs(PSD_log - noise_mean)
        not_outlier_idx = np.where(distance_from_mean < noise_std * max_deviation_noise)
        powers.append(np.mean(PSD_log))

    avg_noise_power = np.mean(powers)

    # Return SNR in decibels
    return (avg_symbol_power - avg_noise_power, stages if return_stages else None)