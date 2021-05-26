"""
Printing
========
Provides a collection of useful printing related fuctions.

"""

def make_vprint(verbose=True):
    """
    Make a togglable print function.

    If verbose is true, make_vprint will return the print function. If 
    false, then make_vprint will return a function that does nothing.

    Examples
    --------
    >>> vprint = make_vprint(verbose=True)
    >>> vprint("Example Text")
    "Example Text"

    >>> vprint = make_vprint()
    >>> vprint("Example Text")
    "Example Text"

    >>> vprint = make_vprint(verbose=False)
    >>> vprint("Example Text")

    """

    if verbose:
        return print
    else:
        return _do_nothing

def _do_nothing(*args, **kwargs):
    """This function literally does nothing."""
    pass
