"""
FIT
---
A collection of various functions for fitting data.

"""
import numpy as np

__all__ = [
    'fit_poly_least_squares',
    'fit_straight_line_least_squares',
    'calculate_poly_chisq',
]


def fit_poly_least_squares(xvals, yvals, yerr, order=1):
    """
    Fits a polynomial to data using the least squares method.

    Parameters
    ----------
    xvals : np.ndarray
        The x-coordinates of the N sample points.
    yvals : np.ndarray
        The y-coordinates of the N sample points.
    yerr : np.ndarray
        The y uncertainties of the N sample points.
    order : int, optional
        Order of the fitting polynomial.
        Default: 1
    
    Returns
    -------
    fit : np.ndarray
        The coefficients of the best fitting polynomial
        from the lowest order term to the highest.
    uncerts : np.ndarray
        The uncertaintys on the coefficients of the best fitting
        polynomial. Ordered from the lowest order term to the highest.
    chisq : float
        The chi squared value of the best fit.
    redchisq : float
        The reduced chi square value of the best fit.
        redchisq = chisq / (N - order - 1)

    """

    # Vandermonde matrix
    A = np.vander(xvals, order+1, increasing=True)

    # Matrix of Y Uncert
    C = np.diag(yerr * yerr)
    Cinv = np.linalg.inv(C)

    # See Hogg+2010 How to Fit a Model to Data, p.g. 4-5.
    AT_Cinv_A = A.T @ Cinv @ A
    AT_Cinv_Y = A.T @ Cinv @ yvals
    best_fit = np.linalg.inv(AT_Cinv_A) @ AT_Cinv_Y

    uncerts = np.sqrt(np.diag(np.linalg.inv(AT_Cinv_A)))
    chisq, redchisq = calculate_poly_chisq(best_fit, xvals, yvals, yerr, order=order)

    return best_fit, uncerts, chisq, redchisq


def fit_straight_line_least_squares(xvals, yvals, yerr):
    """
    Fits a straight line to data using the least squares method.

    Parameters
    ----------
    xvals : np.ndarray
        The x-coordinates of the N sample points.
    yvals : np.ndarray
        The y-coordinates of the N sample points.
    yerr : np.ndarray
        The y uncertainties of the N sample points.
    
    Returns
    -------
    fit : np.ndarray
        The coefficients of the best fitting polynomial
        from the lowest order term to the highest.
        i.e. [incercept, slope].
    uncerts : np.ndarray
        The uncertaintys on the coefficients of the best fitting
        polynomial. Ordered from the lowest order term to the highest.
        i.e. [incercept, slope].
    chisq : float
        The chi squared value of the best fit.
    redchisq : float
        The reduced chi square value of the best fit.
        redchisq = chisq / (N - 2)

    """
    return fit_poly_least_squares(xvals, yvals, yerr, order=1)


def calculate_poly_chisq(fit, xvals, yvals, yerr, order=1):
    """
    Get the chi-squared and reduced chi-squared for a
    best-fitting model.
    
    Parameters
    ----------
    fit : 1 x N array
        The best-fit coefficients ordered from lowest to
        highest order terms.
    xvals : np.ndarray
        The x-coordinates of the N sample points.
    yvals : np.ndarray
        The y-coordinates of the N sample points.
    yerr : np.ndarray
        The y uncertainties of the N sample points.
    order : int, optional
        Order of the best fitting fitting polynomial.
        Default: 1 

    Returns
    -------
    chisq : float
        The chi-squared value.
    redchisq : float
        The reduced chi-squared value.
        reduced chi = chi / (N - order - 1)
    
    """
    # Vandermonde matrix
    A = np.vander(xvals, order+1, increasing=True)

    # Matrix of Y Uncert
    C = np.diag(yerr * yerr)
    Cinv = np.linalg.inv(C)

    residuals = yvals - A@fit
    chisq = residuals.T @ Cinv @ residuals
    redchisq = chisq/(len(yvals) - (order+1))
    return chisq, redchisq