# Quantum Battleship

Project done by:

	    Name			ID
    Jay Goswami		    201501037
    Nirav Doshi		    201501056
    Hiren Chauhan		    201501195
    Sachin Chauhan	            201501200
    Rohan Maheshwari	    201501428

#### Instructions

The python packages that are required to play the game can be installed by the following commands:
```bash
pip install numpy
pip install qiskit
```

To play the game simple run the corresponding python file using the following command:
```bash
python3 game_1.py
```
	OR
```bash
python3 game_2.py
```

### Game 1(Simple Version)

Quantum Battleship is a two player game where both the players have a number of ships which they can place in any position. The two players attack at different position and the one who destroys all the ships of the opponent wins the battle. 

Now what happens in Quantum Battleship is that some ships take more than 1 hits to be destroyed. One qubit is used for every ships and the convention is that, if the ship is in 0 state, then it is intact and 1 means that it is destroyed. Here the ships are not in superposition but the state in which the ships exists are in superposition. Initially all the ships are in 0 state but when the opponent fires a bomb then we apply NOT gate using u3 operator (fractal NOT) available in QISKit. If the respective ship will be destroyed by 2 hits than we rotate the axis by pi/2 and then we take the measurement of it. For this game we took Quantum Register and initialized with single qubit for each position and took classical registers with normal bit for measuring. Then we implement a Quantum Circuit with these quantum and classical registers. In fact it will be the superposition state, called u3(0.5*pi,0,0) |0>. Measuring whether this is 0 or 1 will force it to randomly choose one or the other, with equal probabilities and we get the result accordingly whether the ship is destroyed or not.

### Game 2(Enhanced version)

The second version of the game is an improved version of the first game, where capabilities like both the players have two types of attacks - bombs and torpedoes, has been introduced. Here, Consider 3 axis, one for the reference, second for the measurement for bombs and the third for torpedoes. The catch is that, ship can be immune to any of them. When a player attacks with a bomb the ship itself does not know whether it is immune to bombs or not. When we calculate according to the probabilities if the probability is more than 50% we apply fractal NOT gate (u3) and change it to destroyed. The states initially are according to game 1. Now we measure it and if it comes to be 1 then it is considered destroyed and if not then the attacker get to know that the ship is immune to bombs. Next, he/she will attack the same ship with a torpedo. Now the same ship will know that it is immune to bombs so the next attack with bombs will not affect it. But for an attack with a torpedo, we will have to check with the 3rd axis which can be|0⟩ or |1⟩. Now according to the probability it can check the state. We apply hadamard gate to it and take the measurement. Now if the ship is destroyed, then the state will change to 1 otherwise 0. A ship can be immune to both bombs as well as torpedoes. But now the ship does not remember that it was immune to bombs or not. Hence, if attacked by bomb, there is a chance that it will be destroyed. So here we have used u3, hadamard gates to change the states of the qubits that is ships. In this game, both the players attack the position with any one type of attack and after both of their attacks are executed then only the damages are displayed. Therefore, both the players will get equal number of attacks, and hence equal number of chances to destroy all the ships of the opponent.
