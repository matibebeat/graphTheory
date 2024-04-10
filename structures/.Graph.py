

##############################################################################
#
#
#                               Test File, to delete
#
##############################################################################









class Graph:


    def __init__(self, file=""):
        self.graph = []
        self.durations = []
        self.read_graph(file)
        self.ranks = {}
        self.ComputeRanks()
        
        


    def add_edge(self, u, v,w):
        self.graph[u][v] = w

    def read_graph(self, file):
        '''Any constraint table of the following form (we take as an example the table C01 of the TD Appendix, and we’ve replaced the alphabetic task labels by numbers (A1, B2 etc.). On each line, the first number is the task number, the second is its duration, and the other numbers (if present) are the constraints (predecessors) : 
1 9 
2 2 
3 3 2
4 5 1
5 2 1 4
6 2 5
7 2 4
8 4 4 5
9 5 4
10 1 2 3
11 2 1 5 6 7 8
The N tasks are numbered from 1 to N. The fictitious task   will be denoted as 0. The fictitious task   will be numbered N+1.
'''
        with open(file, 'r') as f:
            lines = f.readlines()
            length = len(lines)
            self.graph = [[0 for column in range(length)] for row in range(length)]
            self.durations = [0 for i in range(length)]
            for line in lines:
                line = line.split()
                u = int(line[0])
                self.durations[u-1] = int(line[1])
                for v in line[2:]:
                    self.add_edge(int(v)-1, u-1, int(line[1]))

    def __str__(self):
        string = "   "
        for i in range(len(self.graph)):
            string += str(i+1).zfill(2) + " "  # Use zfill(2) to pad the index with leading zeros
        for row in enumerate(self.graph):
            string += "\n" + str(row[0]+1).zfill(2) + " "  # Use zfill(2) to pad the index with leading zeros
            for column in row[1]:
                if len(str(column)) == 1:
                    string += "" + str(column) + "  "
                else:
                    string +=  str(column) + " "
        return string

    def ComputeRanks(self):
        # We will use the topological sort algorithm to fill the ranks
        visited = [False for i in range(len(self.graph))]
        stack = []
        for i in range(len(self.graph)):
            if not visited[i]:
                self.topologicalSort(i, visited, stack)
        for i in range(len(stack)):
            self.ranks[stack[i]] = i

    def topologicalSort(self, v, visited, stack):
        visited[v] = True
        for i in range(len(self.graph)):
            if self.graph[v][i] != 0 and not visited[i]:
                self.topologicalSort(i, visited, stack)
        stack.insert(0, v)
        return stack





# Path: projets_l3/graphTheory/structures/Graph.py

test = Graph("./TestFiles/table 1.txt")
Graps = []
for i in range(1, 14):
    Graps.append(Graph("./TestFiles/table {}.txt".format(i)))
    print(Graps[i-1])
    print("\n\n\n")
    print(Graps[i-1].ranks)