import numpy as np
import scipy.stats as stats

def reshape_to_1D(array):
    """
    Reshapes an array to 1D

    Parameters
    ----------
    array: numpy.ndarray

    Returns
    -------
    1D array:

    """

    shape = array.shape

    total_elements = 1
    for axis in shape:
        total_elements = axis * total_elements

    return array.reshape(total_elements)


def calc_bin_centre(bin_edges):
    """
    Calculates the centre of a histogram bin fromthe big edges.

    """
    return bin_edges[:-1] + np.diff(bin_edges) / 2


def mean_median_mode(array):
    """
    Returns the mean, median and mode of an array

    Parameters
    ----------
    array: numpy.ndarray

    Returns:
    mean, median, mod
    """
    mean = np.mean(array)
    median = np.median(array)
    mode = stats.mode(array)[0][0]

    return mean, median, mode
