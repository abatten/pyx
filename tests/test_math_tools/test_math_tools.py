import pyx.math_tools
from pyx.math_tools import cosmology as pyxcosmo
import astropy.units as apu
import astropy.cosmology as acosmo
import numpy as np
import pytest


def test_z_to_cMpc_float():
    """
    Test comoving distance is calculated from redshift to match astropy

    """
    redshift = 1.0
    expected_distance = 3395.905416665515  # Calculated from astropy
    calculated_distance = pyxcosmo.z_to_cMpc(redshift).value
    # Since expected distance is a float, no not test for exact equality
    assert np.isclose(expected_distance, calculated_distance)


def test_z_to_cMpc_redshift_zero():
    """
    Test 0 Mpc is returned when given 0 redshift

    """
    redshift = 0.0
    expected_distance = 0.0
    calculated_distance = pyxcosmo.z_to_cMpc(redshift).value
    assert np.isclose(expected_distance, calculated_distance)


def test_z_to_cMpc_redshift_array():
    """
    Test using a redshift array returns an array of distances

    """
    redshift_array = np.array([0.0, 1.0])

    # Must return an array
    expected_distance_array = np.array([0.0, 3395.905416665515])
    calculated_distance_array = pyxcosmo.z_to_cMpc(redshift_array).value

    assert np.isclose(expected_distance_array, calculated_distance_array).all


def test_cMpc_to_z_float():
    """
    Test redshift is calculated from cMpc with dtype = float

    """
    comoving_distance = 3000
    expected_redshift = 0.8479314667609102  # Calculated from astropy
    calculated_redshift = pyxcosmo.cMpc_to_z(comoving_distance)
    assert np.isclose(expected_redshift, calculated_redshift)


def test_cMpc_to_z_zero():
    """
    Test zero comoving distance should return zero redshift

    """
    # Zero distance should give zero redshift
    comoving_distance = 0.0
    expected_redshift = 0.0
    calculated_redshift = pyxcosmo.cMpc_to_z(comoving_distance)
    assert np.isclose(expected_redshift, calculated_redshift)


def test_cMpc_to_z_array():
    """
    Test passing a comoving distance array returns a redshift array

    """
    comoving_distance_array = np.array([0.0, 3000])
    # Must return an array
    expected_redshift_array = np.array([0.0, 0.8479314667609102])
    calculated_redshift_array = pyxcosmo.cMpc_to_z(comoving_distance_array)
    assert np.isclose(expected_redshift_array, calculated_redshift_array).all


def test_cMpc_to_z_with_units():
    """
    Test that passsing comoving distance with units calculated redshift
    correctly.

    """
    comoving_distance_units = 3000 * apu.Mpc
    expected_redshift = 0.8479314667609102
    calculated_redshift = pyxcosmo.cMpc_to_z(comoving_distance_units)
    assert np.isclose(expected_redshift, calculated_redshift)


def test_get_cosmology_from_name():
    """

    """

    P13 = acosmo.Planck13
    assert pyxcosmo.get_cosmology_from_name("Planck13") == P13


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
    P13 = acosmo.Planck13
    assert pyxcosmo.get_cosmology_from_name(P13) == P13


def test_scale_factor_scalar():
    """
    Test that scale factor is correctly calculated from redshif).allt

    """
    redshift = 1.0
    expected_scale_factor = 0.5
    calculated_scale_factor = pyxcosmo.scale_factor(redshift)
    assert np.isclose(calculated_scale_factor, expected_scale_factor)


def test_scale_factor_array():
    z = np.array([0, 1, 3])
    expected_scale_factor = np.array([1, 0.5, 0.25])
    assert (pyxcosmo.scale_factor(z) == expected_scale_factor).all


def test_physical_to_comoving_single():
    """
    Test converting physical distance to comoving distance at a redshift

    """
    redshift = 1.0
    physical_distance = 50 * apu.Mpc
    expected_comoving_distance = 100 * apu.Mpc
    calculated_comoving_distance = \
            pyxcosmo.physical_to_comoving(physical_distance, redshift)
    assert np.isclose(calculated_comoving_distance.value,
                      expected_comoving_distance.value)

# def test_physical_to_comoving_array():


def test_comoving_to_physical_single():
    redshift = 1
    comoving_distance = 100 * apu.Mpc
    expected_physical_distance = 50 * apu.Mpc
    assert pyxcosmo.comoving_to_physical(comoving_distance, redshift) == expected_physical_distance

# def test_comoving_to_physical_array():


def test_reshape_to_1D_1D_array():
    """
    Test that reshaping a 1D array still returns a 1D array

    """
    test_array = np.array([1, 2, 3, 4, 5])
    reshaped_array = pyx.math_tools.reshape_to_1D(test_array)
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
    reshaped_array = pyx.math_tools.reshape_to_1D(test_array)

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

    reshaped_array = pyx.math_tools.reshape_to_1D(test_array)

    assert np.allclose(expected_output_array, reshaped_array)

def test_mean_median_mode():

    sample_array = np.array([1, 2, 3, 3, 3, 3, 4, 4, 5, 5, 6, 6])

    expected_mean = 3.75
    expected_median = 3.5
    expected_mode = 3
    expected_mean_median_mode = np.array([expected_mean,
                                          expected_median,
                                          expected_mode])
    calc_mean, calc_median, calc_mode = \
            pyx.math_tools.mean_median_mode(sample_array)
    calculated_mean_median_mode = np.array([calc_mean, 
                                            calc_median,
                                            calc_mode])

    assert np.allclose(expected_mean_median_mode, calculated_mean_median_mode)


