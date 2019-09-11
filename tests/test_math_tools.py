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
