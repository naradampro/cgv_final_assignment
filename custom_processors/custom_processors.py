import numpy as np

def custom_threshold(image, threshold):
    # Apply thresholding using NumPy operations
    thresholded_image = np.where(image >= threshold, 255, 0).astype(np.uint8)

    return thresholded_image

