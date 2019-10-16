"""
Dictconfig
==========
A wrapper for configparser to help create dictionaries from parameter files.

"""

import os
import json
import configparser as cp


def _isfloat(string):
    """
    Checks if a string can be converted into a float.

    Parameters
    ----------
    value : str

    Returns
    -------
    bool:
        True/False if the string can/can not be converted into a float.

    """
    try:
        float(string)
        return True

    except ValueError:
        return False


def _isint(string):
    """
    Checks if a string can be converted into an int.

    Parameters
    ----------
    value : str

    Returns
    -------
    bool:
        True/False if the string can/can not be converted into an int.

    """
    try:
        int(string)
        return True

    except ValueError:
        return False


def _isbool(string):
    """
    Checks if a string can be converted into a boolean.

    Parameters
    ----------
    value : str

    Returns
    -------
    bool:
        True/False if the string can/can not be converted into a boolean.

    """
    return string in ("True", "true", "False", "false")


def _islist(string):
    """
    Checks if a string can be converted into a list.

    Parameters
    ----------
    value : str

    Returns
    -------
    bool:
        True/False if the string can/can not be converted into a list.

    """
    return (list(string)[0] == "[") and (list(string)[-1] == "]")


def get_option(option, value, section, config):
    """
    Get an option value from a given section

    Parameters
    ----------
    option: str

    value: str

    section: str

    config: configparser.ConfigParser

    Returns
    -------
    param: int, float, list or bool
        The
    """
    if _isint(value):
        param = config.getint(section, option)

    elif _isfloat(value):
        param = config.getfloat(section, option)

    elif _isbool(value):
        param = config.getboolean(section, option)

    elif _islist(value):
        param = json.loads(config.get(section, option))

    else:
        param = config.get(section, option)

    return param



def _check_sections_exist(section, config):
    """

    Parameters
    ----------
    section: str or list or "All"
        The section name or list of section names to read from the
        parameter file. Default: "All"

    config:


    Returns
    -------
    section: list
        A list containing all the sections requested. If 'All' is specified
        then all the sections listen in the parameter file will be returned.
        If a single string is passed, the it will be converted to a single item
        list.

    """

    # If the sections are given as a list check that each name is valid.
    if isinstance(section, list):
        for section_name in section:
            if not config.has_section(section_name):
                msg = (f"'{section_name}' is not a section in the "
                "parameter file")
                raise ValueError(msg)

    # If 'All' sections are wanted get the list of sections in the param file
    elif isinstance(section, str):
        if section == "All":
            section = config.sections()

        else:
            if not config.has_section(section):
                msg = f"'{section}' is not a section in the parameter file"
                raise ValueError(msg)
            else:
                # Convert the single string into a list to enumerate later.
                section = [section]

    else:
        raise TypeError(f"Sections must be a string or a list of strings. "
                       "Instead section is type {type(section)}")

    return section

def read(path, section="All"):
    """
    Reads 

    Parameters
    ----------
    path : str
        The path to a parameter file that can be read using config parser.

    section : str or list or "All"
        The section name or list of section names to read from the
        parameter file. Default: "All"

    Returns
    -------
    params : dict
        A dictionary containing the parameters and values from the file.

    """
    
    if not os.path.exists(path):
        raise OSError(f"Could not find parameter file: {path}")

    params = {}

    config = cp.ConfigParser()
    config.read(path)

    section = _check_sections_exist(section, config)

    for name in section:
        for key, value in zip(config[name].keys(), config[name].values()):
            params[key] = get_option(key, value, name, config)
            
    return params
