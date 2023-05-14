from detector import beacon_power
import pyqtgraph as pg
from PyQt5.QtWidgets import QApplication
import sys
import numpy as np
from matplotlib import pyplot as plt

if __name__ == "__main__":
    app = QApplication(sys.argv)

    dir = sys.argv[1]

    fs = 768e3
    center_freq = 500e3
    freq = 457e3

    amp_power = []
    noamp_power = []
    
    detectionPowerAmp = []
    detectionPowerNoAmp = [] 

    distance = np.arange(1, 21, dtype=int)
    for i in distance:
        preamp = np.fromfile(dir+f"/distance_{i}/nonamp.bin", dtype=np.complex64)
        noamp = np.fromfile(dir+f"/distance_{i}/amp.bin", dtype=np.complex64)

        print(dir+f"/distance_{i}/nonamp.bin")

        powerNoamp, detectionNoAmp = beacon_power(noamp,fs,center_freq,freq)
        powerAmp, detectionAmp = beacon_power(preamp, fs,center_freq, freq)

        amp_power.append(powerAmp)
        noamp_power.append(powerNoamp)

        detectionPowerAmp.append(detectionAmp)
        detectionPowerNoAmp.append(detectionNoAmp)

    plt.plot(distance, amp_power, label="Active antenna")
    plt.plot(distance, noamp_power, label="Passive antenna")
    plt.title(f"Recieved beacon power")
    if len(sys.argv) >= 4:
        plt.suptitle(sys.argv[3])
    plt.legend()
    plt.xlabel("m")
    plt.ylabel("Power/Db")
    plt.yscale('log')
    plt.savefig('power_'+sys.argv[2])
    # plt.show()
    plt.clf()

    plt.plot(distance, detectionPowerAmp, label="Active antenna")
    plt.plot(distance, detectionPowerNoAmp, label="Passive antenna")
    plt.title("Beacon detection power")
    if len(sys.argv) >= 4:
        plt.suptitle(sys.argv[3])
    plt.legend()
    plt.xlabel("m")
    plt.ylabel("Power/Db")
    plt.yscale('log')
    plt.savefig('detection_'+sys.argv[2])
    # plt.show()

    # sys.exit(app.exec_())