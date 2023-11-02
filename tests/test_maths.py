import numpy as np
import pytest

from pyx import maths as pyxmaths

def test_reshape_to_1D_1D_array():
    """
    Test reshaping a 1D array to a 1D array
    (should do nothing).

    """
    test_array = np.array([0, 1, 2, 3, 4, 5])
    reshaped_array = pyxmaths.reshape_to_1D(test_array)
    assert np.allclose(test_array, reshaped_array)

def test_reshape_to_1D_2D_array():
    """
    Test reshaping a 2D array to a 1D array

    """
    test_array = np.array([
                           [1, 2, 3],
                           [4, 5, 6],
                           [7, 8, 9]
                         ])

    expected_output_array = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9])
    reshaped_array = pyxmaths.reshape_to_1D(test_array)
    assert np.allclose(expected_output_array, reshaped_array)


def test_reshape_to_1D_3D_array():
    """
    Test reshaping a 3D array to a 1D array

    """
    test_array = np.array([
                           [[1, 2, 3],
                            [4, 5, 6],
                            [7, 8, 9]],

                           [[1, 2, 3],
                            [4, 5, 6],
                            [7, 8, 9]],

                           [[1, 2, 3],
                            [4, 5, 6],
                            [7, 8, 9]]
                          ])

    expected_output_array = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9,
                                      1, 2, 3, 4, 5, 6, 7, 8, 9,
                                      1, 2, 3, 4, 5, 6, 7, 8, 9])
    reshaped_array = pyxmaths.reshape_to_1D(test_array)
    assert np.allclose(expected_output_array, reshaped_array)
