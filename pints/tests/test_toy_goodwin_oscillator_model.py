#!/usr/bin/env python3
#
# Tests if the goodwin oscillator (toy) model runs.
#
# This file is part of PINTS.
#  Copyright (c) 2017-2018, University of Oxford.
#  For licensing information, see the LICENSE file distributed with the PINTS
#  software package.
#
import unittest
import pints
import pints.toy
import numpy as np
from scipy.interpolate import interp1d


class TestGoodwinOscillatorModel(unittest.TestCase):
    """
    Tests if the goodwin oscillator (toy) model runs.
    """

    def test_run(self):
        model = pints.toy.GoodwinOscillatorModel()
        self.assertEqual(model.n_parameters(), 5)
        self.assertEqual(model.n_outputs(), 3)
        times = model.suggested_times()
        parameters = model.suggested_parameters()
        values = model.simulate(parameters, times)
        self.assertEqual(values.shape, (len(times), 3))

    def test_values(self):
        # value-based tests of Goodwin-oscillator
        model = pints.toy.GoodwinOscillatorModel()
        parameters = [3, 2.5, 0.15, 0.1, 0.12]
        times = np.linspace(0, 10, 101)
        values = model.simulate(parameters, times)
        self.assertEqual(values[0, 0], 0.0054)
        self.assertEqual(values[0, 1], 0.053)
        self.assertEqual(values[0, 2], 1.93)
        self.assertAlmostEqual(values[100, 0], 0.0061854, places=6)
        self.assertAlmostEqual(values[100, 1], 0.1779547, places=6)
        self.assertAlmostEqual(values[100, 2], 2.6074527, places=6)

    def test_sensitivity(self):
        model = pints.toy.GoodwinOscillatorModel()
        parameters = [3, 2.5, 0.15, 0.1, 0.12]
        k2, k3, m1, m2, m3 = parameters
        time = np.linspace(0, 10, 101)
        state = [0.01, 0.1, 2]
        x, y, z = state
        ret = model.jacobian(state, time, parameters)
        self.assertEqual(ret[0, 0], -m1)
        self.assertEqual(ret[0, 1], 0)
        self.assertEqual(ret[0, 2], -10 * z**9 / ((1 + z**10)**2))
        self.assertEqual(ret[1, 0], k2)
        self.assertEqual(ret[1, 1], -m2)
        self.assertEqual(ret[1, 2], 0)
        self.assertEqual(ret[2, 0], 0)
        self.assertEqual(ret[2, 1], k3)
        self.assertEqual(ret[2, 2], -m3)
        values = model.simulate(parameters, time)
        values1, dvals = model.simulateS1(parameters, time)
        self.assertTrue(np.array_equal(values.shape, values1.shape))
        self.assertTrue(
            np.array_equal(dvals.shape,
                           np.array([len(time),
                                    model.n_outputs(), model.n_parameters()])))
        # note -- haven't coded this up separately to check but compare against
        # current output in case of future changes
        self.assertTrue(np.abs(-2.20655371e-05 - dvals[10, 0, 0]) < 10**(-5))
        for i in range(len(time)):
            for j in range(3):
                self.assertTrue(
                    np.abs(values[i, j] - values1[i, j]) < 10**(-3))

    def test_sensitivities(self):
        model = pints.toy.GoodwinOscillatorModel()
        times_finer = np.linspace(0, 100, 500)
        parameters = model.suggested_parameters()
        sols, sens = model.simulateS1(parameters, times_finer)
        f = interp1d(times_finer, sens[:, 0][:, 2])
        self.assertTrue(np.abs(f([35])[0] - 0.0770570443277744) <= 0.01)
        f = interp1d(times_finer, sens[:, 1][:, 3])
        self.assertTrue(np.abs(f([80])[0] - 3.3570408738564357) <= 0.01)


if __name__ == '__main__':
    unittest.main()
