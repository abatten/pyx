import numpy as np
import scipy.interpolate as interpolate


class cdf_sampler(object):
    # __init__ computed the normalisation
    # factor then constructs the cumulative
    # distribution function (cdf).
    def __init__(self, x, y, seed=None):
        if seed is None:
            raise ValueError("Must provide seed for np.random.default_rng()")

        self.rng = np.random.default_rng(seed)
        self.seed = seed
        self.x_input = x
        self.y_input = y
        self.sample  = None

        pdf_fnorm = np.sum(y)
        self.cdf = np.cumsum(y / pdf_fnorm)

        self.inverse_cdf = interpolate.interp1d(self.cdf, self.x_input)

    # sample_n in produces a random sample
    # of n with a distribution matched to the
    # input array, y.
    def sample_n(self, n):
        self.r_values = self.rng.uniform(self.cdf[0], self.cdf[-1], size=n)
        self.sample = self.inverse_cdf(self.r_values)
        return self.sample
