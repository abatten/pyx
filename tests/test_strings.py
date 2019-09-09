from pyx import strings

def test_float2str_int():
    assert strings.float2str(23) == '23'

def test_float2str_float():
    assert strings.float2str(23.5) == '23.5'

def test_float2str_float_separator():
    assert strings.float2str(23.5, separator="p") == '23p5'

def test_float2str_float_precision_lower():
    assert strings.float2str(23.5, precision=4) == '23.5000'

def test_float2str_float_precision_higher():
    assert strings.float2str(23.501345, precision=4) == '23.5013'

def test_float2str_float_precision_zero():
    assert strings.float2str(23.5, precision=0) == '24'

def test_float2str_prefix_separator():
    assert strings.float2str(23.5, prefix='z', separator='p') == 'z23p5'

def test_float2str_prefix_suffix_separator():
    assert strings.float2str(23.5, prefix='z', separator='p', suffix='dex') == 'z23p5dex'


