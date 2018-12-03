import sys
from qiskit import *
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister, QISKitError
from qiskit import execute, IBMQ, Aer
from qiskit import compile,Aer
from qiskit.tools import visualization

def input_state(circuit,f_in,f_out,n):
    for j in range(n):
        circuit.h(f_in[j])
    circuit.x(f_out)
    circuit.h(f_out)

def oracle(circuit,f_in,f_out,aux,n,expression_3_sat):
    num_clauses = len(expression_3_sat)
    if(num_clauses > 3):
        raise ValueError('Not_more_than_3')
    for(k,clause) in enumerate(expression_3_sat):
        for literal in clause:
            if literal > 0:
                circuit.cx(f_in[literal-1],aux[k])
            else:
                circuit.x(f_in[-literal-1])
                circuit.cx(f_in[-literal-1],aux[k])
        circuit.ccx(f_in[0],f_in[1],aux[num_clauses])
        circuit.ccx(f_in[2],aux[num_clauses],aux[k])
        circuit.ccx(f_in[0],f_in[1],aux[num_clauses])
        for literal in clause:
            if literal < 0:
                circuit.x(f_in[-literal-1])
    if(num_clauses == 1):
        circuit.cx(aux[0],f_out[0])
    elif(num_clauses == 2):
        circuit.ccx(aux[0],aux[1],f_out[0])
    elif(num_clauses == 3):
        circuit.ccx(aux[0],aux[1],aux[num_clauses])
        circuit.ccx(aux[2],aux[num_clauses],f_out[0])
        circuit.ccx(aux[0],aux[1],aux[num_clauses])
    for(k,clause) in enumerate(expression_3_sat):
        for literal in clause:
            if literal > 0:
                circuit.cx(f_in[literal-1],aux[k])
            else:
                circuit.x(f_in[-literal-1])
                circuit.cx(f_in[-literal-1],aux[k])
        circuit.ccx(f_in[0],f_in[1],aux[num_clauses])
        circuit.ccx(f_in[2],aux[num_clauses],aux[k])
        circuit.ccx(f_in[0],f_in[1],aux[num_clauses])
        for literal in clause:
            if literal < 0:
                circuit.x(f_in[-literal-1])

def inversion_about_average(circuit,f_in,n):
    for j in range(n):
        circuit.h(f_in[j])
    for j in range(n):
        circuit.x(f_in[j])
    n_controlled_Z(circuit,[f_in[j] for j in range(n-1)],f_in[n-1])
    for j in range(n):
        circuit.x(f_in[j])
    for j in range(n):
        circuit.h(f_in[j])
        
def n_controlled_Z(circuit,controls,target):
    if(len(controls) > 2):
        raise ValueError('more_than_2_controls_is_not_implemented')
    elif(len(controls) == 1):
        circuit.h(target)
        circuit.cx(controls[0],target)
        circuit.h(target)
    elif(len(controls)== 2):
        circuit.h(target)
        circuit.ccx(controls[0],controls[1],target)
        circuit.h(target)
        

n=3
expression_3_sat = [[1,2,-3],[-1,-2,-3],[1,-2,3]]
f_in = QuantumRegister(n)
f_out = QuantumRegister(1)
aux = QuantumRegister(len(expression_3_sat) + 1)
ans = ClassicalRegister(n)
qc = QuantumCircuit(f_in,f_out,aux,ans,name = 'grover_search')

input_state(qc,f_in,f_out,n)
oracle(qc,f_in,f_out,aux,n,expression_3_sat)
inversion_about_average(qc,f_in,n)
oracle(qc,f_in,f_out,aux,n,expression_3_sat)
inversion_about_average(qc,f_in,n)

for j in range(n):
    qc.measure(f_in[j],ans[j])
    
quantum_simulator = Aer.get_backend('qasm_simulator')
qobj = compile(qc,quantum_simulator,shots=2048)
job = quantum_simulator.run(qobj)
#job = execute(qc,backend = Aer.get_backend('qasm_simulator'),shots = 100)
result = job.result()
counts = result.get_counts('grover_search')
visualization.plot_histogram(counts)
                    