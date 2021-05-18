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

    if separator is not  ".":
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

