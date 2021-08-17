#!/usr/bin/env python3
#
# Functional tests for EmceeHammerMCMC
#
# This file is part of PINTS (https://github.com/pints-team/pints/) which is
# released under the BSD 3-clause license. See accompanying LICENSE.md for
# copyright notice and full license details.
#
import pints
import pints.functionaltests as ft


def two_dim_gaussian(n_iterations=10000, n_warmup=1000):
    """
    Tests :class:`pints.EmceeHammerMCMC`
    on a two-dimensional Gaussian distribution with true solution
    ``[0, 0]`` and returns a dictionary with entries ``kld`` and ``mean-ess``.

    For details of the solved problem, see
    :class:`pints.functionaltests.RunMcmcMethodOnTwoDimGaussian`.
    """
    problem = ft.RunMcmcMethodOnTwoDimGaussian(
        _method, 10, n_iterations, n_warmup)
    return {
        'kld': problem.estimate_kld(),
        'mean-ess': problem.estimate_mean_ess()
    }


def banana(n_iterations=10000, n_warmup=2000):
    """
    Tests :class:`pints.EmceeHammerMCMC`
    on a two-dimensional "twisted Gaussian" distribution with true solution
    ``[0, 0]`` and returns a dictionary with entries ``kld`` and ``mean-ess``.

    For details of the solved problem, see
    :class:`pints.functionaltests.RunMcmcMethodOnBanana`.
    """
    problem = ft.RunMcmcMethodOnBanana(
        _method, 10, n_iterations, n_warmup)
    return {
        'kld': problem.estimate_kld(),
        'mean-ess': problem.estimate_mean_ess()
    }


def correlated_gaussian(n_iterations=8000, n_warmup=4000):
    """
    Tests :class:`pints.EmceeHammerMCMC`
    on a six-dimensional highly correlated Gaussian distribution with true
    solution ``[0, 0, 0, 0, 0, 0]`` and returns a dictionary with entries
    ``kld`` and ``mean-ess``.

    For details of the solved problem, see
    :class:`pints.functionaltests.RunMcmcMethodOnCorrelatedGaussian`.
    """
    problem = ft.RunMcmcMethodOnCorrelatedGaussian(
        _method, 10, n_iterations, n_warmup)
    return {
        'kld': problem.estimate_kld(),
        'mean-ess': problem.estimate_mean_ess()
    }


def annulus(n_iterations=4000, n_warmup=2000):
    """
    Tests :class:`pints.EmceeHammerMCMC`
    on a two-dimensional annulus distribution with radius 10, and returns a
    dictionary with entries ``distance`` and ``mean-ess``.

    For details of the solved problem, see
    :class:`pints.functionaltests.RunMcmcMethodOnAnnulus`.
    """
    problem = ft.RunMcmcMethodOnAnnulus(
        _method, 10, n_iterations, n_warmup)
    return {
        'distance': problem.estimate_distance(),
        'mean-ess': problem.estimate_mean_ess()
    }


def multimodal_gaussian(n_iterations=10000, n_warmup=1000):
    """
    Tests :class:`pints.EmceeHammerMCMC`
    on a two-dimensional multi-modal Gaussian distribution with modes at
    ``[0, 0]``, ``[5, 10]``, and ``[10, 0]``, and returns a dict with entries
    "kld" and "mean-ess".

    For details of the solved problem, see
    :class:`pints.functionaltests.RunMcmcMethodOnMultimodalGaussian`.
    """
    problem = ft.RunMcmcMethodOnMultimodalGaussian(
        _method, 10, n_iterations, n_warmup)
    return {
        'kld': problem.estimate_kld(),
        'mean-ess': problem.estimate_mean_ess()
    }


def cone(n_iterations=10000, n_warmup=1000):
    """
    Tests :class:`pints.EmceeHammerMCMC`
    on a two-dimensional cone distribution centered at ``[0, 0]``, and returns
    a dict with entries "distance" and "mean-ess".

    For details of the solved problem, see
    :class:`pints.functionaltests.RunMcmcMethodOnCone`.
    """
    problem = ft.RunMcmcMethodOnCone(
        _method, 10, n_iterations, n_warmup)
    return {
        'distance': problem.estimate_distance(),
        'mean-ess': problem.estimate_mean_ess()
    }


_method = pints.EmceeHammerMCMC
_functional_tests = [
    annulus,
    banana,
    cone,
    correlated_gaussian,
    multimodal_gaussian,
    two_dim_gaussian,
]
