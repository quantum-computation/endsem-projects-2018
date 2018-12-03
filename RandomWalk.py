import numpy as np
import matplotlib.pyplot as plt

def flip(state, parameters):
    """Coin Transformation C"""
    new_state = []
    a, b, c, d = parameters
    for ket, amp in state:
        n, coin = ket
        if coin == 0:
            new_state.append(((n, 0), a*amp))
            new_state.append(((n, 1), b*amp))
        elif coin == 1:
            new_state.append(((n, 0), c*amp))
            new_state.append(((n, 1), d*amp))
    return new_state

def shift(state):
    """Shift Transformation S"""
    new_state = []
    for ket, amp in state:
        n, coin = ket
        if coin == 1:
            new_state.append(((n+1, coin), amp))
        if coin == 0:
            new_state.append(((n-1, coin), amp))
    return new_state

def simplify(state):
    """Combines like terms in the state vector"""
    kets = []
    new_state = []
    for ket, amp in state:
        if ket not in kets:
            new_amp = sum(a for k, a in state if k == ket)
            kets.append(ket)
            new_state.append((ket, new_amp))
    return new_state


def walk(num_iterations, parameters):
    """Performs a quantum random walk for num_iteration steps using parameters
    for the coin transformation"""
    state = [((0, 0), 1)]
    for i in range(num_iterations):
        state = flip(state, parameters)
        state = simplify(state)
        state = shift(state)
        state = simplify(state)
    return state

def plot_state(state):
    """Plots the state vector"""
    min_val = min(state, key=lambda ka: ka[0][0])[0][0]
    max_val = max(state, key=lambda ka: ka[0][0])[0][0]
    X = np.arange(min_val, max_val+1)
    Y = np.zeros((len(X)))
    for i, x in enumerate(X):
        for ket, amp in state:
            if ket[0] == x:
                Y[i] += abs(amp)**2
    plt.plot(X,Y)
    plt.ylabel("$|\psi(x)|^2$")
    plt.xlabel("$x$")
    plt.title("Quantum Random Walk")
    plt.show()

def main():
    parameters = [2**-.5, 2**-.5, 2**-.5, -2**-.5] # Hadamard Transformation 
    state = walk(100, parameters)
    plot_state(state)

if __name__ == '__main__':
 main()
