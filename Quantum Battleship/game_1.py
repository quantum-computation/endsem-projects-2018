from qiskit import ClassicalRegister, QuantumRegister, QuantumCircuit
from qiskit import execute, register
from qiskit import Aer
import getpass, random, numpy, math

print("Welcome to Quantum Battleship!")
randPlace = input("> Press Enter to play...\n").upper()

device = Aer.get_backend('qasm_simulator') 

randPlace = input("> Press Enter to start placing ships...\n").upper()

shipPos = [ [-1]*3 for _ in range(2)]

for player in [0,1]:
  for ship in [0,1,2]:
      choosing = True
      while (choosing):
          position = getpass.getpass("Player " + str(player+1) + ", choose a position for ship " + str(ship+1) + " (0, 1, 2, 3 or 4)\n" )
          if position.isdigit(): 
              position = int(position)
              if (position in [0,1,2,3,4]) and (not position in shipPos[player]): 
                  shipPos[player][ship] = position
                  choosing = False
                  print ("\n")
              elif position in shipPos[player]:
                  print("\nYou already have a ship there. Try again.\n")
              else:
                  print("\nThat's not a valid position. Try again.\n")
          else:
              print("\nThat's not a valid position. Try again.\n")

game = True

shots = 1024

grid = [{},{}]

damage = [ [0]*5 for _ in range(2)] 

destroyed = [False]*2
game = not destroyed[0] and not destroyed[1]

while (game):
    
    bomb = [ [0]*5 for _ in range(2)]
    
    input("> Press Enter to place some bombs...\n")
    
    for player in range(2):
        print("\n\nIt's now Player " + str(player+1) + "'s turn.\n")
        choosing = True
        while (choosing):
            position = input("Choose a position to bomb (0, 1, 2, 3 or 4)\n")
            if position.isdigit(): 
                position = int(position)
                if position in range(5): 
                    bomb[player][position] = 1
                    choosing = False
                    print ("\n")
                else:
                    print("\nThat's not a valid position. Try again.\n")
            else:
                print("\nThat's not a valid position. Try again.\n")
    
    qc = []
    for player in range(2):
        q = QuantumRegister(5)
        c = ClassicalRegister(5)
        qc.append( QuantumCircuit(q, c) )
        
        for position in range(5):
            if bomb[(player+1)%2][position] == 1:
                for ship in [0,1,2]:
                    if ( position == shipPos[player][ship] ):
                        frac = 1/(ship+1)
                        qc[player].u3(frac * math.pi, 0.0, 0.0, q[position])
                                        
        for position in range(5):
            qc[player].measure(q[position], c[position])

    job = execute(qc, backend=device, shots=shots)
    if not device.configuration()['simulator']:
        print("\nWe've now submitted the job to the quantum computer to see what happens to the ships of each player\n(it might take a while).\n")
    else:
        print("\nWe've now submitted the job to the simulator to see what happens to the ships of each player.\n")
    
    for player in range(2):
        grid[player] = job.result().get_counts(qc[player])
    #print(grid[0])
    for player in range(2):
        for bitString in grid[player].keys():
            for position in range(5):
                if (bitString[4-position]=="1" and bomb[(player+1)%2][position] == 1):
                    damage[player][position] += grid[player][bitString]/shots          
        
    for player in [0,1]:
        input("\nPress Enter to see the results for Player " + str(player+1) + "'s ships...\n")
        display = [" ?  "]*5
        for position in shipPos[player]:
            if ( damage[player][position] > 0.1 ):
                if (damage[player][position]>0.9):
                    display[position] = "100%"
                else:
                    display[position] = str(int( 100*damage[player][position] )) + "% "
                    
        print("Here is the percentage damage for ships that have been bombed.\n")
        print(display[ 4 ] + "    " + display[ 0 ])
        print(" |\     /|")
        print(" | \   / |")
        print(" |  \ /  |")
        print(" |  " + display[ 2 ] + " |")
        print(" |  / \  |")
        print(" | /   \ |")
        print(" |/     \|")
        print(display[ 3 ] + "    " + display[ 1 ])
        print("\n")
        print("Ships with 95% damage or more have been destroyed\n")

        print("\n")

        if (damage[player][ shipPos[player][0] ]>.9) and (damage[player][ shipPos[player][1] ]>.9) and (damage[player][ shipPos[player][2] ]>.9):
            print ("***All Player " + str(player+1) + "'s ships have been destroyed!***\n\n")
            destroyed[player] = True

    game = not destroyed[0] and not destroyed[1]

if ( destroyed[0] and not destroyed[1] ):
    print ( "Player 2 wins" )
elif (destroyed[1] and not destroyed[0]):
	print ("Player 1 wins" )
else:
	print ("Match Tied")    
print("")
print("=====================================GAME OVER=====================================")
print("")