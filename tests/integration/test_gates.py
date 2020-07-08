#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul  8 10:36:57 2020

@author: zevunderwood
"""
from shor.gates import CNOT, Hadamard,Ry
from shor.layers import Qubits
from shor.operations import Measure
from shor.quantum import Circuit
from shor.backends import QuantumSimulator, QSession
import numpy as np

def test_ry_int():
    circuit = Circuit()
    circuit.add(Qubits(1))
    circuit.add(Ry(0,angle = np.pi/2))
    circuit.add(Measure(0))

    sess = QSession(backend=QuantumSimulator())
    result = sess.run(circuit, num_shots=1000)

    assert result['0']>450
    assert result['1']>450