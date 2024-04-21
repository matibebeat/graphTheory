import copy

class graph_class:
    def __init__(self, file=""):
        self.graph = {}
        self.orginal_graph = {}
        with open(file, "r") as f:
            for i, line in enumerate(f):
                line = line.split()
                vrai_i = i + 1


                self.graph[vrai_i] = {"duration": int(line[1]), "predecessors": line[2:]}
        for i in self.graph:
            self.graph[i]["predecessors"] = [int(i) for i in self.graph[i]["predecessors"]]
        self.orginal_graph = copy.deepcopy(self.graph)

        self.display_graph_matrix()
        
    def display_graph_matrix(self):
        matrix = [ ["*" for _ in range(len(self.orginal_graph))] for _ in range(len(self.orginal_graph))]
        for i in self.orginal_graph:
            for j in self.orginal_graph[i]["predecessors"]:
                if int(j) < len(matrix) and i < len(matrix[int(j)]):
                    matrix[int(j)][i] = self.orginal_graph[i]["duration"]
        for i in range(len(matrix)):
            print(matrix[i])

    def is_acyclic(self):
        """
        Return True if the graph is acyclic.
        Return False otherwise.
        this function use a copy to delete the nodes that have no predecessors 
        """
        print(self.orginal_graph)
        matrix = [ [None for _ in range(len(self.orginal_graph))] for _ in range(len(self.orginal_graph))]
        for i in self.orginal_graph:
            for j in self.orginal_graph[i]["predecessors"]:
                if int(j) < len(matrix) and i < len(matrix[int(j)]):
                    matrix[int(j)][i] = self.orginal_graph[i]["duration"]


        visited = [False] * len(matrix)
        stack = [False] * len(matrix)
        def dfs(node):
            visited[node] = True
            stack[node] = True

            for neighbor in range(len(matrix)):
                if matrix[node][neighbor] != None:
                    if not visited[neighbor]:
                        if dfs(neighbor):
                            return True
                    elif stack[neighbor]:
                        return True

            stack[node] = False
            return False

        for node in range(len(matrix)):
            if not visited[node]:
                if dfs(node):
                    return False

        return True

    def has_negative_edges(self):
        for i in self.graph:
            for j in self.graph[i]["predecessors"]:
                if self.graph[j]["duration"] < 0:
                    return True
        return False
        


        

        
                
    def __str__(self):
        return str(self.graph)
    
    def compute(self):

        #check if the graph has negative edges
        if self.has_negative_edges():
            print("The graph has negative edges")
            return
        
        #check if the graph is acyclic
        if not self.is_acyclic():
            print("The graph is not acyclic")
            return
        
        #create a node nammed 0 with no predecessors and a duration of 0 
        self.graph[0] = {"duration": 0, "predecessors": []}
        #the node 0 is the only node that has no predecessors so we add 0 as predecessor to all the nodes that have no predecessors ! except 0
        for i in self.graph:
            if self.graph[i]["predecessors"] == [] and i != 0:
                self.graph[i]["predecessors"].append(0)
        self.graph[len(self.graph)] = {"duration": 0, "predecessors": []}
        has_successor = []
        for i in self.graph:
            if self.graph[i]["predecessors"] != []:
                has_successor.extend(self.graph[i]["predecessors"])
        print(has_successor)
        for i in self.graph:
            if i not in has_successor:
                self.graph[len(self.graph)-1]["predecessors"].append(i)
        self.display_graph_matrix()

        
        self.ranks = self.compute_ranks()

        print(self.ranks)

        toVisit = []
        max_rank = max(self.ranks)
        for i in range(max_rank+1):
            for index, value in enumerate(self.ranks):
                if value == i:
                    toVisit.append(index)
        print("toVisit", end=" ")
        print(toVisit)

        earliest_start = [0] * len(self.graph)

        for vertex in toVisit:
            for predecessor in self.graph[vertex]["predecessors"]:
                if earliest_start[vertex] < earliest_start[int(predecessor)] + self.graph[int(predecessor)]["duration"] or earliest_start[vertex] == 0:
                    earliest_start[vertex] = earliest_start[int(predecessor)] + self.graph[int(predecessor)]["duration"]
        print("earliest_start", end=" ")
        print(earliest_start)

        latest_start = [-1] * len(self.graph)

        latest_start[len(self.graph)-1] = earliest_start[len(self.graph)-1]

        for vertex in reversed(toVisit):
            for successor in self.successors[vertex]:
                if latest_start[vertex] > latest_start[successor] - self.graph[vertex]["duration"] or latest_start[vertex] == -1:
                    latest_start[vertex] = latest_start[successor] - self.graph[vertex]["duration"]
        print("latest_start", end=" ")
        print(latest_start)

        floats = [latest_start[i] - earliest_start[i] for i in range(len(self.graph))]

        print("floats", end=" ")
        print(floats)

                
                    
        

    
    def get_successors(self):
        successors = {vertex: [] for vertex in self.graph}
        for vertex in self.graph:
            for predecessor in self.graph[vertex]["predecessors"]:
                successors[int(predecessor)].append(vertex)
        self.successors = successors


    def compute_ranks(self):
        '''compute_ranks function takes as a parameter a graph and returns a dictionary of ranks for each vertex'''
        ranks = [-1] * len(self.graph)
        self.get_successors()
        
        #use dfs to compute the ranks
        def dfs(vertex, rank):
            if ranks[vertex] != -1:
                return
            ranks[vertex] = rank
            for successor in self.successors[vertex]:
                dfs(successor, rank + 1)
        dfs(0, 0)
        return ranks


graphe = graph_class("TestFiles/table 8.txt")
graphe.compute()

"""
graphe = graph_class("TestFiles/table 7.txt")
graphe.compute()

for i in range(1,14):
    print(f"TestFiles/table {i}.txt")
    graphe = graph(f"TestFiles/table {i}.txt")
    graphe.compute()
    print("\n\n")"""






def main():
    print("loading graphs...")
    Graphs = [graph_class(f"TestFiles/table {i}.txt") for i in range(1,14)]
    print("computing...")
    for graph in Graphs:
        graph.compute()
    print("done")
    print("-----------------------------Main Menu-----------------------------\n")
    print("Enter the number of the graph you want to use:")
    choice = int(input())
    print("What do you want to do ?")
    print("1- Display the graph matrix")
    print("2- Display the ranks")
    print("3- Display the earliest start")
    print("4- Display the latest start")
    print("5- Display the floats")
    choice2 = int(input())
    if choice2 == 1:
        Graphs[choice-1].display_graph_matrix()
    elif choice2 == 2:
        print(Graphs[choice-1].ranks)
    elif choice2 == 3:
        print(Graphs[choice-1].earliest_start)
    elif choice2 == 4:
        print(Graphs[choice-1].latest_start)
    elif choice2 == 5:
        print(Graphs[choice-1].floats)
    else:
        print("Invalid choice")
"""
if __name__ == "__main__":
    main()
"""

results = []
for i in range(1,15):
    graphe = graph_class(f"TestFiles/table {i}.txt")
    graphe.compute()
    results.append(graphe.is_acyclic())
    print("\n\n")

print(results)
graph_class("TestFiles/table 1.txt").is_acyclic()




graphe = graph_class("TestFiles/table 2.txt")
graphe.compute()