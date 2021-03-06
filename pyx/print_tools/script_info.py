import os
import datetime
import __main__

from pyx import Params


def print_header(title=None, printParams='auto'):
    """
    Prints out a header containing information about file,
    file location, user, date and time.

    Parameters
    ----------
    title: string, optional
        The heading title. This will be capitalised in the print out.
        If *None*, it will use the name returned by __file__ instead.

    Example
    -------

    >>> scriptinfo.print_header()

    *********************************************
                    SCRIPTINFO.PY
    .............................................
    FILE  : decoprint.py
    PATH  : /Users/abatten/pyx/pyx/scriptinfo.py
    USER  : abatten
    DATE  : 2019-08-22
    TIME  : 15:20:12.114276
    *********************************************

    >>> scriptinfo.print_header("THIS IS A HEADER")

    *********************************************
                   THIS IS A HEADER
    .............................................
    FILE  : scriptinfo.py
    PATH  : /Users/abatten/pyx/pyx/scriptinfo.py
    USER  : abatten
    DATE  : 2019-08-22
    TIME  : 15:18:55.503771
    *********************************************
    """
    # __main__.file__ gets the filename of the script that is running.
    # Whereas __file__ is this file.
    filename = os.path.basename(__main__.__file__)

    if printParams == 'auto':
        printParams = printing_params()

    info = []
    info.append("\n")    
    info.append(printParams['section.line_major'])

    # If no title is provided, use the script name as a title.
    if title is None:
        title = filename.upper()

    if printParams['header.centre_title']:
        info.append(f"{title:^{printParams['section.width']}}")
    else:
        info.append(f"{title}")

    info.append(printParams['section.line_minor'])

    if printParams['header.print_file']:
        info.append(f"{'FILE':<6}: {filename}")

    if printParams['header.print_path']:
        info.append(f"{'PATH':<6}: {__main__.__file__}")

    if printParams['header.print_user']:
        username = os.getlogin()
        info.append(f"{'USER':<6}: {username}")
    
    now = datetime.datetime.now()

    if printParams['header.print_date']:
        info.append(f"{'DATE':<6}: {now.date()}")
    if printParams['header.print_time']:
        info.append(f"{'TIME':<6}: {now.time()}")
    
    info.append(printParams['section.line_major'])

    info.append("\n")

    info = '\n'.join(info)
    print(info)


def print_footer(title=None, printParams='auto'):
    """
    By default prints the date and time information.

    Example:

    >>> pyx.scriptinfo.print_footer()

    *********************************************
                    COMPLETED
    .............................................
    DATE  : 2019-08-22
    TIME  : 16:40:39.427011
    *********************************************

    """
    if printParams == 'auto':
        printParams = printing_params().copy()
        disable_header_lines = [
            'header.print_file',
            'header.print_path',
            'header.print_user',
        ]
        for item in disable_header_lines:
            printParams[item] = False
       
    if title is None:
        title = "COMPLETED"
    print_header(title=title, printParams=printParams)


def printing_params():
    pParams = Params()

    pParams["section.width"] = 45
    pParams["section.character_major"] = "*"
    pParams["section.line_major"] = (pParams["section.character_major"] * 
                                     pParams["section.width"])

    pParams["section.character_minor"] = "."
    pParams["section.line_minor"] = (pParams["section.character_minor"] * 
                                     pParams["section.width"])


    pParams['header.print_file'] = True
    pParams['header.print_path'] = True
    pParams['header.print_user'] = False
    pParams['header.print_date'] = True
    pParams['header.print_time'] = True
    pParams['header.centre_title'] = True
    return pParams


