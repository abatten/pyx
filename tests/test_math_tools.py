from pyx.math_tools import cosmology as pyxcosmo
import astropy.units as apu
import numpy as np

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

def test_z_to_cMpc_zero():
    # Zero distance should give zero redshift
    z = 0.0
    assert pyxcosmo.cMpc_to_z(0) == z

def test_z_to_cMpc_array():
    # Must return an array
    z = np.array([0.0, 0.8479314667609102])
    assert (pyxcosmo.z_to_cMpc(np.array([0.0, 3000])).value == z).all


