#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 21 12:59:06 2020

@author: zevunderwood
"""

from shor.gates import CNOT, Hadamard,PauliX,PauliY,PauliZ
from shor.layers import Qubits
from shor.operations import Measure
from shor.quantum import Circuit
from shor.backends import QuantumSimulator, QSession


def test_paulix_integration():
    circuit = Circuit()
    circuit.add(Qubits(1))
    circuit.add(PauliX(0))  # Can also use H()
    circuit.add(Measure())

    sess = QSession(backend=QuantumSimulator())
    result = sess.run(circuit, num_shots=1024)

    # Accounting for random noise, results won't be exact
    assert result['0'] == 0
    assert result['1'] == 1024


def test_pauliy_integration():
    circuit = Circuit()
    circuit.add(Qubits(1))
    circuit.add(PauliY(0))  # Can also use H()
    circuit.add(Measure())

    sess = QSession(backend=QuantumSimulator())
    result = sess.run(circuit, num_shots=1024)

    # Accounting for random noise, results won't be exact
    assert result['0'] == 0
    assert result['1'] == 1024
    

def test_pauliz_integration():
    circuit = Circuit()
    circuit.add(Qubits(1))
    circuit.add(Hadamard(0))
    circuit.add(PauliZ(0))  # Can also use H()
    circuit.add(Measure())

    sess = QSession(backend=QuantumSimulator())
    result = sess.run(circuit, num_shots=1024)

    # Accounting for random noise, results won't be exact
    assert result['0'] > 450
    assert result['1'] > 450