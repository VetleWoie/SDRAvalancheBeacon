from estimate_snr import estimate_snr
import pyqtgraph as pg
from PyQt5.QtWidgets import QApplication
import numpy as np
import sys


if __name__ == "__main__":
    app = QApplication(sys.argv)

    alpha_snrs = []
    beta_snrs = []
    for i in range(1,6):
        alpha = np.fromfile(f"{sys.argv[1]}/0d@{i}mr70cmd/alpha.bin",dtype=np.complex64)
        beta = np.fromfile(f"{sys.argv[1]}/0d@{i}mr70cmd/beta.bin",dtype=np.complex64)
        print(f"{sys.argv[1]}/0d@{i}mr70cmd/alpha.bin")
        alpha_snr, stages = estimate_snr(alpha, 768e3, 1.8e-7, 768, 0, 100, True)
        # beta_snr, _ = estimate_snr(beta, 768e3, 1.8e-7, 768, 0, 100)

        # pg.plot(np.abs(stages[-1])**2)
        
        # if input() == 'exit':
        #     exit()
        print(alpha_snr)
        alpha_snrs.append(alpha_snr)
        # beta_snrs.append(beta_snr)
    print(alpha_snrs)
    wg = pg.plot(alpha_snrs)
    # wg.plot(beta_snrs)

    status = app.exec_()
    sys.exit()
    
        