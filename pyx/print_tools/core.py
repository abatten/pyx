import numpy as np

def vprint(*args, verbose=True, **kwargs):
    """
    Behaves exactly the same as the regular print function except
    with the additional 'verbose' keyword.

    Setting `verbose = False` will skip the print statement entirely.

    """
    if verbose:
        print(*args, **kwargs)

