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
    Calculates the centre of a histogram bin from the bin edges.

    """
    return bin_edges[:-1] + np.diff(bin_edges) / 2

import numpy as np

def rebin(array, bin_size):
    """
    Rebins 1D data

    Parameters
    ----------
    array: array-like

    bin_size: int
        The number of elements

    """
    if not isinstance(bin_size, int):
        msg = ("bin_size must have type int")
        raise ValueError(msg)

    if bin_size > len(array):
        msg = ("bin_size must be less than the length of array")
        raise ValueError(msg)

    if bin_size < 1:
        msg = ("bin_size must have value greater or equal to 1")
        raise ValueError(msg)

    # Calculate the length of the new array
    # Note that if the array isn't divisible by bin_size
    # It will leave off the remaining bins
    new_size = int(array.size / bin_size)

    # Generate a new empty array for the new bins
    new_array = np.zeros(new_size)

    # Loop over each of the new bins
    for idx in range(new_size):

        # Calculate the start and end points for each new bin
        start_idx = idx * bin_size
        end_idx = start_idx + bin_size

        # Combine the bins between start_idx and end_idx
        new_array[idx] = np.sum(array[start_idx:end_idx])

    return new_array