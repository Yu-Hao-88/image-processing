from random import random
from math import cos, sin, log, pi, sqrt

from numpy.core.fromnumeric import sort

gray_level_lower_bound = 0
gray_level_upper_bound = 255

levels = 100


def generation_additive_zero_mean_Gaussian_noise(sd, image_array):
    shape = image_array.shape
    image_array = image_array[:shape[0]//2 * 2, :shape[1]//2 * 2]
    shape = image_array.shape
    histogram_count = [0] * (levels * 2 + 1)  # -1 ~ 1

    for i in range(0, shape[0]):
        for l in range(0, shape[1], 2):
            r = random()
            phi = random()

            z1 = sd*cos(2*pi*phi)*sqrt(-2*log(r))
            z2 = sd*sin(2*pi*phi)*sqrt(-2*log(r))

            index_z1 = int((z1 + 1) / 0.01)
            index_z2 = int((z2 + 1) / 0.01)

            if index_z1 < len(histogram_count) and index_z1 > 0:
                histogram_count[index_z1] += 1

            if index_z2 < len(histogram_count) and index_z2 > 0:
                histogram_count[index_z2] += 1

            image_array[i][l] = __normalize_gray_level(
                round(image_array[i][l] + z1 * 255))
            image_array[i][l+1] = __normalize_gray_level(
                round(image_array[i][l+1] + z2 * 255))

    return image_array, histogram_count


def __normalize_gray_level(gray_level):
    if gray_level < gray_level_lower_bound:
        return gray_level_lower_bound

    if gray_level > gray_level_upper_bound:
        return gray_level_upper_bound

    return gray_level
