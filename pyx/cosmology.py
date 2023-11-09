"""
COSMOLOGY
---------
A collection of various functions for doing cosmological calculations.

"""

__all__ = [
    'cMpc_to_z', 
    'get_cosmology_from_name', 
    'scale_factor', 
    'z_to_cMpc',
]

import numpy as np
import astropy.units as apu
import astropy.constants as apc
import astropy.cosmology as acosmo
import astropy.cosmology.units as acu


def get_cosmology_from_name(cosmology):
    """
    Get an astropy cosmology from a name.

    Parameters
    ----------
    cosmology : string or astropy.cosmology.core.FLRW
        The cosmology to obtain. This can either be a string of the
        cosmology keyword used in astropy (e.g 'Planck13' or 'WMAP7')
        or an instance of an astropy.cosmology.

    Returns
    -------
    cosmo : astropy.cosmology.core.FLRW
        An astropy cosmology.

    """
    available_cosmologies = {
        "WMAP5": acosmo.WMAP5,
        "WMAP7": acosmo.WMAP7,
        "WMAP9": acosmo.WMAP9,
        "Planck13": acosmo.Planck13,
        "Planck15": acosmo.Planck15,
        "Planck18": acosmo.Planck18,
    }

    # If the user uses a string for the cosmology look it up in the dict.
    # If they specify a cosmology class, use that instead.
    from astropy.cosmology import FLRW

    if isinstance(cosmology, str):
        if cosmology in available_cosmologies.keys():
            cosmo = available_cosmologies[cosmology]
        else:
            msg = (f"""The cosmology '{cosmology}' is not in the list of
            available cosmologies with string keywords. The list
            if available cosmologies accessable via keyword are:
            {available_cosmologies.keys()}""")
            raise ValueError(msg)

    elif isinstance(cosmology, FLRW):
        cosmo = cosmology

    return cosmo


def z_to_cMpc(redshift, cosmology='Planck18'):
    """
    Convert a redshift into a comoving distance with units of Mpc.

    Parameters
    ----------
    redshift : array-like, shape (N, )
        The redshift values. Must be 1D or scalar.
    cosmology : string or astropy.cosmology.core.FLRW
        The cosmology used to calculate distance. This can either be a
        string of the cosmology keyword used in astropy (e.g 'Planck13'
        or 'WMAP7') or an instance of an astropy.cosmology.
        Default: 'Planck18'

    Returns
    -------
    distance : astropy.unit.quantity.Quantity
        The distance to a redshift in comoving Mpc.

    Examples
    --------
    >>> cosmology.z_to_cMpc(2)
    <Quantity 5308.18888389 Mpc>

    >>> cosmology.z_to_cMpc(2, cosmology="WMAP7")
    <Quantity 5279.26488146 Mpc>

    >>> import astropy.cosmology as acosmo
    >>> P13 = acosmo.Planck13
    >>> cosmology.z_to_cMpc(2, cosmology=Planck13)
    <Quantity 5310.8891027 Mpc>

    >>> redshifts = np.array([0, 1, 2, 3])
    >>> cosmology.z_to_cMpc(redshifts)
    <Quantity [0.    , 3395.63447115, 5308.18888389, 6504.00398895] Mpc>

    """

    cosmo = get_cosmology_from_name(cosmology)
    distance = cosmo.comoving_distance(redshift)

    # If the redshift is really small the user likely wants the result
    # to be at 0.0 Mpc. 1e-4 Mpc is 100 pc.
    distance_zero_threshold = 1e-4 * apu.Mpc
    distance[distance < distance_zero_threshold] = 0
    return distance


def cMpc_to_z(cMpc, cosmology="Planck18"):
    """
    Convert a comoving distance with units Mpc into a redshift.

    Parameters
    ----------
    cMpc : array-like, shape (N, )
        The distance values. Must be 1D or scalar.
    cosmology : string or astropy.cosmology.core.FLRW
        The cosmology used to calculate distance. This can either be a
        string of the cosmology keyword used in astropy (e.g 'Planck13'
        or 'WMAP7') or an instance of an astropy.cosmology.
        Default: 'Planck15'

    Returns
    -------
    redshift : astropy.unit.Quantity
        The redshift to the distance.

    Examples
    --------
    >>> cosmology.cMpc_to_z(200)
    <Quantity 0.51602537 redshift>

    >>> cosmology.cMpc_to_z(200, cosmology="WMAP7")
    <Quantity 0.5314927 redshift>

    >>> import astropy.cosmology as acosmo
    >>> P13 = acosmo.Planck13
    >>> cosmology.cMpc_to_z(2000, cosmology=Planck13)
    <Quantity 0.51646246 redshift>

    >>> distances = np.array([0, 1000, 2000, 3000])
    >>> cosmology.z_to_cMpc(distances)
    <Quantity [0.  , 0.23952583, 0.51602537, 0.84787111] redshift>

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

    return redshift * acu.redshift


def scale_factor(redshift):
    """
    Calculates the scale factor, a, at a given redshift.

    a = (1 + z)**-1

    Parameters
    ----------
    redshift : array-like
        The redshift values.

    Returns
    -------
    a : array-like
        The scale factor at the given redshift.

    Examples
    --------
    >>> cosmology.scale_factor(1)
    0.5

    >>> cosmology.scale_factor(np.array([0, 1, 2, 3]))
    array([1, 0.5, 0.3333333, 0.25])

    """
    return (1 + redshift)**-1.0
