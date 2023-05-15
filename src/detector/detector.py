import numpy as np
from numpy.lib.stride_tricks import as_strided
import pyqtgraph as pg
# Lets use pyfftw to hopefully get some more speed
import pyfftw
import sys
from PyQt5.QtWidgets import QApplication
from scipy import signal
from matplotlib import pyplot as plt


# Static variables decorator
def static_vars(**kwargs):
    def decorate(func):
        for k in kwargs:
            setattr(func, k, kwargs[k])
        return func
    return decorate

@static_vars(wisdom_exists=False)
def vectorized_specgram(x, nfft, step, fs, window_func = signal.hann, dtype=None, mode='PSD', fftwflags = []):
    """
    Vectorized spectogram computation, using FFTW.

    @Params
    x: array_like
        - Time series measurment values
    nfft: int
        - Length of each fft
    step: int
        - Number of time series measurements to step between each fft
    fs: int
        - Sample rate of time series measurments in x
    window_func: function(int) -> array_like or none, 
        - Function used to create window, should take in a length and 
          return an array like object of length. If None then no 
          window is used
          Defaults to scipy.signal.hann
    dtype:  dtype or None
        - Datatype of x, if None then it is determined by type(x[0])
          Defaults to None
    mode: str{'PSD', 'magnitude', 'complex'}
        - Defines the expected return
          'PSD' - Return a power spectrum estimate
          'magnitude' - Return the magnitude of the spectogram
          'complex' - Raw fft results 
    fftwflags: list[str]
        - List of FFTW flags to use
          More information can be found here:
          https://pyfftw.readthedocs.io/en/latest/source/pyfftw/pyfftw.html
    
    @Returns
    f_vec: ndarray
        - Array of sample frequencies
    t_vec: ndarray
        - Array of segment times
    Sxx: ndarray
        - Spectogram of x
    """

    # If the method has been used once before then wisdom is allready cached
    if not vectorized_specgram.wisdom_exists:
        wisdom = None
        try:
            with open("/tmp/fftwSpec.wisdom", 'rb') as wisdom_file:
                wisdom = wisdom_file.readlines()
                pyfftw.import_wisdom(wisdom)
        except FileNotFoundError:
            # If wisdom file don't exist don't worry, well create it at the end
            pass

    if dtype is None:
        dtype = type(x[0])
    #Calculate number of steps needed for th fft
    n_steps = (len(x) - nfft) // step

    #Generate time vector from number of steps
    t_vec = np.arange(n_steps) * step / fs
    #Generate frequency vector
    f_vec = np.fft.fftshift(np.fft.fftfreq(nfft, 1/fs))
    
    #Find shape of output spectogram
    spec_shape = (f_vec.shape[0], n_steps)

    #Create byte aligned matricies for input and output
    sig = pyfftw.empty_aligned(spec_shape, dtype=dtype)
    Sxx = pyfftw.empty_aligned(spec_shape, dtype=dtype)

    #Make DFT plan, DFT should be done on the matricies over axis 0
    fft_obj = pyfftw.FFTW(sig, Sxx, axes=(0,), 
                            flags = [
                                'FFTW_DESTROY_INPUT'
                                ])

    #Reshape x with strides magic, this does not use any more memory
    #it just changes the view of x
    strides = x.strides[0]
    shaped_x = as_strided(x, spec_shape, strides=(strides,strides*step))

    #Copy the shaped x into byte aligned array and multiply with window
    sig[:] = shaped_x

    if window_func is not None:
        #Create window from input windowfunc
        window = window_func(nfft)
        sig *= window.reshape(-1,1)
    
    #Run FFT
    fft_obj()
    
    # FFT shift the spectogram
    # FFTW computes the non-normalized fft, so it needs to be normalized aswell
    Sxx = np.fft.fftshift(Sxx, axes=(0,))/nfft

    if mode == 'PSD':
        # If wanted type is PSD return the power of the spectogram 
        Sxx = np.abs(Sxx)**2
    elif mode == 'magnitude':
        Sxx = np.abs(Sxx)
    elif mode == 'complex':
        pass
    
    # Store wisdom in a tmp dictionary
    if not vectorized_specgram.wisdom_exists:
        #Write wisdom to tmp file
        if wisdom is None:
            wisdom = pyfftw.export_wisdom()
            with open("/tmp/fftwSpec.wisdom", 'wb') as wisdom_file:
                wisdom_file.writelines(wisdom)

    vectorized_specgram.wisdom_exists = True
    return f_vec, t_vec, Sxx 


def beacon_power(
    x,
    fs, # Sample rate of signal
    fc, # Frequency center of signal
    f, # Frequency of interest
    max_freq_dev=1000,
    fft_step=20000,
    plot = False
):
    fo = f - fc
    f_vec, t_vec, pwr = vectorized_specgram(x, nfft=77000, step=fft_step, fs=fs, mode='PSD')

    # Extract only frequencies indices of interest
    fidx=np.where( np.abs(f_vec - fo) < max_freq_dev)[0]
    freq_vec2=f_vec[fidx]
    pwr=pwr[fidx,:]

    # # Estimate noise using median of signal
    # noise = np.median(pwr, axis=1).reshape(-1,1)

    # #Calculate SNR
    # pwr = (pwr - noise) / noise
    # remove median power to remove constant tones
    for fi in range(pwr.shape[0]):
        # signal to noise ratio for each frequency bin
        pwr[fi,:]=(pwr[fi,:]-np.median(pwr[fi,:]))/np.median(pwr[fi,:])

    # detect center frequency of beacon signal, might be up to 80Hz offset from 457 kHz
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
        

    # amount of power from beacon divided by one standard deviation
    beacon_blip_power_for_detection = total_blip_pwr[max_idx]/std_estimate

    # unnormalized peak detected power (for mapping power as a function of position)
    beacon_blip_power_for_mapping = total_blip_pwr[max_idx]

    if plot:
        # plot signal-to-noise ratio of blip pwr
        plt.plot(freq_vec2,total_blip_pwr/std_estimate)
        plt.axvline(freq_vec2[max_idx],color="red")
        plt.axhline(total_blip_pwr[max_idx]/std_estimate,color="red")
        plt.title("Amount of power in blips")
        plt.xlabel("Frequency (Hz)")
        plt.ylabel("SNR/standard deviation")
        plt.show()

        # make sure no negative value
        pwr[pwr<0]=1e-3
        dB=10.0*np.log10(pwr)    
        plt.pcolormesh(t_vec,freq_vec2,dB,vmin=-3,vmax=30)
        plt.axhline(freq_vec2[max_idx],color="red",alpha=0.3)
        plt.xlabel("Time (s)")
        plt.ylabel("Frequency (Hz)")
        plt.colorbar()
        plt.show()

    return beacon_blip_power_for_mapping, beacon_blip_power_for_detection

if __name__ == "__main__":
    data = np.fromfile(sys.argv[1], dtype=np.complex64)
    
    beacon_blip_power_for_mapping,beacon_blip_power_for_detection = beacon_power(data,768e3,500e3, 457e3, plot=True)
    print(f"Beacon blip detection power: {beacon_blip_power_for_detection}")
    print(f"Beacon blip power: {beacon_blip_power_for_mapping}")
