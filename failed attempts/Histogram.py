import os
import numpy as np
import matplotlib.pyplot as plt
import lmfit as lm
import glob

path = r"C:\Users\Mika Music\Nextcloud\Data\#AFM\20260428\x"
intervall_radius = 5
slope_change_threshold = 0.4
value_change_distance = 2

for path in glob.glob(os.path.join(path, "*.txt")):
    scan = np.genfromtxt(path, delimiter="\t")
    if scan.shape[0] > scan.shape[1]:
        scan = scan.T
    center_line = scan[16]

    histgram = np.histogram(scan, 500)

    x=np.arange(len(center_line))
    plt.plot(x, center_line)
    plt.title(os.path.basename(path)[:-4])
    plt.show()
    plt.close()
    plt.plot(histgram[0])
    plt.title(f"Histogram:{os.path.basename(path)[:-4]}")
    plt.show()