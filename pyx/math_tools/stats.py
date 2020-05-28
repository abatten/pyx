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


def gaussian(x, mu, sig, scale=None, normed=False):
    """
    Generates a gaussian curve 

    Parameters:
    x : numpy.ndarray
        x values

    mu : float or int
        The mean of the gaussian curve.

    sig : float or int
        The standard deviation of the gaussian curve.

    scale : float or int

    normed : boolean, optional
        If normed is true, the gassuan returned will be normalised such
        that the area under the curve intergrates to unity.
        Setting `normed = True` overrides the value in scale.
        Default: False

    """
    if scale is None:
        a = 1

    else:
        a = scale

    if normed:
        a = 1 / (sig * np.sqrt(2 * np.pi))

    return a * np.exp(-(x - mu)**2.0 / (2 * sig**2.0))



