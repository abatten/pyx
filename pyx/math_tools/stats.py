import numpy as np
import scipy.stats as stats

def mean_median_mode(array):
    """
    Returns the mean, median and mode of an array

    Parameters
    ----------
    array: numpy.ndarray

    Returns:
    mean, median, mode

    """
    mean = np.mean(array)
    median = np.median(array)
    mode = stats.mode(array)[0][0]

    return mean, median, mode