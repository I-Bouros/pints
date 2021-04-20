#!/usr/bin/env python3
#
# This file is part of PINTS (https://github.com/pints-team/pints/) which is
# released under the BSD 3-clause license. See accompanying LICENSE.md for
# copyright notice and full license details.
#

from __future__ import division

import pints

from ._problems import (RunMcmcMethodOnTwoDimGaussian,
                        RunMcmcMethodOnCorrelatedGaussian)


def test_dram_acmc_on_two_dim_gaussian(n_iterations=None):
    if n_iterations is None:
        n_iterations = 8000
    problem = RunMcmcMethodOnTwoDimGaussian(
        method=pints.DramACMC,
        n_chains=4,
        n_iterations=n_iterations,
        n_warmup=2000
    )

    return {
        'kld': problem.estimate_kld(),
        'mean-ess': problem.estimate_mean_ess()
    }


def test_dram_acmc_on_correlated_gaussian(n_iterations=None):
    if n_iterations is None:
        n_iterations = 8000
    problem = RunMcmcMethodOnCorrelatedGaussian(
        method=pints.DramACMC,
        n_chains=4,
        n_iterations=n_iterations,
        n_warmup=4000
    )

    return {
        'kld': problem.estimate_kld(),
        'mean-ess': problem.estimate_mean_ess()
    }
