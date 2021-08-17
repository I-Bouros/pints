#
# Shared problems used in functional testing.
#
# This file is part of PINTS (https://github.com/pints-team/pints/) which is
# released under the BSD 3-clause license. See accompanying LICENSE.md for
# copyright notice and full license details.
#
import numpy as np

import pints
import pints.toy


class RunMcmcMethodOnProblem(object):
    """
    Base class for tests that run an MCMC method on a log-PDF.

    Parameters
    ----------
    log_pdf : pints.LogPDF
        The PDF to sample. Will be passed to a :class:`pints.MCMCController`.
    x0
        One or more starting points to be passed to the
        :class:`pints.MCMCController`.
    sigma0
        One or more ``sigma0`` parameters to be passed to the
        :class:`pints.MCMCController`.
    method : pints.MCMCSampler
        The method to test. Will be passed to the
        :class:`pints.MCMCController`.
    n_chains : int
        The number of chains to run. Will be passed to the
        :class:`pints.MCMCController`.
    n_iterations : int
        The number of iterations to run
    n_warmup : int
        The number of iterations to discard
    method_hyper_parameters : list
        A list of hyperparameter values.

    """

    def __init__(self, log_pdf, x0, sigma0, method, n_chains, n_iterations,
                 n_warmup, method_hyper_parameters):
        self.log_pdf = log_pdf

        controller = pints.MCMCController(
            log_pdf, n_chains, x0, sigma0=sigma0, method=method)
        controller.set_max_iterations(n_iterations)
        controller.set_log_to_screen(False)
        set_hyperparameters_for_any_mcmc_class(controller, method,
                                               method_hyper_parameters)
        self.chains = run_and_throw_away_warmup(controller, n_warmup)

    def estimate_kld(self):
        """
        Estimates the Kullback-Leibler divergence.

        Raises an ``AttributeError`` if the underlying LogPDF does not have a
        method ``kl_divergence()``.
        """
        chains = np.vstack(self.chains)
        return np.mean(self.log_pdf.kl_divergence(chains))

    def estimate_mean_ess(self):
        """
        Estimates the effective sample size (ESS) for each chain and each
        parameter and returns the mean ESS for across all chains and
        parameters.
        """
        # Estimate mean ESS for each chain
        n_chains, _, n_parameters = self.chains.shape
        ess = np.empty(shape=(n_chains, n_parameters))
        for chain_id, chain in enumerate(self.chains):
            ess[chain_id] = pints.effective_sample_size(chain)

        return np.mean(ess)

    def estimate_distance(self):
        """
        Estimates a measure of distance between the sampled chains and the true
        distribution.

        Raises an ``AttributeError`` if the underlying LogPDF does not have a
        method ``distance()``.
        """
        return self.log_pdf.distance(np.vstack(self.chains))


class RunMcmcMethodOnTwoDimGaussian(RunMcmcMethodOnProblem):
    """
    Tests a given MCMC method on a two-dimensional Gaussian distribution with
    means ``[0, 0]`` and sigma ``[1, 1]``.

    For constructor arguments, see :class:`RunMcmcMethodOnProblem`.
    """

    def __init__(self, method, n_chains, n_iterations, n_warmup,
                 method_hyper_parameters=None):
        log_pdf = pints.toy.GaussianLogPDF(mean=[0, 0], sigma=[1, 1])

        # Get initial parameters
        log_prior = pints.ComposedLogPrior(
            pints.GaussianLogPrior(mean=0, sd=10),
            pints.GaussianLogPrior(mean=0, sd=10))
        x0 = log_prior.sample(n=n_chains)
        sigma0 = None

        super().__init__(log_pdf, x0, sigma0, method, n_chains, n_iterations,
                         n_warmup, method_hyper_parameters)


class RunMcmcMethodOnBanana(RunMcmcMethodOnProblem):
    """
    Tests a given MCMC method on a two-dimensional
    :class:`pints.toy.TwistedGaussianLogPDF` distribution with means
    ``[0, 0]``.

    For constructor arguments, see :class:`RunMcmcMethodOnProblem`.
    """
    def __init__(self, method, n_chains, n_iterations, n_warmup,
                 method_hyper_parameters=None):
        log_pdf = pints.toy.TwistedGaussianLogPDF(dimension=2, b=0.1)

        # Get initial parameters
        log_prior = pints.MultivariateGaussianLogPrior([0, 0],
                                                       [[10, 0], [0, 10]])
        x0 = log_prior.sample(n_chains)
        sigma0 = np.diag(np.array([1, 3]))

        super().__init__(log_pdf, x0, sigma0, method, n_chains, n_iterations,
                         n_warmup, method_hyper_parameters)


'''
class RunMcmcMethodOnSimpleEggBox(RunMcmcMethodOnProblem):
    """
    Tests a given MCMC method on `pints.toy.SimpleEggBoxLogPDF`.
    """
    def __init__(self, method, n_chains, n_iterations, n_warmup,
                 method_hyper_parameters=None):
        sigma = 2
        r = 4
        log_pdf = pints.toy.SimpleEggBoxLogPDF(sigma, r)
        x0 = np.random.uniform(-15, 15, size=(n_chains, 2))
        sigma0 = None

        super().__init__(log_pdf, x0, sigma0, method, n_chains, n_iterations,
                         n_warmup, method_hyper_parameters)
'''


class RunMcmcMethodOnHighDimensionalGaussian(RunMcmcMethodOnProblem):
    """
    Tests a given MCMC method on a 20-dimensional
    :class:`pints.toy.HighDimensionalGaussianLogPDF` centered at the origin.

    For constructor arguments, see :class:`RunMcmcMethodOnProblem`.
    """
    def __init__(self, method, n_chains, n_iterations, n_warmup,
                 method_hyper_parameters=None):
        log_pdf = pints.toy.HighDimensionalGaussianLogPDF()
        x0 = np.random.uniform(-4, 4, size=(n_chains, 20))
        sigma0 = None

        super().__init__(log_pdf, x0, sigma0, method, n_chains, n_iterations,
                         n_warmup, method_hyper_parameters)


class RunMcmcMethodOnCorrelatedGaussian(RunMcmcMethodOnProblem):
    """
    Tests a given MCMC method on a 6-dimensional, highly correlated
    :class:`pints.toy.HighDimensionalGaussianLogPDF` centered at the origin.

    For constructor arguments, see :class:`RunMcmcMethodOnProblem`.
    """
    def __init__(self, method, n_chains, n_iterations, n_warmup,
                 method_hyper_parameters=None):
        log_pdf = pints.toy.HighDimensionalGaussianLogPDF(dimension=6, rho=0.8)
        x0 = np.random.uniform(-4, 4, size=(n_chains, 6))
        sigma0 = None

        super().__init__(log_pdf, x0, sigma0, method, n_chains, n_iterations,
                         n_warmup, method_hyper_parameters)


class RunMcmcMethodOnAnnulus(RunMcmcMethodOnProblem):
    """
    Tests a given MCMC method on a two-dimensional
    :class:`pints.toy.AnnulusLogPDF` distribution, with its highest values at
    any point ``x`` with ``np.linalg.norm(x) == 10``.

    For constructor arguments, see :class:`RunMcmcMethodOnProblem`.
    """
    def __init__(self, method, n_chains, n_iterations, n_warmup,
                 method_hyper_parameters=None):
        log_pdf = pints.toy.AnnulusLogPDF()
        x0 = log_pdf.sample(n_chains)
        sigma0 = None

        super().__init__(log_pdf, x0, sigma0, method, n_chains, n_iterations,
                         n_warmup, method_hyper_parameters)


class RunMcmcMethodOnMultimodalGaussian(RunMcmcMethodOnProblem):
    """
    Tests a given MCMC method on a two-dimensional
    :class:`pints.toy.MultimodalGaussianLogPDF` with modes at ``[0, 0]``,
    ``[5, 10]``, and ``[10, 0]``.

    For constructor arguments, see :class:`RunMcmcMethodOnProblem`.
    """
    def __init__(self, method, n_chains, n_iterations, n_warmup,
                 method_hyper_parameters=None):
        modes = [[0, 0],
                 [5, 10],
                 [10, 0]]
        covariances = [[[1, 0], [0, 1]],
                       [[2, 0.8], [0.8, 3]],
                       [[1, -0.5], [-0.5, 1]]]
        log_pdf = pints.toy.MultimodalGaussianLogPDF(modes, covariances)
        x0 = log_pdf.sample(n_chains)
        sigma0 = None

        super().__init__(log_pdf, x0, sigma0, method, n_chains, n_iterations,
                         n_warmup, method_hyper_parameters)


class RunMcmcMethodOnCone(RunMcmcMethodOnProblem):
    """
    Tests a given MCMC method on a two-dimensional
    :class:`pints.toy,ConeLogPDF` centered at ``[0, 0]``.

    For constructor arguments, see :class:`RunMcmcMethodOnProblem`.
    """
    def __init__(self, method, n_chains, n_iterations, n_warmup,
                 method_hyper_parameters=None):
        log_pdf = pints.toy.ConeLogPDF(dimensions=2, beta=0.6)
        x0 = log_pdf.sample(n_chains)
        sigma0 = None

        super().__init__(log_pdf, x0, sigma0, method, n_chains, n_iterations,
                         n_warmup, method_hyper_parameters)


def set_hyperparameters_for_any_mcmc_class(controller, method,
                                           method_hyper_parameters):
    """ Sets hyperparameters for any MCMC class. """
    if method_hyper_parameters is not None:
        if issubclass(method, pints.MultiChainMCMC):
            controller.sampler().set_hyper_parameters(
                method_hyper_parameters)
        else:
            for sampler in controller.samplers():
                sampler.set_hyper_parameters(method_hyper_parameters)


def run_and_throw_away_warmup(controller, n_warmup):
    """ Runs sampling then throws away warmup. """
    chains = controller.run()
    return chains[:, n_warmup:]
