import os
import numpy as np
import matplotlib.pyplot as plt
import lmfit as lm
import glob
import copy
import scipy as sp
import uncertainties


path = r"C:\Users\Mika Music\Nextcloud\Data\#AFM\20260428\test"
intervall_radius = 5
slope_threshold = 1e-9


for path in glob.glob(os.path.join(path, "*.txt")):
    scan = np.genfromtxt(path, delimiter="\t")
    if scan.shape[0] > scan.shape[1]:
        scan = scan.T

    layer_thickness_array_uncertainties = []

    for j in range(scan.shape[0]):
        line = scan[j]
        threshold = np.nanmean(line)
        top_level_array = line[line > threshold]
        top_level_median = np.median(line[line > threshold])
        top_level_mad = sp.stats.median_abs_deviation(top_level_array)
        bottom_level_array = line[line < threshold]
        bottom_level_median = np.median(line[line < threshold])
        bottom_level_mad = sp.stats.median_abs_deviation(bottom_level_array)

        top_level = uncertainties.ufloat(top_level_median, top_level_mad)
        bottom_level = uncertainties.ufloat(bottom_level_median, bottom_level_mad)


        layer_thickness_measurement = top_level - bottom_level
        layer_thickness_array_uncertainties.append(layer_thickness_measurement)

        plt.plot(line)
        plt.plot(np.arange(len(line)), np.full(len(line), top_level_median))
        plt.plot(np.arange(len(line)), np.full(len(line), bottom_level_median))
        plt.title(f"{os.path.basename(path)}: line {j}")
        plt.xlabel("measurement point [1]")
        plt.ylabel("height [m]")
        plt.show()

    layer_thickness_value = []
    layer_thickness_error = []

    for value in layer_thickness_array_uncertainties:
        layer_thickness_value.append(value.nominal_value)
        layer_thickness_error.append(value.std_dev)

    weights = 1 / np.array(layer_thickness_error) ** 2
    layer_thickness_mean = np.average(layer_thickness_value, weights=weights)

    scatter_var = np.average((np.array(layer_thickness_value) - layer_thickness_mean) ** 2, weights=weights)
    scatter_err = np.sqrt(scatter_var)
    stat_err = np.sqrt(1 / np.sum(weights))
    total_err = np.sqrt(stat_err ** 2 + scatter_err ** 2)

    layer_thickness = uncertainties.ufloat(layer_thickness_mean, total_err)

    print(layer_thickness)