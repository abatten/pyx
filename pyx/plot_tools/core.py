import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable


def plot_2d_array(data, xvals=None, yvals=None, extents=None, passed_ax=False, 
                  *args, **kwargs):
    """

    Parameters
    ----------
    data:

    xvals: numpy.ndarray, optional

    yvals: numpy.ndarray, optional

    extents: (xmin, xmax, ymin, ymax), optional
        These are

    passed_ax: 

    Returns
    -------
    im: matplotlib.collections.QuadMesh
        

    """
    if ((xvals is None and yvals is not None) or
        (yvals is None and xvals is not None)):
        msg = ("Both xvals and yvals must be either None or not None. "
               "You can't provide one without the other. "
               f"xvals is None: {xvals is None}, "
               f"yvals is None: {yvals is None}.")
        raise ValueError(msg)

    if passed_ax:

        axis = passed_ax
    else:
        fig = plt.figure()
        axis = fig.add_subplot(111)


    # If extents are provided and not xvals and yvals.
    # Calculate the new xvals and yvals
    if extents and not (xvals and yvals):
        xmin, xmax, ymin, ymax = extents
        yvals = np.linspace(ymin, ymax, data.shape[0])
        xvals = np.linspace(xmin, xmax, data.shape[1])

    if xvals is not None and yvals is not None:
        xx, yy = np.meshgrid(xvals, yvals)
        im = axis.pcolormesh(xx, yy, data, *args, **kwargs)

    else:
        im = axis.pcolormesh(data, *args, **kwargs)

    

    return im


def make_colorbar(im, ax, label=None, fontsize=14, *args, **kwargs):
    """
    """
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="5%", pad=0.05)
    cbar = plt.colorbar(im, cax=cax, *args, **kwargs)

    if label:
        cbar.set_label(label, fontsize=fontsize)
    return ax, cbar


