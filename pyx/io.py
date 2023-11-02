"""
IO
--
A collection of various functions for dealing with input and outputs.

"""

__all__ = [
    'dict_to_hdf5_attributes', 
    'dict_to_hdf5_group'
    'load_yaml', 
    'write_row',
    ]


try:
    import h5py
    import_h5py = True
except ImportError:
    import_h5py = False

import numpy as np
import yaml


def dict_to_hdf5_attributes(item, attrs_dict):
    """
    Adds attributes from a dictionary to a HDF5 dataset or group. 
    The attributes will be automatically sorted into alphabetical
    order.

    Parameters
    ----------
    item: A dataset or group from an open HDF5 file (h5py._hl.files.File)
        The dataset or group to attach the attributes.

    attrs_dict: dict
        The attributes of the data set or group. The key is the name 
        of the attribute.

    """
    if not import_h5py:
        raise ImportError("This function requires h5py!")
    else:
        if not isinstance(attrs_dict, dict):  # Must be a dict!
            raise TypeError("attrs_dict must be a dictionary") 

        # Sort into alphabetical order
        attributes = sorted(attrs_dict.items())
        for key, value in attributes:
            item.attrs[key] = value


def dict_to_hdf5_group(hdf5_file, attrs_dict, group_name):
    """
    Creates a new group in a hdf5 file and writes a dictionary as
    attributes of that group.

    Parameters
    ----------
    hdf5_file: An open HDF5 file (h5py._hl.files.File)
        The open HDF5 file to add the new group into

    attrs_dict: dict
        The attributes of the new group.

    group_name: str
        The name of the new group.

    """
    if not import_h5py:
        raise ImportError("This function requires h5py!")
    else:
        hdf5_file.create_group(group_name)
        group = hdf5_file[group_name]
        dict_to_hdf5_attributes(group, attrs_dict)


def load_yaml(path):
    """
    Loads data from a YAML configuration file.

    Given an a path to a YAML file, returns a dictionary
    containing all of the data contained in the file.

    Parameters
    ----------
    path : str
        The path to a YAML file..

    Returns
    -------
    dict:
        A dictionary containing all the data in the YAML.

    """
    with open(path, 'r') as file_object:
        data = yaml.safe_load(file_object)
        return data


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
