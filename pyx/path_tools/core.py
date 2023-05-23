import os

from glob import glob


def get_paths_with_suffix(loc=".", suffix=None):
    """
    Glob all the files in a directory with a suffix and return an
    ordered list

    Parameters
    ----------
    loc: str, optional
        The path to the directory containing the files.
        Default: "."

    suffix: str, or None
        If suffix is a st

    Returns
    -------

    """
    
    if suffix is None:
        paths = glob(loc)
    elif isinstance(suffix, str):
        suffix = "".join(["*", suffix])
        paths = glob(os.path.join(loc, suffix))
    else:
        msg = ("suffix must have type None or str")
        raise TypeError(msg)

    return sorted(paths)

def get_paths_with_prefix(loc=".", prefix=None):
    """
    Glob all the files in a directory with a prefix and return an 
    ordered list.

    Parameters
    ----------

    Returns
    -------

    """
    pass
