import numpy as np
import pytest

import astropy.units as apu
import astropy.cosmology as acosmo

from pyx import cosmology as pyxcosmo


def test_get_cosmology_from_name():
    """
    Test that all cosmologies are load correctly from name.
    """
    W5 = acosmo.WMAP5
    W7 = acosmo.WMAP7
    W9 = acosmo.WMAP9
    P13 = acosmo.Planck13
    P15 = acosmo.Planck15
    P18 = acosmo.Planck18
    assert pyxcosmo.get_cosmology_from_name("WMAP5") == W5
    assert pyxcosmo.get_cosmology_from_name("WMAP7") == W7
    assert pyxcosmo.get_cosmology_from_name("WMAP9") == W9
    assert pyxcosmo.get_cosmology_from_name("Planck13") == P13
    assert pyxcosmo.get_cosmology_from_name("Planck15") == P15
    assert pyxcosmo.get_cosmology_from_name("Planck18") == P18


def test_get_cosmology_from_name_invalid_entry():
    """
    Test that passing an invalid string will return a ValueError
    """
    with pytest.raises(ValueError):
        pyxcosmo.get_cosmology_from_name("NOTPLANCK2020")


def test_get_cosmology_from_name_pass_cosmo():
    """
    Test that passing an astropy.cosmology will return that same
    cosmology.

    """
    W5 = acosmo.WMAP5
    W7 = acosmo.WMAP7
    W9 = acosmo.WMAP9
    P13 = acosmo.Planck13
    P15 = acosmo.Planck15
    P18 = acosmo.Planck18
    assert pyxcosmo.get_cosmology_from_name(W5) == W5
    assert pyxcosmo.get_cosmology_from_name(W7) == W7
    assert pyxcosmo.get_cosmology_from_name(W9) == W9
    assert pyxcosmo.get_cosmology_from_name(P13) == P13
    assert pyxcosmo.get_cosmology_from_name(P15) == P15
    assert pyxcosmo.get_cosmology_from_name(P18) == P18


def test_z_to_cMpc_check_float_and_int_works():
    """
    Test comoving distance is calculated from redshift to match astropy

    """
    redshift_int = 1
    redshift_float = 1.0
    expected_distance = 3395.905416665515  # Calculated from astropy
    calculated_distance_float = pyxcosmo.z_to_cMpc(redshift_float, cosmology='Planck15').value
    calculated_distance_int = pyxcosmo.z_to_cMpc(redshift_int, cosmology='Planck15').value
    # Since expected distance is a float, no not test for exact equality
    assert np.isclose(expected_distance, calculated_distance_float)
    assert np.isclose(expected_distance, calculated_distance_int)


def test_z_to_cMpc_redshift_zero():
    """
    Test 0 Mpc is returned when given 0 redshift

    """
    redshift = 0.0
    expected_distance = 0.0
    calculated_distance = pyxcosmo.z_to_cMpc(redshift, cosmology='Planck15').value
    assert np.isclose(expected_distance, calculated_distance)


def test_z_to_cMpc_redshift_array():
    """
    Test using a redshift array returns an array of distances

    """
    redshift_array = np.array([0.0, 1.0])

    # Must return an array
    expected_distance_array = np.array([0.0, 3395.905416665515])
    calculated_distance_array = pyxcosmo.z_to_cMpc(redshift_array, cosmology='Planck15').value
    assert np.isclose(expected_distance_array, calculated_distance_array).all


def test_cMpc_to_z_check_float_and_int_works():
    """
    Test redshift is calculated from cMpc with dtype = float

    """

    comoving_distance_int = 3000
    comoving_distance_float = 3000.0
    expected_redshift = 0.8479314667609102  # Calculated from astropy
    calculated_redshift_int = pyxcosmo.cMpc_to_z(comoving_distance_int, cosmology='Planck15')
    calculated_redshift_float = pyxcosmo.cMpc_to_z(comoving_distance_float, cosmology='Planck15')
    assert np.isclose(expected_redshift, calculated_redshift_float)
    assert np.isclose(expected_redshift, calculated_redshift_int)


def test_cMpc_to_z_zero():
    """
    Test zero comoving distance should return zero redshift

    """
    # Zero distance should give zero redshift
    comoving_distance = 0.0
    expected_redshift = 0.0
    calculated_redshift = pyxcosmo.cMpc_to_z(comoving_distance, cosmology='Planck15')
    assert np.isclose(expected_redshift, calculated_redshift)


def test_cMpc_to_z_array():
    """
    Test passing a comoving distance array returns a redshift array

    """
    comoving_distance_array = np.array([0.0, 3000])
    # Must return an array
    expected_redshift_array = np.array([0.0, 0.8479314667609102])
    calculated_redshift_array = pyxcosmo.cMpc_to_z(comoving_distance_array, cosmology='Planck15')
    assert np.isclose(expected_redshift_array, calculated_redshift_array).all


def test_cMpc_to_z_with_units():
    """
    Test that passsing comoving distance with units calculated redshift
    correctly.

    """
    comoving_distance_units = 3000 * apu.Mpc
    expected_redshift = 0.8479314667609102
    calculated_redshift = pyxcosmo.cMpc_to_z(comoving_distance_units, cosmology='Planck15')
    assert np.isclose(expected_redshift, calculated_redshift)

def test_scale_factor_check_float_and_int_works():
    """
    Test that the scale factor function works with floats and ints
    """
    redshift_int = 1
    redshift_float = 1.0
    true_a = 0.5
    scale_factor_int = pyxcosmo.scale_factor(redshift_int)
    scale_factor_float = pyxcosmo.scale_factor(redshift_float)
    assert true_a == scale_factor_float
    assert true_a == scale_factor_int


def test_scale_factor_with_arrays():
    """
    Test that the scale factor function works with floats and ints
    """
    redshift = np.array([0, 1, 2, 3])
    true_a_array = np.array([1, 1/2, 1/3, 1/4])
    scale_factors = pyxcosmo.scale_factor(redshift)

    assert np.isclose(true_a_array, scale_factors).all()

