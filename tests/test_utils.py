import numpy as np
import pytest

from pyx import utils as pyxutils

def test_float2str_int():
    assert pyxutils.float2str(23) == '23'

def test_float2str_float():
    assert pyxutils.float2str(23.5) == '23.5'

def test_float2str_float_separator():
    assert pyxutils.float2str(23.5, separator="p") == '23p5'

def test_float2str_float_precision_lower():
    assert pyxutils.float2str(23.5, precision=4) == '23.5000'

def test_float2str_float_precision_higher():
    assert pyxutils.float2str(23.501345, precision=4) == '23.5013'

def test_float2str_float_precision_zero():
    assert pyxutils.float2str(23.5, precision=0) == '24'

def test_float2str_prefix_separator():
    assert pyxutils.float2str(23.5, prefix='z', separator='p') == 'z23p5'

def test_float2str_prefix_suffix_separator():
    assert pyxutils.float2str(23.5, prefix='z', separator='p', suffix='dex') == 'z23p5dex'


def test_str2float_int():
    assert pyxutils.str2float('23') == 23

def test_str2float_float():
    assert pyxutils.str2float('23p5') == 23.5

def test_str2float_float_decimals():
    assert np.isclose(pyxutils.str2float('23p51234'), 23.51234)

def test_str2float_float_separator():
    assert pyxutils.str2float('23_5', separator="_") == 23.5

def test_float2str_prefix_separator():
    assert pyxutils.str2float('z23p5', prefix='z', separator='p') == 23.5

def test_float2str_prefix_suffix_separator():
    assert pyxutils.str2float('z23_5dex', prefix='z', separator='_', suffix='dex') == 23.5

def test_float2str_prefix_suffix_separator_decimals():
    assert np.isclose(pyxutils.str2float('z23_51234dex', prefix='z', separator='_', suffix='dex'), 23.51234)