#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 24 11:50:44 2020

@author: zevunderwood
"""

from shor.gates import S,Sdg,T,Tdg,PauliX
from shor.layers import Qubits
from shor.operations import Measure
from shor.quantum import Circuit
from shor.backends import QuantumSimulator, QSession


def test_s_integration():
    circuit = Circuit()
    circuit.add(Qubits(1))
    circuit.add(S(0))  # Can also use H()
    circuit.add(Measure())

    sess = QSession(backend=QuantumSimulator())
    result = sess.run(circuit, num_shots=1024)

    
    assert result['0'] == 1024
    assert result['1'] == 0


def test_sdg_integration():
    circuit = Circuit()
    circuit.add(Qubits(1))
    circuit.add(PauliX(0))
    circuit.add(Sdg(0))  # Can also use H()
    circuit.add(Measure())

    sess = QSession(backend=QuantumSimulator())
    result = sess.run(circuit, num_shots=1024)

    
    assert result['1'] == 1024
    assert result['0'] == 0
    

def test_t_integration():
    circuit = Circuit()
    circuit.add(Qubits(1))
    circuit.add(T(0))  # Can also use H()
    circuit.add(Measure())

    sess = QSession(backend=QuantumSimulator())
    result = sess.run(circuit, num_shots=1024)

    
    assert result['0'] == 1024
    assert result['1'] == 0


def test_tdg_integration():
    circuit = Circuit()
    circuit.add(Qubits(1))
    circuit.add(PauliX(0))
    circuit.add(Tdg(0))  # Can also use H()
    circuit.add(Measure())

    sess = QSession(backend=QuantumSimulator())
    result = sess.run(circuit, num_shots=1024)

    
    assert result['1'] == 1024
    assert result['0'] == 0