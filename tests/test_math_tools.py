from pyx.math_tools import cosmology as pyxcosmo
import astropy.units as apu
import astropy.cosmology as acosmo
import numpy as np
import pytest

def test_z_to_cMpc_float():
    dist = 3395.905416665515
    assert pyxcosmo.z_to_cMpc(1).value == dist

def test_z_to_cMpc_zero():
    # Zero redshift should give zero distance
    dist = 0.0
    assert pyxcosmo.z_to_cMpc(0).value == dist

def test_z_to_cMpc_array():
    # Must return an array
    dist = np.array([0.0, 3395.905416665515])
    assert (pyxcosmo.z_to_cMpc(np.array([0, 1])).value == dist).all

def test_cMpc_to_z_float():
    z = 0.8479314667609102
    assert pyxcosmo.cMpc_to_z(3000) == z

def test_cMpc_to_z_zero():
    # Zero distance should give zero redshift
    z = 0.0
    assert pyxcosmo.cMpc_to_z(0) == z

def test_cMpc_to_z_array():
    # Must return an array
    z = np.array([0.0, 0.8479314667609102])
    assert (pyxcosmo.cMpc_to_z(np.array([0.0, 3000])) == z).all

def test_cMpc_to_z_with_units():
    # Zero distance should give zero redshift
    z = 0.8479314667609102
    assert pyxcosmo.cMpc_to_z(3000 * apu.Mpc) == z

def test_get_cosmology_from_name():
    P13 = acosmo.Planck13
    assert pyxcosmo.get_cosmology_from_name("Planck13") == P13

def test_get_cosmology_from_name_invalid_entry():
    with pytest.raises(ValueError):
        pyxcosmo.get_cosmology_from_name("NOTPLANCK2020")

def test_get_cosmology_from_name_pass_cosmo():
    P13 = acosmo.Planck13
    assert pyxcosmo.get_cosmology_from_name(P13) == P13

def test_scale_factor_scalar():
    z = 1
    expected_scale_factor = 0.5
    assert pyxcosmo.scale_factor(z) == expected_scale_factor

def test_scale_factor_array():
    z = np.array([0, 1, 3])
    expected_scale_factor = np.array([1, 0.5, 0.25])
    assert (pyxcosmo.scale_factor(z) == expected_scale_factor).all

def test_physical_to_comoving_single():
    redshift = 1
    physical_distance = 50 * apu.Mpc
    expected_comoving_distance = 100 * apu.Mpc
    assert pyxcosmo.physical_to_comoving(physical_distance, redshift) == expected_comoving_distance

#def test_physical_to_comoving_array():

def test_comoving_to_physical_single():
    redshift = 1
    comoving_distance = 100 * apu.Mpc
    expected_physical_distance = 50 * apu.Mpc
    assert pyxcosmo.comoving_to_physical(comoving_distance, redshift) == expected_physical_distance

#def test_comoving_to_physical_array():
