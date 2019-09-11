#
# Adaptive covariance MCMC method
#
# This file is part of PINTS.
#  Copyright (c) 2017-2018, University of Oxford.
#  For licensing information, see the LICENSE file distributed with the PINTS
#  software package.
#
from __future__ import absolute_import, division
from __future__ import print_function, unicode_literals
import pints
import numpy as np


class RemiACMCMC(pints.GlobalAdaptiveCovarianceMCMC):
    r"""
    Adaptive covariance MCMC, as described in [1]. In this method a
    covariance matrix is tuned so that the acceptance rate of the
    MCMC steps converges to a user specified value.

    Initialise::

        Sigma = diagonal matrix of dimensions equal to number of parameters
        mu = theta_0
        log(a_0) = 0
        adaptation_count = 0

    After adaptation, in each iteration (t)::

        adaptation_count++
        gamma = (adaptation_count)^-eta
        theta* ~ N(theta_t, a Sigma)
        standard random walk Metropolis accept-reject step
        if accept:
            theta_(t+1) = theta*
            accepted = 1
        else:
            theta_(t+1) = theta_t
            accepted = 0
        Sigma = (1 - gamma) Sigma + (theta_(t+1) - mu)^t (theta_(t+1) - mu)
        mu = (1 - gamma) mu + gamma theta_(t+1)
        log(a) += gamma (accepted - target_acceptance_rate)


    [1] Uncertainty and variability in models of the cardiac action potential:
    Can we build trustworthy models?
    Johnstone, Chang, Bardenet, de Boer, Gavaghan, Pathmanathan, Clayton,
    Mirams (2015) Journal of Molecular and Cellular Cardiology

    *Extends:* :class:`GlobalAdaptiveCovarianceMCMC`
    """
    def __init__(self, x0, sigma0=None):
        super(RemiACMCMC, self).__init__(x0, sigma0)

    def ask(self):
        """ See :meth:`SingleChainMCMC.ask()`. """
        super(RemiACMCMC, self).ask()

        # Propose new point
        if self._proposed is None:

            # Note: Normal distribution is symmetric
            #  N(x|y, sigma) = N(y|x, sigma) so that we can drop the proposal
            #  distribution term from the acceptance criterion
            self._proposed = np.random.multivariate_normal(
                self._current, np.exp(self._loga) * self._sigma)

            # Set as read-only
            self._proposed.setflags(write=False)

        # Return proposed point
        return self._proposed

    def _initialise(self):
        """
        See :meth: `AdaptiveCovarianceMCMC._initialise()`.
        """
        super(RemiACMCMC, self)._initialise()

        # log adaptation
        self._loga = 0

    def tell(self, fx):
        """ See :meth:`pints.AdaptiveCovarianceMCMC.tell()`. """
        super(RemiACMCMC, self).tell(fx)

        # Update log acceptance
        if self._adaptive:
            self._loga += (self._gamma *
                           (self._accepted - self._target_acceptance))

        # Return new point for chain
        return self._current
