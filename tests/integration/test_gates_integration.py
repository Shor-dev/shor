#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 20 20:24:28 2020

@author: zevunderwood
"""

from shor.gates import ID
from shor.layers import Qubits
from shor.operations import Measure
from shor.quantum import Circuit
from shor.backends import QuantumSimulator, QSession


def test_single_qubit():
    circuit = Circuit()
    circuit.add(Qubits(1))
    circuit.add(ID(0))  # Can also use H()
    circuit.add(Measure())

    sess = QSession(backend=QuantumSimulator())
    result = sess.run(circuit, num_shots=1024)

    # Accounting for random noise, results won't be exact
    assert result['1'] == 0
    assert result['0'] == 1024