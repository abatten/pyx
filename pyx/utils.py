"""
UTILS
-----
A collection of various functions that do not fit elsewhere.

"""

__all__ = [
    'files_with_stem',
    'files_with_suffix',
    'files_with_prefix',
    'float2str', 
    'get_rng_from_seed',
    'str2float'
    'vprint'
    ]

import os
import numpy as np
from glob import glob


def files_with_stem(loc=".", prefix=None, suffix=None):
    """
    Glob all the files in a directory with a word stem 
    (either prefix and/or suffix) and return an ordered list.

    Parameters
    ----------
    loc : str, optional
        The path to the directory containing the files.
        Default: "."
    prefix : str, or None, optional
        The prefix of the files to find. If None,
        this will return all the files in the directory
        regardless of prefix        
    suffix : str, or None, optional
        The suffix of the files to find. If None,
        this will return all the files in the directory
        regardless of suffix.

    Returns
    -------
    paths : list
        A list of paths to all files in a directory.

    """
    if suffix is None and prefix is None:
        paths = glob(loc)
    elif isinstance(suffix, str) and isinstance(prefix, str):
        stem = "".join([prefix, "*", suffix])
    elif isinstance(suffix, str) and prefix is None:
        stem = "".join(["*", suffix])
    elif suffix is None and isinstance(prefix, str):
        stem = "".join([prefix, "*"])
    else:
        msg = ("Suffix and Prefix both must have type None or str")
        raise TypeError(msg)

    paths = glob(os.path.join(loc, stem))
    return sorted(paths)


def files_with_suffix(loc=".", suffix=None):
    """
    Glob all the files in a directory with a suffix and return an
    ordered list.

    Parameters
    ----------
    loc : str, optional
        The path to the directory containing the files.
        Default: "."
    suffix : str, or None, optional
        The suffix of the files to find. If None,
        this will return all the files in the directory.

    Returns
    -------
    paths : list
        A list of paths to all files in a directory.
    """
    return files_with_stem(loc=loc, suffix=suffix)


def files_with_prefix(loc=".", prefix=None):
    """
    Glob all the files in a directory with a prefix and return an
    ordered list.

    Parameters
    ----------
    loc : str, optional
        The path to the directory containing the files.
        Default: "."
    prefix : str, or None, optional
        The prefix of the files to find. If None,
        this will return all the files in the directory.

    Returns
    -------
    paths : list
        A list of paths to all files in a directory with the prefix.

    """
    return files_with_stem(loc=loc, prefix=prefix)


def float2str(flt, separator=".", precision=None, prefix=None, suffix=None):
    """
    Converts a floating point number into a string.

    Contains numberous options on how the output string should be
    returned including prefixes, suffixes, floating point precision,
    and alternative decimal separators. 

    Parameters
    ----------
    flt : float
        The floating point number
    separator : str
        The symbol that will replace the decimal point in the float.
        Default: "."
    precision : int or None
        The number of decimal places of the float to use in the string.
        Default: None
    prefix : string or None
        Characters that are to appear at the beginning of the output.
        Default: None
    suffix : string or None
        Characters that are to appear at the end of the output.
        Default: None

    Returns
    -------
    string : str
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


def str2float(string, separator="p", prefix=None, suffix=None):
    """
    Converts a string into a floating point number.

    Converts a string that has an encoded floating point number
    into a float by removing prefixes, suffixes and replacing
    the separator.

    Parameters
    ----------
    string : str
        The string containing the endoded float.
    separator : string
        The symbol that had replaced the decimal point in the float.
        Default: "p"
    prefix : string or None
        Characters that appear at the beginning of the string.
        Default: None
    suffix : string or None
        Characters that appear at the end of the string.
        Default: None

    Returns
    -------
    flt : float
        A float extracted from the string representation.

    Examples:
    ---------
    >>> str2float('23p0')
    23.0
    >>> str2float('23p5')
    23.5
    >>> str2float('23_523', separator='_')
    23.523
    >>> str2float('z23p533dex', prefix='z', suffix='dex')
    23.533
    >>> str2float('z23$51dex', prefix='z', separator='$', suffix='dex')
    23.51

    """
    if prefix is not None:
        string = string.removeprefix(prefix)
    if suffix is not None: 
        string = string.removesuffix(suffix)
    if separator is not None:
        values = string.split(separator)

    # This line is a little funky but its a clever way to recombine
    # the two sides of the decimal.
    # e.g [25, 555] = 25 + 555/(10**3)
    if len(values) > 1:
        flt = int(values[0]) + int(values[1])/(10**len(values[1]))
    else:
        flt = int(values[0])
    return flt



def get_rng_from_seed(seed):
    """
    Parameters
    ----------
    seed : None or int
        The random seed that will be used to generate the numpy
        default_rng(). If None, a random seed will be used.
        Default: None

    Returns
    -------
    rng : np.random.default_rng

    """
    if seed is None:
        rng = np.random.default_rng()
    elif isinstance(seed, int):
        rng = np.random.default_rng(seed=seed)
    else:
        raise ValueError("Seed must be of type int")
    return rng  


def vprint(*args, verbose=True, **kwargs):
    """
    Behaves exactly the same as the regular print function except
    with the additional 'verbose' keyword.

    Setting `verbose = False` will skip the print statement entirely.

    """
    if verbose:
        print(*args, **kwargs)
