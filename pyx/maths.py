"""
MATHS
-----
A collection of various mathematical functions.

"""

__all__ = [
    "angle_of_line_through_points", 
    "bin_centres",
    "deg2rad",
    "hist_pdf",
    "linearly_interpolate_pdfs",
    "linspace_angles",
    "moving_mean",
    "pdf_mean",
    "pdf_median",
    "pdf_percentile"
    "pdf_std",
    "pdf_var",
    "rad2deg", 
    "rebin1d",
    "reshape_to_1D",
    "sigma_pdf_percentiles",
    ]

import numpy as np
from scipy import interpolate, special


def angle_of_line_through_points(point, point2=(0.0, 0.0), axis='x', units='deg'):
    """
    Calculates the angle (degrees) between the x-axis and a line drawn
    to a point.

    Parameters
    ----------
    point: (float, float)
        The point.

    point2: (float, float), optional
        A second point to define the line.
        Default: (0.0, 0.0)

    axis: {'x', 'y'}, optional
        The axis to calculate the angle to.
        Default: 'x'
    
    unit: {'deg', 'rad'}, optional
        The unit that the angles are in.
        Default: 'deg'

    Returns
    -------
    angle: float
        The angle to the axis.

    """
    x, y = point
    x0, y0 = point2
    xdelta = x - x0
    ydelta = y - y0
    
    # Can swap the order to calculate angle to y axis.
    if axis.lower() in ['x', 'xaxis', 'x-axis']:
        rad = np.arctan2(ydelta, xdelta)
    elif axis.lower() in ['y', 'yaxis', 'y-axis']:
        rad = np.arctan2(xdelta, ydelta)

    if units.lower() in ['rad', 'radians']:
        return rad

    elif units.lower() in ['deg', 'degrees']:
        deg = rad2deg(rad)
        return deg


def bin_centres(bin_edges):
    """
    Calculates the centre of a histogram bin from the bin edges.

    Parameters
    ----------
    bin_edges: array-like
        An array of bin edges on length N.

    Returns
    -------
    centres: np.ndarray
        An array of bin centers of length N-1.
    
    """
    return bin_edges[:-1] + np.diff(bin_edges)/2

def deg2rad(theta, wrap=False):
    """
    Converts an angle in degrees into radians.

    Parameters
    ----------
    theta: float or np.ndarray
        An angle or angle array in degrees.

    wrap: bool, optional
        If wrap=True, return a value between 0 and 2pi.
        Default: False
    
    Returns
    -------
    rad: float or np.ndarray
        The angle or angle array theta in radians.
    """
    rad = theta * np.pi / 180
    if wrap:
          rad = rad % (2*np.pi)
    return rad


def hist_pdf(hist, bin_widths):
    """
    Normalise a histogram into a probability density function. 

    Parameters
    ----------
    hist: np.ndarray
        The histogram array of length N.

    bin_widths: np.ndarray
        An array of length N containing the width of each bin.
        This can be calculated with np.diff(edges).

    Returns
    -------
    pdf: np.ndarray
        The probability density function.

    """
    if np.sum(hist) < 1e-16:
        pdf = np.zeros(len(hist))
    else:
        pdf = hist / bin_widths / np.sum(hist)
    return pdf


def linearly_interpolate_pdfs(sample, xvals, pdfs):
    """
    Linearly interpolate between two probability density fuctions
    (PDFs) that are associated with two scalars.

    Parameters
    ----------
    sample: float
        A sample scalar to generate an interpolate PDF.
        This sample value sould be between the xvals.

    xvals: (float, float)
        Two scalars that are each associated with a PDF.
    
    pdfs: (np.ndarray, np.ndarray) 
        Two PDFs, with the first PDF associated with the first scalar,
        and the second PDF with the second scalar.
    
    Returns
    -------
    PDF: np.ndarray
        The interpolated PDF at the sample value.

    """
    x1, x2 = xvals
    pdf1, pdf2 = pdfs

    grad = (pdf2 - pdf1) / (x2 - x1)
    dist = sample - x1

    return grad*dist + pdf1


def linspace_angles(start, stop, num=50, unit='deg', **kwargs):
    """
    Returns evenly spaced angles over a specified interval.

    Returns num evenly spaced angle samples, calculated over the interval [start, stop].
    The endpoint of the interval can optionally be excluded.

    Parameters
    ----------
    start: float
        The starting value of the sequence.

    stop: float
        The end value of the sequence.

    num: int, optional
        The number of samples to generate. Must be non-negative.
        Default: 50

    unit: {'deg', 'rad'}, optional
        The unit that the angles are in.
        Default: 'deg'

    Returns
    -------
    samples: np.ndarray
        There are num equally spaced angle samples in the closed interval [start, stop]

    """

    if unit.lower() in ['degrees', 'deg']:
        rotation_angle = 360
    elif unit.lower() in ['radians', 'rad']:
        rotation_angle = 2 * np.pi

    if start < stop:
        samples = np.linspace(start, stop, num, **kwargs) % rotation_angle
    elif start > stop:
        # This uses the fact that angles are cyclic.
        # Here we add the full rotation angle to get a positive angle.
        # e.g  The Angle range (330 to 30) is the same as ((0 to 60) + 330) % 360
        samples = (np.linspace(0, rotation_angle + stop - start, num, **kwargs) + start) % rotation_angle
    
    return samples


def moving_mean(x, w, mode='full'):
    """
    Calculates the moving average of a dataset within a window.

    Uses a convolution to calculate the moving average wintin a window.
    = np.convolve(x, np.ones(w), mode=mode) / w

    Parameters
    ----------
    x: np.ndarray or array-like
        The dataset

    w: int
        The width of the window.
    
    mode: {'full', 'valid', 'same'}, optional
        'full': 
            By default, mode is 'full'. This returns the moving 
            average at each point of overlap, with an output shape
            of (N+M-1,). At the end-points of the convolution, the 
            window and dataset do not overlap completely, and 
            boundary effects may be seen.
        'same': 
            Mode 'same' returns output of length max(M, N). 
            Boundary effects are still visible.
        'valid': 
            Mode 'valid' returns output of length 
            max(M, N) - min(M, N) + 1. The moving average is only
            given for points where the window and data overlap
            completely.

    Returns
    -------
    moving_avg: np.ndarray
        The moving average of the array x within the window.

    """
    return np.convolve(x, np.ones(w), mode=mode) / w


def pdf_mean(x, pdf, dx=None):
    """
    Calculates the mean of a probability density function

    Parameters
    ----------
    x : np.ndarray
        The x values.

    pdf : np.ndarray
        The value of the PDF at x.

    dx : np.ndarray or None, optional
        The spacing between the x bins. 
        If `None`, then the bins are assumed to be linearly spaced.

    Returns
    -------
    mean : float
        The mean of the PDF.

    """
    if dx is None:
        # If no dx is provided assume they are linearly spaced
        dx = (x[-1] - x[0]) / len(x)
    return np.sum(pdf * x * dx)


def pdf_median(x, pdf):
    """
    Calculates the median of a PDF.

    Parameters
    ----------
    x : np.ndarray
        The x values.

    pdf : np.ndarray
        The value of the PDF at x.

    Returns
    -------
    median: float
        The median value (50% percentile) of the PDF.

    """
    return pdf_percentile(x, pdf, percentile=0.5)


def pdf_percentile(x, pdf, percentile):
    """
    Calculates the x value that corresponds to a given percentile
    in a probability density function.

    Parameters
    ----------
    x : np.ndarray
        The x values of the PDF.

    pdf : np.ndarray
        The value of the PDF at x.

    percentile : float
        The percentile of the PDF (range 0 - 1).

    Returns
    -------
    value : float
        The x value that corresponds to the given percentile.

    """
    cumsum = np.cumsum(pdf)
    normed_cumsum = cumsum / cumsum[-1]
    interpolated_cumsum = interpolate.interp1d(normed_cumsum, x)
    return interpolated_cumsum(percentile)


def pdf_std(x, pdf, dx=None):
    """
    Calculates the standard deviation from a probability
    density function.

    Parameters
    ----------
    x : np.ndarray
        The x values.

    pdf : np.ndarray
        The value of the PDF at x.

    dx : np.ndarray or None, optional
        The spacing between the x bins. 
        If `None`, then the bins are assumed to be linearly spaced.

    Returns
    -------
    std : float
        The standard deviation of the PDF.

    """
    if dx is None:
        # If no dx is provided assume they are linearly spaced
        dx = (x[-1] - x[0]) / len(x)
    return np.sqrt(pdf_var(x, pdf, dx))


def pdf_var(x, pdf, dx=None):
    """
    Calculates the variance from a probability density
    function.

    Parameters
    ----------
    x : np.ndarray
        The x values.

    pdf : np.ndarray
        The value of the PDF at x.

    dx : np.ndarray or None, optional
        The spacing between the x bins. 
        If `None`, then the bins are assumed to be linearly spaced.

    Returns
    -------
    variance : float
        The variance of the PDF.

    """

    if dx is None:
        # If no dx is provided assume they are linearly spaced
        dx = (x[-1] - x[0]) / len(x)
    mean = pdf_mean(x, pdf, dx)
    return np.sum(pdf * dx * (x - mean)**2)


def rad2deg(theta, wrap=False):
    """
    Converts an angle in radians into degrees.

    Parameters
    ----------
    theta: float or np.ndarray
        An angle or an array of angles in radians.

    wrap: bool, optional
        If wrap=True, return the values between 0 and 360.
        Default: False
    
    Returns
    -------
    deg: float or np.ndarray
        The angle or angle array theta in degrees.
    """
    deg = theta * 180 / np.pi
    if wrap:
          deg = deg % (360)
    return deg


def rebin1d(array, bin_size):
    """
    Rebins 1D data into a smaller number of bins.

    Parameters
    ----------
    array: array-like
        The 1D array of length N.

    bin_size: int
        The number of bins to be combined into new bins.
        If bin_size is not a divisor of N, then the remaining
        bins will be left off.

    Returns
    -------
    new_arrays: array-like
        The of new rebined array of length int(N/bin_size).

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


def reshape_to_1D(array):
    """
    Reshapes a multidimensional array into 1D.

    Parameters
    ----------
    array: numpy.ndarray
        An N x M x ... array.

    Returns
    -------
    1D array: np.ndarray
        The output 1D array of length N x M x ..

    """
    total_elements = np.prod(array.shape)
    return np.reshape(array, total_elements)


def sigma_pdf_percentiles(sigma):
    """
    Calculates the percentile range of a Gaussian for a given
    standard deviation.

    Parameters
    ----------
    sigma: float
        The standard deviation to calculate a percentile.

    Returns
    -------
    Lower: float
        The lower percentile.
    Higher: float
        The higher percentile.

    Example
    -------
    >>> sigma_pdf_percentiles(1)
    (0.15865525393145707, 0.8413447460685429)

    >>> sigma_pdf_percentiles(2.5)
    (0.006209665325776159, 0.9937903346742238)

    """
    if sigma < 0.0:
        raise ValueError("Sigma must be creater than zero.")
    sigma_prop = special.erf(sigma/np.sqrt(2))
    return (1 - sigma_prop)/2, (1 + sigma_prop)/2

