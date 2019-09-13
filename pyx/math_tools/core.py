import numpy as np

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

    return array.reshape(1, total_elements)

