#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul  8 10:44:36 2020

@author: zevunderwood
"""
from shor.gates import CNOT, Hadamard,PauliX,U3,Rx
from shor.layers import Qubits
from shor.operations import Measure
from shor.quantum import Circuit
from shor.backends import QuantumSimulator, QSession
import math
import numpy as np


def test_U3_int():
    circuit_1 = Circuit()
    circuit_1.add(Qubits(1))
    circuit_1.add(U3(0,theta = np.pi/2,phi = -np.pi/2,alpha = np.pi/2))
    circuit_1.add(Measure(0))
    
    circuit_2 = Circuit()
    circuit_2.add(Qubits(1))
    circuit_2.add(Rx(theta = np.pi))
    circuit_2.add(Measure(0))

    sess = QSession(backend=QuantumSimulator())
    result_1 = sess.run(circuit_1, num_shots=1024)
    result_2 = sess.run(circuit_2, num_shots=1024)

    assert result_1['0'] > 450
    assert result_1['1'] > 450
    assert result_2['0'] > 450
    assert result_2['1'] > 450
    
    

