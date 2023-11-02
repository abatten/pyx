"""
UTILS
-----
A collection of various functions that do not fit elsewhere.

"""

__all__ = ['float2str', 'get_rng_from_seed', 'vprint']

import numpy as np

def get_rng_from_seed(seed):
    """
    Parameters
    ----------
    seed: None or int
        The random seed that will be used to generate the numpy
        default_rng(). If None, a random seed will be used.
        Default: None

    Returns
    -------
    rng: np.random.default_rng

    """
    if seed is None:
        rng = np.random.default_rng()
    elif isinstance(seed, int):
        rng = np.random.default_rng(seed=seed)
    else:
        raise ValueError("Seed must be of type int")
    return rng  


def float2str(flt, separator=".", precision=None, prefix=None, suffix=None):
    """
    Converts a floating point number into a string.

    Contains numberous options on how the output string should be
    returned including prefixes, suffixes, floating point precision,
    and alternative decimal separators. 

    Parameters
    ----------
    flt: float
        The floating point number
    
    separator: string
        The symbol that will replace the decimal point in the float.
        Default: "."

    precision: int or None
        The number of decimal places of the float to use in the string.
        Default: None

    prefix: string or None
        Characters that are to appear at the beginning of the output.
        Default: None

    suffix: string or None
        Characters that are to appear at the end of the output.
        Default: None

    Returns
    -------
    string: str
        A string representation of the floating point number.

    Examples:
    ---------
    >>> float2str(23)
    '23'
    >>> float2str(23.5)
    '23.5'
    >>> float2str(23.5, separator="p")
    '23p5'
    >>> float2str(23.5, precision=4)
    '23.5000'
    >>> float2str(23.501345, precision=4)
    '23.5013'
    >>> float2str(23.5, precision=0)
    '24'
    >>> float2str(23.5, prefix='z', separator='p')
    'z23p5'
    >>> float2str(23.5, prefix 'z', separator='p', suffix='dex')
    'z23p5dex'

    """
    
    if isinstance(precision, int):
        str_number = f"{flt:.{precision}f}"
    else:
        str_number = str(flt)

    if separator!=".":
        # Split number around the decimal point. 
        number_parts = str_number.split(".")
        string = separator.join(number_parts)
    else:
        string = str_number

    if isinstance(prefix, str):
        string = "".join([prefix, string])

    if isinstance(suffix, str):
        string = "".join([string, suffix])

    return string


def vprint(*args, verbose=True, **kwargs):
    """
    Behaves exactly the same as the regular print function except
    with the additional 'verbose' keyword.

    Setting `verbose = False` will skip the print statement entirely.

    """
    if verbose:
        print(*args, **kwargs)