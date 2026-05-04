import os
import numpy as np
import matplotlib.pyplot as plt
import glob
import copy
import scipy as sp
import uncertainties
import json


path = r"C:\Users\Mika Music\Nextcloud\Data\#AFM\20260428\x\facet tilt"
intervall_radius = 5
slope_threshold = 1e-9

def linear(x, a, b):
    return a * x + b

result_dict = dict()

for path in glob.glob(os.path.join(path, "*.txt")):
    scan = np.genfromtxt(path, delimiter="\t")
    if scan.shape[0] > scan.shape[1]:
        scan = scan.T

    layer_thickness_array_uncertainties = []

    for j in range(scan.shape[0]):
        line = scan[j]

        slope_array = []
        indizes = []
        cleand_line = copy.deepcopy(line)
        for i in range(len(line)):
            if intervall_radius > i:
                start = 0
                stop = i+intervall_radius
                intervall = line[start:stop]
            elif i > len(line):
                start = i-intervall_radius
                stop = len(line)
                intervall = line[start:stop]
            else:
                start = i-intervall_radius
                stop = i+intervall_radius
                intervall = line[start:stop]
            x = np.arange(len(intervall))
            slope, _ = sp.optimize.curve_fit(linear, x, intervall)
            slope_array.append(slope[0])


        for i, slope in enumerate(slope_array):
            if i+1 > len(slope_array)-1:
                break
            if abs(slope) > slope_threshold:
                cleand_line[i] = np.nan

        threshold = np.nanmean(cleand_line)
        top_level_array = cleand_line[cleand_line > threshold]
        top_level_median = np.median(cleand_line[cleand_line > threshold])
        top_level_mad = sp.stats.median_abs_deviation(top_level_array)
        bottom_level_array = cleand_line[cleand_line < threshold]
        bottom_level_median = np.median(cleand_line[cleand_line < threshold])
        bottom_level_mad = sp.stats.median_abs_deviation(bottom_level_array)

        top_level = uncertainties.ufloat(top_level_median, top_level_mad)
        bottom_level = uncertainties.ufloat(bottom_level_median, bottom_level_mad)


        layer_thickness_measurement = top_level - bottom_level
        layer_thickness_array_uncertainties.append(layer_thickness_measurement)

        plt.plot(line)
        plt.plot(cleand_line)
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

    result = {
        "layer_thickness": layer_thickness_mean,
        "error": total_err
    }
    result_dict[os.path.basename(path)] = result

    print(f"{os.path.basename(path)}:\n\tlayer thickness = {layer_thickness_mean} +/- {total_err}")

with open(f"{os.path.join(os.path.dirname(path), "layer_tickness.json")}", "w") as f:
    json.dump(result_dict, f)