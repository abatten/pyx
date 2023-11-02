"""
PLOTS
-----
A collection of various functions for creating plots.

"""

__all__ = [
    'make_comoving_distance_axis', 
    'make_lookback_time_axis', 
    'pcolormesh2d'
    ]

import numpy as np
import matplotlib.pyplot as plt
import astropy.units as apu
import astropy.cosmology as acosmo
from pyx.cosmology import get_cosmology_from_name


def make_lookback_time_axis(ax, cosmo='Planck18', z_range=None, major_tick_spacing=2, minor_tick_spacing=1):
    """
    Creates a comoving distance axis on the top axis of a plot.

    Given a matplotlib axis, and assuming that the x-axis is
    a range of redshift values, creates a comoving distance axis 
    on the top axis in Gyrs.

    To use this ensure that that the xlims have been set to
    the correct redshift range (and must be greater than zero.)

    Parameters
    ----------
    ax: plt.Axes
        The matplotlib axis to draw the comoving distance axis. This
        axis should have a redshift x-axis.

    cosmo: str or astropy.cosmology.FLRW
        The cosmology to assume whilst calculating comoving distance.
        Default: 'Planck18'

    z_range:
        The redshift range to calculate comoving distance for. If None, 
        z_range will be the range of the redshift axis.
        Default: None

    major_tick_spacing: int, optional
        The major tick spacing in units of Gyr.
        Default: 2

    minor_tick_spacing: int, optional
        The minor tick spacing in units of Gyr.
        Default: 1

    Returns
    -------
    ax2: plt.Axes
        The matplotlib comoving distance axis.

    Example
    -------
    >>> import numpy as np
    >>> import matplotlib.pyplot as plt
    >>> from pyx import plots as pyxplots
    >>> fig, ax = plt.subplots(1, 1) 
    >>> x = np.linspace(0, 6, 100)
    >>> y = x**2
    >>> ax.plot(x, y)
    >>> ax.set_xlim(min(x), max(x))
    >>> ax2 = pyxplots.make_lookback_time_axis(ax)
    >>> ax.set_xlabel('Redshift')
    >>> ax2.set_xlabel('comoving distance (Gyr)')

    """
    ax2 = ax.twiny()

    if cosmo is None:
        cosmo = get_cosmology_from_name("Planck18")
    else: 
        cosmo = get_cosmology_from_name(cosmo)

    # If the redshift range is not provided calculate from axis.
    if z_range is not None:
        z_min, z_max = z_range
    else:
        tick_locs = ax.xaxis.get_majorticklocs()
        z_min, z_max = tick_locs[0], tick_locs[-1]

    lb_time_min = cosmo.lookback_time(z_min).value
    lb_time_max = cosmo.lookback_time(z_max).value

    lb_time_max_r = np.floor(lb_time_max / minor_tick_spacing) * minor_tick_spacing
    lb_time_min_r = np.ceil(lb_time_min / minor_tick_spacing) * minor_tick_spacing

    if (lb_time_max_r - lb_time_min_r) % major_tick_spacing == 0:
        minor_tick_labels = np.arange(lb_time_min_r + 1, lb_time_max_r + 1, minor_tick_spacing)
        major_tick_labels = np.arange(lb_time_min_r, lb_time_max_r + 1, major_tick_spacing)
    else:
        minor_tick_labels = np.arange(lb_time_min_r, lb_time_max_r + 1, minor_tick_spacing)
        major_tick_labels = np.arange(lb_time_min_r + 1, lb_time_max_r + 1, major_tick_spacing)

    # Create empty tick location lists
    major_tick_loc = np.zeros(len(major_tick_labels))
    minor_tick_loc = np.zeros(len(minor_tick_labels))

    # Calculate the position of the comoving distance Labels
    # Need to split them up because they can be different length arrays
    for idx, label in enumerate(major_tick_labels):
        if label < 0.01: # If Lookbacktime is too small -> Redshift = 0
            major_tick_loc[idx] = 0
        else:
            z_label = acosmo.z_at_value(cosmo.lookback_time, apu.Gyr * label)
            # This correctly accounts for if the min _redshift > 0.
            major_tick_loc[idx] = (z_label - z_min) / (z_max - z_min)

    for idx, label in enumerate(minor_tick_labels):
        if label < 0.01:
            minor_tick_loc[idx] = 0
        else:
            z_label = acosmo.z_at_value(cosmo.lookback_time, apu.Gyr * label)
            minor_tick_loc[idx] = (z_label - z_min) / (z_max - z_min)

    # Check if any tick_loc is larger than 1.0 and delete it if so:
    major_ticks_to_delete = np.where(major_tick_loc > 1)[0]
    minor_ticks_to_delete = np.where(minor_tick_loc > 1)[0]

    # Again splitting up because they can have different length arrays
    if len(major_ticks_to_delete) > 0:
        major_tick_loc = np.split(major_tick_loc, major_ticks_to_delete)[0]
        major_tick_labels = np.split(major_tick_labels, major_ticks_to_delete)[0]

    if len(minor_ticks_to_delete) > 0:
        minor_tick_loc = np.split(minor_tick_loc, minor_ticks_to_delete)[0]
        minor_tick_labels = np.split(minor_tick_labels, minor_ticks_to_delete)[0]

    # Display the tick marks
    ax2.set_xticks(major_tick_loc)
    ax2.set_xticks(minor_tick_loc, minor=True)

    # Only put numbers on the major ticks
    major_tick_labels = [f"{label:.0f}" for label in major_tick_labels]
    ax2.set_xticklabels(major_tick_labels)

    return ax2


def make_comoving_distance_axis(ax, cosmo='Planck18', z_range=None,
    minor_tick_spacing=500, major_tick_spacing=2000):
    """
    Creates a comoving distance axis on the top axis of a plot.

    Given a matplotlib axis, and assuming that the x-axis is
    a range of redshift values, creates a comoving distance axis 
    on the top axis in cMpc.

    To use this ensure that that the xlims have been set to
    the correct redshift range (and must be greater than zero.)

    Parameters
    ----------
    ax: plt.Axes
        The matplotlib axis to draw the comoving distance axis. This
        axis should have a redshift x-axis.

    cosmo: str or astropy.cosmology.FLRW
        The cosmology to assume whilst calculating comoving distance.
        Default: 'Planck18'

    z_range:
        The redshift range to calculate comoving distance for. If None, 
        z_range will be the range of the redshift axis.
        Default: None

    major_tick_spacing: int, optional
        The major tick spacing in units of cMpc.
        Default: 2

    minor_tick_spacing: int, optional
        The minor tick spacing in units of cMpc.
        Default: 1

    Returns
    -------
    ax2: plt.Axes
        The matplotlib comoving distance axis.

    Example
    -------
    >>> import numpy as np
    >>> import matplotlib.pyplot as plt
    >>> from pyx import plots as pyxplots
    >>> fig, ax = plt.subplots(1, 1) 
    >>> x = np.linspace(0, 6, 100)
    >>> y = x**2
    >>> ax.plot(x, y)
    >>> ax.set_xlim(min(x), max(x))
    >>> ax2 = pyxplots.make_comoving_distance_axis(ax)
    >>> ax.set_xlabel('Redshift')
    >>> ax2.set_xlabel('Comoving Distance (cMpc)')

    """
    ax2 = ax.twiny()

    if cosmo is None:
        cosmo = get_cosmology_from_name("Planck18")
    else: 
        cosmo = get_cosmology_from_name(cosmo)

    # If the redshift range is not provided calculate from axis.
    if z_range is not None:
        z_min, z_max = z_range
    else:
        tick_locs = ax.xaxis.get_majorticklocs()
        z_min, z_max = tick_locs[0], tick_locs[-1]

    dist_min = cosmo.comoving_distance(z_min).value
    dist_max = cosmo.comoving_distance(z_max).value

    # Round the min/max distances based on tick_spacing
    dist_max_r = np.floor(dist_max / minor_tick_spacing) * minor_tick_spacing
    dist_min_r = np.ceil(dist_min / minor_tick_spacing) * minor_tick_spacing

    minor_min_label = dist_min_r + minor_tick_spacing
    major_min_label = dist_min_r

    minor_max_label = dist_max_r + minor_tick_spacing
    major_max_label = dist_max_r + major_tick_spacing

    minor_tick_labels = np.arange(minor_min_label,
                                  minor_max_label,
                                  minor_tick_spacing)

    major_tick_labels = np.arange(major_min_label,
                                  major_max_label,
                                  major_tick_spacing)

    # Create empty tick location lists
    major_tick_loc = np.zeros(len(major_tick_labels))
    minor_tick_loc = np.zeros(len(minor_tick_labels))

    # Calculate the position of the comoving distance Labels
    # Need to split them up because they can be different length arrays
    for idx, label in enumerate(major_tick_labels):
        if label < 0.01: # If Comoving Distance is too small -> Redshift = 0
            major_tick_loc[idx] = 0
        else:
            z_label = acosmo.z_at_value(cosmo.comoving_distance, apu.Mpc * label)
            # This correctly accounts for if the min _redshift > 0.
            major_tick_loc[idx] = (z_label - z_min) / (z_max - z_min)

    for idx, label in enumerate(minor_tick_labels):
        if label < 0.01:
            minor_tick_loc[idx] = 0
        else:
            z_label = acosmo.z_at_value(cosmo.comoving_distance, apu.Mpc * label)
            minor_tick_loc[idx] = (z_label - z_min) / (z_max - z_min)

    # Check if any tick_loc is larger than 1.0 and delete it if so:
    major_ticks_to_delete = np.where(major_tick_loc > 1)[0]
    minor_ticks_to_delete = np.where(minor_tick_loc > 1)[0]

    # Again splitting up because they can have different length arrays
    if len(major_ticks_to_delete) > 0:
        major_tick_loc = np.split(major_tick_loc, major_ticks_to_delete)[0]
        major_tick_labels = np.split(major_tick_labels, major_ticks_to_delete)[0]

    if len(minor_ticks_to_delete) > 0:
        minor_tick_loc = np.split(minor_tick_loc, minor_ticks_to_delete)[0]
        minor_tick_labels = np.split(minor_tick_labels, minor_ticks_to_delete)[0]

    # Display the tick marks
    ax2.set_xticks(major_tick_loc)
    ax2.set_xticks(minor_tick_loc, minor=True)

    # Only put numbers on the major ticks
    major_tick_labels = [f"{label:.0f}" for label in major_tick_labels]
    ax2.set_xticklabels(major_tick_labels)

    return ax2



def pcolormesh2d(data, xvals=None, yvals=None, extents=None, ax=None, 
    *args, **kwargs):
    """
    Plots a 2D array using pcolormesh.

    Can provide both xvals and yvals for each pixel to create non-square
    pixels. Or, provide extents for linearly spaced pixels. 

    Only provide xvals & yvals or provide an extents tuple, not both. 
    Additional args and kwargs are passed to the pcolormesh function.

    Parameters
    ----------
    data:

    xvals: numpy.ndarray, optional

    yvals: numpy.ndarray, optional

    extents: (xmin, xmax, ymin, ymax), optional

    passed_ax:

    Returns
    -------
    im: matplotlib.collections.QuadMesh
        
    Examples
    --------
    >>> import numpy as np
    >>> array2d = np.random.randint(1,10, (10,10))
    >>> xvals = 2**np.linspace(1, 6)
    >>> yvals = 2**np.linspace(1, 6)
    >>> fig, ax = plt.subplots(1, 1)
    >>> im = plots.pcolormesh2d(array2d, xvals=xvals, yvals=yvals, ax=ax)
    
    >>> fig, ax = plt.subplots(1, 1)
    >>> im = plots.pcolormesh2d(array2d, extents=(0, 6, 0, 6), ax=ax)

    """
    if ((xvals is None and yvals is not None) or
        (yvals is None and xvals is not None)):
        msg = ("Both xvals and yvals must be either None or not None. "
               "You can't provide one without the other. "
               f"xvals is None: {xvals is None}, "
               f"yvals is None: {yvals is None}.")
        raise ValueError(msg)

    # If no axis is provided, create one.
    if ax is None:
        fig = plt.figure()
        ax = fig.add_subplot(111)

    # If extents are provided and not xvals and yvals.
    # Generate linearly spaced xvals and yvals.
    if extents and not (xvals and yvals):
        xmin, xmax, ymin, ymax = extents
        yvals = np.linspace(ymin, ymax, data.shape[0])
        xvals = np.linspace(xmin, xmax, data.shape[1])

    if xvals is not None and yvals is not None:
        xx, yy = np.meshgrid(xvals, yvals)
        im = ax.pcolormesh(xx, yy, data, *args, **kwargs)

    else:
        im = ax.pcolormesh(data, *args, **kwargs)

    return im
