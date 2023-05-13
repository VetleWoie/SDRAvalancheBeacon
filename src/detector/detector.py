import numpy as np
from numpy.lib.stride_tricks import as_strided
# import pyqtgraph as pg
# Lets use pyfftw to hopefully get some more speed
import pyfftw
import sys
# from PyQt5.QtWidgets import QApplication
from scipy import signal
from matplotlib import pyplot as plt


def vectorized_specgram(x, nfft, step, sr, window_func = signal.hann, dtype=None, mode='PSD'):

    if dtype is None:
        dtype = type(x[0])
    #Calculate number of steps needed for th fft
    n_steps = (len(x) - nfft) // step

    #Generate time vector from number of steps
    t_vec = np.arange(n_steps) * step / sr
    #Generate frequency vector
    f_vec = np.fft.fftshift(np.fft.fftfreq(nfft, 1/sr))
    
    #Find shape of output spectogram
    spec_shape = (f_vec.shape[0], n_steps)

    #Create byte aligned matricies for input and output
    sig = pyfftw.empty_aligned(spec_shape, dtype=dtype)
    Sxx = pyfftw.empty_aligned(spec_shape, dtype=dtype)

    #Make DFT plan, DFT should be done on the matricies over axis 0
    fft_obj = pyfftw.FFTW(sig, Sxx, axes=(0,))

    #Reshape x with strides magic, this does not use any more memory
    #it just changes the view of x
    strides = x.strides[0]
    shaped_x = as_strided(x, spec_shape, strides=(strides,strides*step))

    #Create window from input windowfunc
    window = window_func(nfft)

    #Copy the shaped x into byte aligned array and multiply with window
    sig[:] = shaped_x * window.reshape(-1,1)
    
    #Run FFT
    fft_obj()
    
    ##FFT shift the spectogram
    ##FFTW computes the non-normalized fft, so it needs to be normalized aswell
    Sxx = np.fft.fftshift(Sxx, axes=(0,))/nfft

    ##If wanted type is PSD return the power of the spectogram 
    if mode == 'PSD':
        Sxx = np.abs(Sxx)**2
    return f_vec, t_vec, Sxx 


def beacon_power(
    x,
    fs, # Sample rate of signal
    fc, # Frequency center of signal
    fo, # Frequency offset to frequency of interest
    max_freq_dev=1000,
    fft_step=20000,
):
    f_vec, t_vec, Sxx = vectorized_specgram(x, nfft=77000, step=fft_step, sr=fs, mode='PSD')
    # pg.show(np.abs(Sxx)**2)
    # frequency indices of interest
    fidx=np.where( np.abs(f_vec - fo) < max_freq_dev)[0]

    freq_vec2=f_vec[fidx]

    pwr=np.abs(Sxx[fidx,:])**2.0
    #noise_floor = np.median(pwr)

    #dB=dB-noise_floor

    # remove median power to remove constant tones
    for fi in range(pwr.shape[0]):
        # signal to noise ratio for each frequency bin
        pwr[fi,:]=(pwr[fi,:]-np.median(pwr[fi,:]))/np.median(pwr[fi,:])

    # detect center frequency
    # we know that the blips are within 70 ms
    duration=np.max(t_vec)-np.min(t_vec)
    # this is how many seconds there are in one time sample of the spectrogram
    dt=(fft_step/fs)

    # this is how many time samples contain a blip
    n_blip_samples=int((duration*70e-3)/dt)

    # go through each frequency bin
    # and count how much power is in blips
    total_blip_pwr=np.zeros(pwr.shape[0])
    for fi in range(pwr.shape[0]):
        # todo: could be improved by integrating power in one second segments
        # sum the peak power of each one second segment, because each time
        # sample is approximately the length of a blip (770 samples)
        idx=np.argsort(pwr[fi,:])
        total_blip_pwr[fi]=np.mean(pwr[fi,idx[(pwr.shape[1]-n_blip_samples):(pwr.shape[1])]])

    max_idx=np.argmax(total_blip_pwr)
    # estimate standard deviation with median
    std_estimate = np.median(np.abs(total_blip_pwr - np.median(total_blip_pwr)))
        
    # plot signal-to-noise ratio of blip pwr
    plt.plot(freq_vec2,total_blip_pwr/std_estimate)
    plt.axvline(freq_vec2[max_idx],color="red")
    plt.axhline(total_blip_pwr[max_idx]/std_estimate,color="red")
    plt.title("Amount of power in blips")
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("SNR/standard deviation")
    plt.show()

    # amount of power from beacon divided by one standard deviation
    beacon_blip_power_for_detection = total_blip_pwr[max_idx]/std_estimate

    # unnormalized peak detected power (for mapping power as a function of position)
    beacon_blip_power_for_mapping = total_blip_pwr[max_idx]

    print(f"Beacon blip detection power: {beacon_blip_power_for_detection}")
    print(f"Beacon blip power: {beacon_blip_power_for_mapping}")

    # make sure no negative value
    pwr[pwr<0]=1e-3

    dB=10.0*np.log10(pwr)    
    plt.pcolormesh(t_vec,freq_vec2,dB,vmin=-3,vmax=30)
    plt.axhline(freq_vec2[max_idx],color="red",alpha=0.3)
    plt.xlabel("Time (s)")
    plt.ylabel("Frequency (Hz)")
    #plt.pcolormesh(dB-noise_floor)
    plt.colorbar()
    plt.show()
    plt.show()


if __name__ == "__main__":
    # app = QApplication(sys.argv)

    data = np.fromfile(sys.argv[1], dtype=np.complex64)

    beacon_power(data,768e3,500e3, 457e3-500e3)

    # sys.exit(app.exec_())