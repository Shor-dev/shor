#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 18 16:02:33 2020

@author: zevunderwood
"""

from shor.gates import CNOT, Hadamard, Cx
from shor.layers import Qubits
from shor.operations import Measure
from shor.quantum import Circuit
from shor.backends import QuantumSimulator, QSession


def test_cx_int():
    circuit_1 = Circuit()
    circuit_1.add(Qubits(2))
    circuit_1.add(Hadamard(0))
    circuit_1.add(Cx(0, 1))
    circuit_1.add(Measure(0, 1))
    
    circuit_2 = Circuit()
    circuit_2.add(Qubits(2))
    circuit_2.add(Hadamard(1))
    circuit_2.add(Cx(0, 1))
    circuit_2.add(Measure(0, 1))    

    sess = QSession(backend=QuantumSimulator())
    result_1 = sess.run(circuit_1, num_shots=1024)
    result_2 = sess.run(circuit_2, num_shots=1024)
    
    assert result_1['01'] == 0
    assert result_1['10'] > 450
    assert result_1['00'] > 450
    assert result_1['11'] == 0

    assert result_2['01'] == 0
    assert result_2['10'] == 0 
    assert result_2['00'] > 450
    assert result_2['11'] > 450