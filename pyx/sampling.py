"""
SAMPLING
--------
A collection of various functions and classes for performing different types
of sampling.

"""



__all__ = [
    'bootstrap_resample', 
    'InverseCDFSampler', 
    'jackknife_resample'
    ]

import numpy as np
import scipy.interpolate as interpolate

from pyx.utils import get_rng_from_seed


def bootstrap_resample(data, bootnum=100, num_samples=None, seed=None):
    """
    Performs a bootstrap resampling on an array.

    Parameters
    ----------
    data : array-like
        An array of length N
    bootnum : int, optional
        The number of bootstrap resamples. 
        Default: 100
    num_samples : None or int, optional
        The number of samples in each bootstrap resample. If None
        num_samples is equal to the length of data.
        Default: 100
    seed : None or int, optional
        The random seed that will be used to generate the numpy
        default_rng(). If None, a random seed will be used.
        Default: None

    Returns
    -------
    boot :
        An num_samples x bootnum array.

    Example
    -------
    >>> import numpy as np
    >>> from pyx import sampling as pyxsampling
    >>> rng = np.random.default_rng(seed=123456)
    >>> x = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 0])
    >>> xboot = pyxsampling.bootstrap_resample(x, 100, rng=rng)

    """
    rng = get_rng_from_seed(seed)

    if num_samples is None:
        num_samples = len(data)

    boot_dims = (bootnum, ) + (num_samples, )
    boot = np.empty(boot_dims)

    for i in range(bootnum):
         boot_idx_arr = rng.integers(low=0, high=len(data), size=num_samples)
         boot[i] = data[boot_idx_arr]
    return boot


def jackknife_resample(data):
    """
    Performs a jackknife resampling on an array.

    Jackknife resampling is a technique to generate 'n' deterministic samples
    of size 'n-1' from a measured sample of size 'n'. Basically, the i-th
    sample, (1<=i<=n), is generated by means of removing the i-th measurement
    of the original sample. Like the bootstrap resampling, this statistical
    technique finds applications in estimating variance, bias, and confidence
    intervals.

    Parameters
    ----------
    data : array-like
        An array of length N.

    Returns
    -------
    resamples : np.ndarray
        An N x N-1 array. Where the i-th row is the i-th jackknife sample
        with the i-th data point deleted. 

    Example
    -------
    >>> import numpy as np
    >>> from pyx import sampling as pyxsampling
    >>> x = np.ndarray([1,2,3,4,5,6,7,8,9,0])
    >>> jack_resamples = pyxsampling.jackknife_resampling(x)

    """
    if not isinstance(data, np.ndarray):
        data = np.array(data)

    resamples = np.empty([len(data), len(data) - 1])
    for idx, _ in enumerate(data):
        resamples[idx] = np.delete(data, idx)

    return resamples


class InverseCDFSampler(object):
    """
    Inverse Cumulative Distribution Sampler

    Performs an inverse cdf sample (also known as an inverse 
    transform) n times.

    The distribution does not need to be normalised. 
    Only need the x & y values of the distribution. 

    Parameters
    ----------
    xvals : array-like
        The x values.
    yvals : array-like
        The y values of the distribution.
    seed : None or int, optional
        The random seed that will be used to generate the numpy
        default_rng(). If None, a random seed will be used.
        Default: None

    Example
    -------
    >>> import numpy as np
    >>> from pyx import sampling as pyxsampling
    >>> xvals = np.linspace(-5, 5, 10)
    >>> yvals = np.abs(xvals)
    >>> icdf_sampler = pyxsampling.InverseCDFSampling(x, y, seed=12345)
    >>> samples = icdf_sampler.sample(1000)

    """
    def __init__(self, xvals, yvals, seed=None):
        self.rng = get_rng_from_seed(seed)
        self.x_input = xvals
        self.y_input = yvals
        self.sample  = None

        pdf_fnorm = np.sum(yvals)
        self.cdf = np.cumsum(yvals / pdf_fnorm)
        self.inverse_cdf = interpolate.interp1d(self.cdf, self.x_input)

    def sample_n(self, n):
        """
        Produces an array of random samples of length n with a
        distribution matched to the input arrays of x and y.

        Parameters
        ----------
        n : int
            The number of random samples to generate.

        Returns
        -------
        samples : np.ndarray
            The samples array of length n.

        """
        self.r_values = self.rng.uniform(self.cdf[0], self.cdf[-1], size=n)
        self.sample = self.inverse_cdf(self.r_values)
        return self.sample
