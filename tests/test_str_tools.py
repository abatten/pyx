from pyx import str_tools

def test_float2str_int():
    assert str_tools.float2str(23) == '23'

def test_float2str_float():
    assert str_tools.float2str(23.5) == '23.5'

def test_float2str_float_separator():
    assert str_tools.float2str(23.5, separator="p") == '23p5'

def test_float2str_float_precision_lower():
    assert str_tools.float2str(23.5, precision=4) == '23.5000'

def test_float2str_float_precision_higher():
    assert str_tools.float2str(23.501345, precision=4) == '23.5013'

def test_float2str_float_precision_zero():
    assert str_tools.float2str(23.5, precision=0) == '24'

def test_float2str_prefix_separator():
    assert str_tools.float2str(23.5, prefix='z', separator='p') == 'z23p5'

def test_float2str_prefix_suffix_separator():
    assert str_tools.float2str(23.5, prefix='z', separator='p', suffix='dex') == 'z23p5dex'


