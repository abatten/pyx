import re

class Params(dict):
    """
    A dictionary designed for parameters.
    """

    #validate = {key: converter
    #            for key, (default, converter) in defaultParams.items()
    #            if key not in _all_deprecated}

    def __init__(self, *args, **kwargs):
        self.update(*args, **kwargs)

    def __str__(self):
        return '\n'.join(map('{0[0]}: {0[1]}'.format, sorted(self.items())))

    def __setitem__(self, key, val):
        try:
            #try:
            #    cval = self.validate[key](val)
            #except ValueError as ve:
            #    raise ValueError("Key %s: %s" % (key, str(ve)))
            dict.__setitem__(self, key, val)
        except KeyError:
            raise KeyError(
                f"{key} is not a valid parameter (see rcParams.keys() for "
                f"a list of valid parameters)")


    def find_all(self, pattern):
        """
        Return the subset of this Params dictionary whose keys match,
        using :func:`re.search`, the given ``pattern``.

        .. note::

        Changes to the returned dictionary are *not* propagated to
        the parent Params dictionary.

        """
        pattern_re = re.compile(pattern)
        return Params((key, value)
                        for key, value in self.items()
                        if pattern_re.search(key))


    def copy(self):
        return {k: dict.__getitem__(self, k) for k in self}




