#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul  8 10:44:36 2020

@author: zevunderwood
"""
from shor.gates import CNOT, Hadamard, Rz,PauliX
from shor.layers import Qubits
from shor.operations import Measure
from shor.quantum import Circuit
from shor.backends import QuantumSimulator, QSession
import math


def test_rz_0():
    circuit = Circuit()
    circuit.add(Qubits(1))
    circuit.add(Rz(0,angle = math.pi/4))
    circuit.add(Measure(0))

    sess = QSession(backend=QuantumSimulator())
    result = sess.run(circuit, num_shots = 1000)

    #Phaseshift gate should not affect 0th |0>
    assert result['0'] == 1000
    assert result['1'] == 0


def test_rz_1():
    circuit = Circuit()
    circuit.add(Qubits(1))
    circuit.add(PauliX(0))
    #circuit.add(Rz(0,angle = math.pi/4))
    circuit.add(Measure(0))

    sess = QSession(backend=QuantumSimulator())
    result = sess.run(circuit, num_shots=1000)

    assert result['1'] == 1000
    assert result['0'] == 0