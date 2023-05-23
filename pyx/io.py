import numpy as np

def write_row(output, data, col_width=16, decimals=4):
    """
    A wrapper around the write function to automate spacing when 
    writing rows of columned data to file.  

    Parameters
    ----------
    output: TextIOWrapper
        An open file with write permissions.

    data: list or 1D np.ndarray
        The data that will be written to output. Each item will be
        written to a new column of the output. 

    Optional
    --------
    col_width: int, optional
        The width of the columns in number of characters. 
        Default: 16
    
    decimals: int, optional
        The decimal point precision for floating point and integers.
        Default: 4

    """

    row = f""

    if isinstance(data, list):
        data = np.array(data)
   

    if data.dtype.type in (np.str_,):
        for item in data:
            row = f"{row}{item:<{col_width}}"

    else:
        for item in data:
            row = f"{row}{item:<{col_width}.{decimals}f}"

    output.write(f"{row}\n")
