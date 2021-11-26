import numpy as np
import astropy.units as apu
import astropy.constants as apc
import astropy.cosmology as acosmo





def z_to_cMpc(redshift, cosmology='Planck15'):
    """
    Convert a redshift into a comoving distance with units of Mpc.

    Parameters
    ----------
    redshift: array-like, shape (N, )
        The redshift values. Must be 1D or scalar.

    cosmology: string or astropy.cosmology.core.FLRW
        The cosmology used to calculate distance. This can either be a
        string of the cosmology keyword used in astropy (e.g 'Planck13'
        or 'WMAP7') or an instance of an astropy.cosmology.
        Default: 'Planck15'

    Returns
    -------
    distance: astropy.unit.quantity.Quantity
        The distance to a redshift in comoving Mpc.

    Examples
    --------
    >>> cosmology.z_to_cMpc(2)
    <Quantity 5311.53878858 Mpc>

    >>> cosmology.z_to_cMpc(2, cosmology="WMAP7")
    <Quantity 5279.26488146 Mpc>

    >>> import astropy.cosmology as acosmo
    >>> P13 = acosmo.Planck13
    >>> cosmology.z_to_cMpc(2, cosmology=Planck13)
    <Quantity 5310.8891027 Mpc>

    >>> cosmology.z_to_cMpc(2, cosmology="WMAP7")
    <Quantity 5279.26488146 Mpc>

    >>> redshifts = np.array([0, 1, 2, 3])
    >>> cosmology.z_to_cMpc(redshifts)
    <Quantity [0. , 3395.90541667, 5311.53878858, 6509.79588814] Mpc>

    """

    cosmo = get_cosmology_from_name(cosmology)

    distance = cosmo.comoving_distance(redshift)

    # If the redshift is really small the user likely wants the result
    # to be at 0.0 Mpc. 1e-4 Mpc is 100 pc.
    distance_zero_threshold = 1e-4 * apu.Mpc

    distance[distance < distance_zero_threshold] = 0

    return distance


def cMpc_to_z(cMpc, cosmology="Planck15"):
    """
    Convert a comoving distance with units Mpc into a redshift.

    Parameters
    ----------
    cMpc: array-like, shape (N, )
        The distance values. Must be 1D or scalar.

    cosmology: string or astropy.cosmology.core.FLRW
        The cosmology used to calculate distance. This can either be a
        string of the cosmology keyword used in astropy (e.g 'Planck13'
        or 'WMAP7') or an instance of an astropy.cosmology.
        Default: 'Planck15'

    Returns
    -------
    redshift: astropy.unit.Quantity
        The distance to a redshift in comoving Mpc.

    Examples
    --------

    """

    cosmo = get_cosmology_from_name(cosmology)

    # If the array doesn't have units, apply them for calculation later.
    if not isinstance(cMpc, apu.Quantity):
        cMpc = cMpc * apu.Mpc

    # If the comoving distance is really small the user likely wants the
    # result to be at 0.0 redshift. 1e-4 Mpc is approx 100 pc.
    distance_zero_threshold = 1e-4 * apu.Mpc

    # Check of the input distances is a list or a scalar.
    distance_is_scalar = cMpc.isscalar

    # If the distance is a scalar, perform a scalar calculation.
    if distance_is_scalar:
        if cMpc >= distance_zero_threshold:
            redshift = acosmo.z_at_value(cosmo.comoving_distance, cMpc)
        else:
            redshift = 0.0

    # If the distance is an array, perform array calculation
    else:
        # Default value is 0.0 redshift
        redshift = np.zeros_like(cMpc.value)

        for i, dist in enumerate(cMpc):
            if dist >= distance_zero_threshold:
                redshift[i] = acosmo.z_at_value(cosmo.comoving_distance, dist)

    return redshift


def get_cosmology_from_name(cosmology):
    """
    Get an astropy cosmology from a name.

    Parameters
    ----------
    cosmology: string or astropy.cosmology.core.FLRW
        The cosmology to obtain. This can either be a string of the
        cosmology keyword used in astropy (e.g 'Planck13' or 'WMAP7')
        or an instance of an astropy.cosmology.

    Returns
    -------
    cosmo: astropy.cosmology.core.FLRW
        An astropy cosmology.

    """

    # This list should be updated when astropy releases the Planck18 cosmology
    available_cosmologies = {
        "WMAP5": acosmo.WMAP5,
        "WMAP7": acosmo.WMAP7,
        "WMAP9": acosmo.WMAP9,
        "Planck13": acosmo.Planck13,
        "Planck15": acosmo.Planck15,
    }

    # If the user uses a string for the cosmology look it up in the dict.
    # If they specify a cosmology class, use that instead.
    if isinstance(cosmology, str):
        if cosmology in available_cosmologies.keys():
            cosmo = available_cosmologies[cosmology]
        else:
            msg = (f"""The cosmology '{cosmology}' is not in the list of
            available cosmologies with string keywords. The list
            if available cosmologies accessable via keyword are:
            {available_cosmologies.keys()}""")
            raise ValueError(msg)

    elif isinstance(cosmology, acosmo.core.FLRW):
        cosmo = cosmology

    return cosmo


def scale_factor(redshift):
    """
    Calculates the scale factor, a, at a given redshift.

    a = (1 + z)**-1

    Parameters
    ----------
    redshift: array-like
        The redshift values.

    Returns
    -------
    a: array-like
        The scale factor at the given redshift.

    Examples
    --------
    >>> scale_factor(1)
    0.5

    >>> scale_factor(np.array([0, 1, 2, 3]))
    array([1, 0.5, 0.3333333, 0.25])

    """

    a = (1 + redshift)**-1.0
    return a


def comoving_to_physical(dist_comoving, redshift):
    """
    Converts a comoving distance to a physical distance.

    This assume a Flat Lambda CDM Cosmology.

    dist_physical = dist_comoving * scale_factor

    Parameters
    ----------
    dist_comoving: array-like

    redshift:

    Returns
    -------
    dist_physical: array-like
        The physical distance of the array.

    """
    return dist_comoving * scale_factor(redshift)


def physical_to_comoving(dist_physical, redshift):
    """
    Converts a physical distance to a comoving distance.

    This assume a Flat Lambda CDM Cosmology.

    dist_comoving = dist_physical / scale_factor

    Parameters
    ----------
    dist_physical: array-like

    redshift:

    Returns
    -------
    dist_comoving: array-like
        The physical distance of the array.

    """
    return dist_physical / scale_factor(redshift)


def make_lookback_time_axis(ax, cosmo=None, z_range=None,
    major_tick_spacing=2, minor_tick_spacing=1):

    """
    Parameters
    ----------
    ax


    Returns
    -------
    ax2:
        The matplotlib axis for the lookback time

    """
    ax2 = ax.twiny()

    if cosmo is None:
        cosmo = get_cosmology_from_name("Planck15")

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

    # Calculate the position of the Lookback Time Labels
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
    major_tick_labels = [f"$\mathrm{label:.0f}$" for label in major_tick_labels]
    ax2.set_xticklabels(major_tick_labels)

    return ax2




def make_comoving_distance_axis(ax, cosmo=None, z_range=None,
    minor_tick_spacing=250, major_tick_spacing=1000):

    """
    Adds

    This assumes that the x-axis of the plot is redshift.


    Parameters
    ----------
    ax:

    cosmo:
        If None, it will load the Planck15 cosmology from Astropy.
        Default: None

    z_range: optional
        Default: None

    major_tick_spacing: int, optional
        Default: 1000

    minor_tick_spacing: int, optional
        Default: 250

    Returns
    -------
    ax2:
        The matplotlib axis for the lookback time

    """
    ax2 = ax.twiny()

    if cosmo is None:
        cosmo = get_cosmology_from_name("Planck15")

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

    # Calculate the position of the Lookback Time Labels
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
    major_tick_labels = [f"$\mathrm{label:.0f}$" for label in major_tick_labels]
    ax2.set_xticklabels(major_tick_labels)

    return ax2
