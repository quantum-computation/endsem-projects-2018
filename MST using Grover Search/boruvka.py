from collections import defaultdict 
from groverSearch import Grover_search

class Graph: 

    def __init__(self,vertices): 
        self.V= vertices
        self.graph = []
        
    def addEdge(self,u,v,w): 
        self.graph.append([u,v,w]) 

    def find(self, parent, i): 
        if parent[i] == i:
            return i
        parent[i] = self.find(parent, parent[i]) 
        return parent[i]

    def union(self, parent, rank, x, y): 
        xroot = self.find(parent, x) 
        yroot = self.find(parent, y) 

        if rank[xroot] < rank[yroot]: 
            parent[xroot] = yroot 
        elif rank[xroot] > rank[yroot]: 
            parent[yroot] = xroot 
        else : 
            parent[yroot] = xroot 
            rank[xroot] += 1

    def boruvkaMST(self): 
        parent = []
        rank = []
        cheapest =[] 
        numTrees = self.V 
        MSTweight = 0
        
        # Initialize variable
        for node in range(self.V): 
            parent.append(node) 
            rank.append(0)
            cheapest.append([])
        
        # Run this loop until we will have only one remaining component
        while numTrees > 1: 

            for i in range(len(self.graph)): 
                u,v,w = self.graph[i] 
                set1 = self.find(parent, u) 
                set2 = self.find(parent ,v) 

                if set1 != set2:
                    cheapest[set1].append([w, u, v])
                    cheapest[set2].append([w, u, v]) 

            # This for loop find the edges which has least nearer component 
            for node in range(self.V):

                if len(cheapest[node]) == 0:
                    continue
                
                minIndex = Grover_search(cheapest[node])

                [ w, u, v ] = cheapest[node][minIndex] 
                set1 = self.find(parent, u) 
                set2 = self.find(parent ,v) 

                if set1 != set2 : 
                    MSTweight += w 
                    self.union(parent, rank, set1, set2) 
                    print ("Edge %d-%d with weight %d included in MST" % (u,v,w)) 
                    numTrees = numTrees - 1
            
            cheapest = [] * self.V

        print ("Weight of MST is %d" % MSTweight)

def takeIntegerInput():
    s = input()
    arr = s.split(' ')
    return [int(i) for i in arr]

def solve():
    # print("Enter the number of nodes")
    # NUM_NODES = takeIntegerInput()[0]
    # g = Graph(NUM_NODES)
    # print("Enter the number of edges")
    # NUM_EDGES = takeIntegerInput()[0]
    # print("Enter 2 vertices and its weight")
    # for i in range(NUM_EDGES):
    #     arr = takeIntegerInput()
    #     g.addEdge(arr[0], arr[1], arr[2])
    print("Peterson Graph")
    NUM_NODES = 10
    g = Graph(NUM_NODES)
    g.addEdge(1, 2, 1)
    g.addEdge(2, 3, 2)
    g.addEdge(3, 4, 3)
    g.addEdge(4, 5, 4)
    g.addEdge(5, 1, 10)
    g.addEdge(6, 8, 6)
    g.addEdge(8, 0, 7)
    g.addEdge(0, 7, 8)
    g.addEdge(7, 9, 9)
    g.addEdge(9, 6, 11)
    g.addEdge(1, 7, 12)
    g.addEdge(2, 8, 13)
    g.addEdge(3, 9, 14)
    g.addEdge(4, 0, 15)
    g.addEdge(5, 6, 5)
    
    g.boruvkaMST() 

if __name__ == "__main__":
    solve()
