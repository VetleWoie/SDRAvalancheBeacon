import numpy as np
from matplotlib import pyplot as plt
def snr(spec : np.ndarray,signal_center : int, signal_width : int, noise_width : int, input_type : str='linear') -> float:
    """
    Returns the signal to noise ratio for a given frequenzy
    @param
    spec - FFT to compute signal to ration over
    signal_center - Center frequenzy of signal in question
    noise_width - Widht of noise to check
    input_type - Specify wether spec is given in decibels or linear format

    @returns
    signal to noise ratio
    """
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

def get_avarage_peak_power(arr : np.ndarray,threshold : int) -> float:
    """
    Returns avarage of all power peaks beyond threshold value
    @param
    arr - Array of peak data
    threshold - threshold value to use
    
    @returns
    avarage peak value above threshold
    """
    peak_idx = np.where(arr > threshold)
    return np.mean(arr[peak_idx])

def spectogram(signal, NFFT, Fs,Fc,noverlap,window):
    spec, freqs, t, _ = plt.specgram(signal,NFFT=NFFT,Fs=Fs,Fc=Fc,noverlap=noverlap, window=window)
    plt.clf()
    return (spec, freqs, t)