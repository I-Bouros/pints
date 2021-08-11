#!/usr/bin/env python3
#
# This file is part of PINTS (https://github.com/pints-team/pints/) which is
# released under the BSD 3-clause license. See accompanying LICENSE.md for
# copyright notice and full license details.
#
import pints
import pints.functionaltests as ft


def two_dim_gaussian(n_iterations=None):
    if n_iterations is None:
        n_iterations = 4000
    problem = ft.RunMcmcMethodOnTwoDimGaussian(
        method=pints.HaarioACMC,
        n_chains=4,
        n_iterations=n_iterations,
        n_warmup=1000
    )

    return {
        'kld': problem.estimate_kld(),
        'mean-ess': problem.estimate_mean_ess()
    }


def banana(n_iterations=None):
    if n_iterations is None:
        n_iterations = 4000
    problem = ft.RunMcmcMethodOnBanana(
        method=pints.HaarioACMC,
        n_chains=4,
        n_iterations=n_iterations,
        n_warmup=1000
    )

    return {
        'kld': problem.estimate_kld(),
        'mean-ess': problem.estimate_mean_ess()
    }


def correlated_gaussian(n_iterations=None):
    if n_iterations is None:
        n_iterations = 8000
    problem = ft.RunMcmcMethodOnCorrelatedGaussian(
        method=pints.HaarioACMC,
        n_chains=4,
        n_iterations=n_iterations,
        n_warmup=4000
    )

    return {
        'kld': problem.estimate_kld(),
        'mean-ess': problem.estimate_mean_ess()
    }
