import numpy as np

def interpolateArrays(sample, xvals, fvals, kind='linear'):

    array = []

    if kind == 'linear':


    elif kind == 'cubic':
        msg = f"{kind} interpolation has not been implemented yet"
        raise NotImplementedError(msg)

    

    return array
