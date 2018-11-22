import numpy as np
import matplotlib.pyplot as plt

from qiskit import Aer, IBMQ
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister
from qiskit import available_backends, execute, register, get_backend, compile

from qiskit.tools import visualization


def oracle(circuit, f_in, f_out, aux, n, manual_index):
    for i in range(n):
        if(((manual_index >> i) & 1) == 0):
            circuit.x(f_in[n - i - 1])
    
    for i in range(n):
        circuit.cx(f_in[i], aux[i])

    circuit.ccx(aux[0], aux[1], aux[3])
    circuit.ccx(aux[2], aux[3], f_out[0])
    circuit.ccx(aux[0], aux[1], aux[3])
    
    for i in range(n):
        circuit.cx(f_in[i], aux[i])
    
    for i in range(n):
        if(((manual_index >> i) & 1) == 0):
            circuit.x(f_in[n - i - 1])

def n_controlled_Z(circuit, controls, target):
    if (len(controls) > 2):
        raise ValueError('The controlled Z with more than 2 ' +
                         'controls is not implemented')
    elif (len(controls) == 1):
        circuit.h(target)
        circuit.cx(controls[0], target)
        circuit.h(target)
    elif (len(controls) == 2):
        circuit.h(target)
        circuit.ccx(controls[0], controls[1], target)
        circuit.h(target)

def inversion_about_average(circuit, f_in, n):
    for j in range(n):
        circuit.h(f_in[j])
    for j in range(n):
        circuit.x(f_in[j])
    n_controlled_Z(circuit, [f_in[j] for j in range(n-1)], f_in[n-1])
    for j in range(n):
        circuit.x(f_in[j])
    for j in range(n):
        circuit.h(f_in[j])

def input_state(circuit, f_in, f_out, n):
    for j in range(n):
        circuit.h(f_in[j])
    circuit.x(f_out)
    circuit.h(f_out)

def get_predefine_index(arr):
    return arr.index(min(arr))

def Grover_search(arr):
    n = 3

    f_in = QuantumRegister(n)
    f_out = QuantumRegister(1)
    aux = QuantumRegister(n + 1)

    ans = ClassicalRegister(n)

    grover = QuantumCircuit()
    grover.add(f_in)
    grover.add(f_out)
    grover.add(aux)
    grover.add(ans)

    predefined_index = get_predefine_index(arr)

    input_state(grover, f_in, f_out, n)

    T = 2
    for t in range(T):
        oracle(grover, f_in, f_out, aux, n, predefined_index)
        inversion_about_average(grover, f_in, n)

    for j in range(n):
        grover.measure(f_in[j], ans[j])

    backend = Aer.get_backend('qasm_simulator')
    job = execute([grover], backend=backend, shots=1000)
    result = job.result()

    counts = result.get_counts(grover)
    inv = [(value, key) for key, value in counts.items()]
    outstr = str(max(inv)[1])
    ind = 0
    for i in range(len(outstr)):
        if outstr[i] == '1':
            ind = ind * 2 + 1
        else:
            ind = ind * 2
    # print(ind)
    # print(arr[ind])
    return ind
    #return arr[ind]
    #visualization.plot_histogram(counts)

# a = [1, 2, 0, 4, 5]
# Grover_search(a)