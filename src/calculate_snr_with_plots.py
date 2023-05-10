import pyqtgraph as pg
import numpy as np
from PyQt5.QtWidgets import QApplication
from scipy import signal
import sys


app = QApplication(sys.argv)

datafolder = '../signals/moving_reciver/'
file = 'alpha.bin'
alpha = np.fromfile(f"{datafolder}/{file}",dtype=np.complex64)

N = 768000
fs = 768000
s = 0
e = s+4
s = int(s * fs)
e = int(e * fs)

N = len(alpha)

subSignal = alpha
# subSignal = alpha[s:e]
period = 10
avg_filter = np.full(N, 1/N)

t = N / fs


x = np.linspace(0,t,N)
pw = pg.plot(x,np.abs(subSignal)**2, pen='red')

# Freq shift
f_o = 0#-57e3 # amount we need to shift by
t = np.arange(N)/fs # time vector
shifted_signal = subSignal * np.exp(2j*np.pi*f_o*t) # down shift

PSD = np.abs(np.fft.fft(shifted_signal)) ** 2 / (fs * N)
PSD_log = 10 * np.log10(PSD)
PSD_shift = np.fft.fftshift(PSD_log)

center_freq = 457e3
f = np.arange(fs/-2,fs/2, fs/N)
f += center_freq
# pg.plot(f, PSD_shift, pen='orange')

#Low pass
# Low-Pass Filter
taps = signal.firwin(numtaps=101, cutoff=768, fs=fs)
filtered_signal = np.convolve(shifted_signal, taps, 'valid')
Nf = len(filtered_signal)
PSD = np.abs(np.fft.fft(filtered_signal)) ** 2 / (fs * Nf)
PSD_log = 10 * np.log10(PSD)
PSD_shift = np.fft.fftshift(PSD_log)

center_freq = 457e3
f = np.arange(fs/-2,fs/2, fs/Nf)
f += center_freq
# pg.plot(f, PSD_shift, pen='blue')


#Decimate signal
decimation_amount = 1
decimated_signal = filtered_signal[::decimation_amount]
fs = fs // decimation_amount
Nd = len(decimated_signal)

# decimated_signal = decimated_signal * np.hamming(Nd)
PSD = np.abs(np.fft.fft(decimated_signal)) ** 2 / (fs * Nd)
PSD_log = 10 * np.log10(PSD)
PSD_shift = np.fft.fftshift(PSD_log)

center_freq = 457e3
f = np.arange(fs/-2,fs/2, fs/Nd)
f += center_freq
# pg.plot(f, PSD_shift, pen='pink')

# x = np.linspace(0,t,Nd)
pg.plot(np.abs(decimated_signal)**2, pen ='green')

print("Signal Mean:", np.mean(np.abs(decimated_signal)**2))

idx = np.where(np.abs(decimated_signal)**2 > 1.8e-7)[0]
print(idx[:5])

aout = np.split(decimated_signal[idx],np.where(np.diff(idx)!=1)[0]+1)
print(decimated_signal[idx].shape)
print(len(aout))

#Find mean all recieved symbols
for sig in aout:
    powers = []
    N = len(sig)
    sig = sig * np.hamming(N)
    PSD = np.abs(np.fft.fft(sig)) ** 2 / (fs * N)
    PSD_log = 10 * np.log10(PSD)
    PSD_shift = np.fft.fftshift(PSD_log)

    center_freq = 457e3
    f = np.arange(fs/-2,fs/2, fs/N)
    f += center_freq
    powers.append(np.max(PSD_shift))
print("Avg measured power: ",np.mean(powers), "dBw")
signal_power = np.mean(powers)
#Find noise floor
idx = np.where(np.abs(decimated_signal)**2 < 0.0001)[0]
print(idx[:5])

aout = np.split(decimated_signal[idx],np.where(np.diff(idx)!=1)[0]+1)
print(decimated_signal[idx].shape)
print(len(aout))
#Find avarage noise value between symbols
for noise in aout:
    powers = []
    N = len(noise)
    noise = noise * np.hamming(N)
    PSD = np.abs(np.fft.fft(noise)) ** 2 / (fs * N)
    PSD_log = 10 * np.log10(PSD)
    PSD_shift = np.fft.fftshift(PSD_log)

    center_freq = 457e3
    f = np.arange(fs/-2,fs/2, fs/N)
    f += center_freq
    pg.plot(PSD_shift)
    noise_mean = np.mean(PSD_shift)
    noise_std = np.std(PSD_shift)
    max_deviations = 2
    distance_from_mean = np.abs(PSD_shift-noise_mean)
    not_outlier_idx = np.where(distance_from_mean < noise_std * max_deviations)
    PSD_without_outlier = PSD_shift[not_outlier_idx]
    pg.plot(PSD_without_outlier)
    powers.append(np.mean(PSD_without_outlier))
noise_power = np.mean(powers)
print("Avg noise power: ", np.mean(powers), "dBw")


print(f"SNR: {signal_power-noise_power}")
status = app.exec_()
sys.exit(status)
