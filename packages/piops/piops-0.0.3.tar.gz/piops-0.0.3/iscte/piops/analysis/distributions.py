import numpy as np
from fitter import Fitter, get_common_distributions, get_distributions


def distfit():
    mu, sigma = 0, 0.1 # mean and standard deviation
    data = np.random.normal(mu, sigma, 10000)
    f = Fitter(data, distributions = get_common_distributions())
    f.fit()
    return f