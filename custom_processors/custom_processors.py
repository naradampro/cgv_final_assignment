import numpy as np 
from scipy import ndimage

def custom_threshold(image, threshold):
    # Apply thresholding using NumPy operations
    thresholded_image = np.where(image >= threshold, 255, 0).astype(np.uint8)

    return thresholded_image


def gaussian_kernel(size, sigma=1):
    size = int(size) // 2
    x, y = np.mgrid[-size:size+1, -size:size+1]
    normal = 1 / (2.0 * np.pi * sigma**2)
    g = np.exp(-((x**2 + y**2) / (2.0*sigma**2))) * normal
    return g

def gaussian_filter(img, kernal):
    gaussian_filtered = ndimage.convolve(img, kernal)

    return gaussian_filtered

