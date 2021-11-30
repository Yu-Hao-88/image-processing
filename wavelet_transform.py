import numpy as np


def wave_transform(layer, image_array):
    x, y = image_array.shape
    new_image_array = __transform(image_array)
    new_image_array = new_image_array * 5
    for i in range(1, layer):
        temp_image_array = new_image_array
        x, y = temp_image_array.shape
        temp_image_array = __transform(
            temp_image_array[:x//(2**i), :y//(2**i)])
        temp_image_array = __brighter(temp_image_array)
        new_image_array = __merge(temp_image_array, new_image_array)

    return new_image_array


def __brighter(image):
    x, y = image.shape
    for i in range(x):
        for l in range(y):
            if i < x//2 and l < y//2:
                continue
            image[i][l] *= 5
    return image


def __merge(temp, new):
    x, y = temp.shape
    for i in range(x):
        for l in range(y):
            new[i][l] = temp[i][l]

    return new


def __transform(image_array):
    x, y = image_array.shape
    new_image_array = np.zeros((x, y))
    x_counter = 0
    for i in range(0, x, 2):
        y_counter = 0
        for l in range(0, y, 2):
            a = image_array[i][l]
            b = image_array[i][l+1]
            c = image_array[i+1][l]
            d = image_array[i+1][l+1]

            new_image_array[0 + x_counter][0 +
                                           y_counter] = __normaile((a+b+c+d)/4)
            new_image_array[0 + x_counter][y//2 +
                                           y_counter] = __normaile((a-b+c-d)/4)
            new_image_array[x//2 + x_counter][0 +
                                              y_counter] = __normaile((a+b-c-d)/4)
            new_image_array[x//2 + x_counter][y//2 +
                                              y_counter] = __normaile((a-b-c+d)/4)

            y_counter += 1
        x_counter += 1

    return new_image_array


def __normaile(x):
    rt = abs(round(x))
    return rt
