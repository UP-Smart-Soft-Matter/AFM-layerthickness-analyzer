import os
import numpy as np
import matplotlib.pyplot as plt
import lmfit as lm
import glob

path = r"C:\Users\Mika Music\Nextcloud\Data\#AFM\20260428\x\facet tilt"
intervall_radius = 5
slope_change_threshold = 0.5
value_change_distance = 10
value_change_threshold = 5e-7

for path in glob.glob(os.path.join(path, "*.txt")):
    scan = np.genfromtxt(path, delimiter="\t")
    if scan.shape[0] > scan.shape[1]:
        scan = scan.T
    center_line = scan[16]

    slope_array = []
    slope_change_indizes = []
    for i in range(len(center_line)):
        if intervall_radius > i:
            start = 0
            stop = i+intervall_radius
            intervall = center_line[start:stop]
        elif intervall_radius <= i and i+intervall_radius <= len(center_line):
            start = i-intervall_radius
            stop = i+intervall_radius
            intervall = center_line[start:stop]
        else:
            start = i-intervall_radius
            stop = len(center_line)
            intervall = center_line[start:stop]
        x = np.arange(len(intervall))
        mod = lm.models.LinearModel()
        params = mod.guess(intervall, x=x)
        fit = mod.fit(intervall, params=params, x=x)
        fit_slope = fit.params['slope'].value
        slope_array.append(fit_slope)

    for i, slope in enumerate(slope_array):
        if i+1 > len(slope_array)-1:
            break
        if slope != 0:
            slope_change = 1 - slope_array[i+1]/slope
        else:
            slope_change = slope_array[i+1]
        if abs(slope_change) > slope_change_threshold:
            if i+value_change_distance > len(slope_array)-1:
                value_change = center_line[255]-center_line[i-value_change_distance]
            elif i-value_change_distance < 0:
                value_change = center_line[i+value_change_distance]-center_line[0]
            else:
                value_change = center_line[i+value_change_distance]-center_line[i-value_change_distance]
                print(value_change)
            if abs(value_change) > value_change_threshold:
                slope_change_indizes.append(i)



    x=np.arange(len(center_line))
    plt.plot(x, center_line)
    plt.plot(slope_change_indizes, center_line[slope_change_indizes], 'x')
    plt.title(path)
    plt.show()