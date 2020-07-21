#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 20 20:05:44 2020

@author: zevunderwood
"""

from shor.gates import U1,PauliX
from shor.layers import Qubits
from shor.operations import Measure
from shor.quantum import Circuit
from shor.backends import QuantumSimulator, QSession


def test_u1_integration():
    circuit = Circuit()
    circuit.add(Qubits(1))
    circuit.add(PauliX(0))
    circuit.add(U1(0))  
    circuit.add(Measure())

    sess = QSession(backend=QuantumSimulator())
    result = sess.run(circuit, num_shots=1024)

    # Accounting for random noise, results won't be exact
    assert result['0'] == 0
    assert result['1'] == 1024
