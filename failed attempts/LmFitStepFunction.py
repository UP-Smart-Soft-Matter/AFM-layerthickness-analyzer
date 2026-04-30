import os
import numpy as np
import matplotlib.pyplot as plt
import lmfit as lm
import glob

path = r"C:\Users\Mika Music\Nextcloud\Data\#AFM\20260428\x"

for path in glob.glob(os.path.join(path, "*.txt")):
    scan = np.genfromtxt(path, delimiter="\t")
    if scan.shape[0] > scan.shape[1]:
        scan = scan.T
    center_line = scan[16]

    x = np.linspace(0, len(center_line), len(center_line))

    model = lm.models.StepModel()
    params = model.guess(center_line, x)
    fit = model.fit(center_line, x=x, params=params)
    print(fit.fit_report())
    plt.plot(center_line)
    plt.plot(x, fit.best_fit)
    plt.title(path)
    plt.show()

