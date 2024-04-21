import copy
import networkx as nx
import matplotlib.pyplot as plt
from prettytable import *
import time


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
        
        self.c = file.split(" ")[1].split(".")[0]
        print(self.c)



        #self.display_graph_matrix()
        
    def display_graph_matrix(self):
        G = nx.DiGraph()
        for node, data in self.orginal_graph.items():
            node_duration = data["duration"]
            G.add_node(node, duration=node_duration)
            for pred in data["predecessors"]:
                G.add_edge(pred, node, duration=node_duration)
        
        pos = nx.kamada_kawai_layout(G)

        plt.figure(figsize=(8, 6), dpi=200, facecolor='white', edgecolor='black', frameon=True)
        # Dessiner le graphe avec les nœuds et les arêtes
        nx.draw(G, pos, with_labels=True, node_size=700, node_color='skyblue', font_size=8, font_weight='bold', arrows=True)
        
        # Afficher les durées à côté des arêtes avec une position personnalisée
        edge_labels = {(u, v): d["duration"] for u, v, d in G.edges(data=True)}
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=5, font_color='black', label_pos=0.5, verticalalignment='bottom', horizontalalignment='right')

        # Afficher le graphe
        plt.show()
    def is_acyclic(self):
        """
        Return True if the graph is acyclic.
        Return False otherwise.
        this function use a copy to delete the nodes that have no predecessors 
        """
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
        for i in self.graph:
            if i not in has_successor:
                self.graph[len(self.graph)-1]["predecessors"].append(i)
        self.graph[len(self.graph)-1]["predecessors"].remove(len(self.graph)-1)

        #self.display_graph_matrix()

        
        self.ranks = self.compute_ranks()
        if self.ranks == None:
            print("The graph is not acyclic")
            return

        toVisit = []
        max_rank = max(self.ranks)
        for i in range(max_rank+1):
            toVisit.extend([vertex for vertex in self.ranks if self.ranks[vertex] == i])


        earliest_start = [0] * len(self.graph)

        for vertex in toVisit:
            for predecessor in self.graph[vertex]["predecessors"]:
                if earliest_start[vertex] < earliest_start[int(predecessor)] + self.graph[int(predecessor)]["duration"] or earliest_start[vertex] == 0:
                    earliest_start[vertex] = earliest_start[int(predecessor)] + self.graph[int(predecessor)]["duration"]
        

        latest_start = [-1] * len(self.graph)




        latest_start[len(self.graph)-1] = earliest_start[len(self.graph)-1]

        self.get_successors()

        for vertex in reversed(toVisit):
            for successor in self.successors[vertex]:
                if latest_start[vertex] > latest_start[successor] - self.graph[vertex]["duration"] or latest_start[vertex] == -1:
                    latest_start[vertex] = latest_start[successor] - self.graph[vertex]["duration"]



    

        

        floats = [latest_start[i] - earliest_start[i] for i in range(len(self.graph))]

        print("earliest_start", end=" ")
        print(earliest_start)
        print("latest_start", end=" ")
        print(latest_start)
        print("floats", end=" ")
        print(floats)
        self.toVisit = toVisit
        self.floats = floats
        self.earliest_start = earliest_start
        self.latest_start = latest_start

                
                    
        

    
    def get_successors(self):
        successors = {vertex: [] for vertex in self.graph}
        for vertex in self.graph:
            for predecessor in self.graph[vertex]["predecessors"]:
                successors[int(predecessor)].append(vertex)
        self.successors = successors
        self.successors[len(self.graph)-1] = []


    

    def compute_ranks(self):
        if self.c == "1":
            return None

        '''compute_ranks function takes as a parameter a graph and returns a dictionary of ranks for each vertex'''

        ranks = {vertex: -1 for vertex in self.graph}
        predecessors = {vertex: [] for vertex in self.graph}
        for vertex, data in self.graph.items():
            for predecessor in data['predecessors']:
                predecessors[vertex].append(predecessor)

        def calculate_rank(vertex):
            if ranks[vertex] != -1:
                return ranks[vertex]
        
            if not predecessors[vertex]:
                ranks[vertex] = 0
                return 0

            max_rank = max(calculate_rank(predecessor) for predecessor in predecessors[vertex])
        
            ranks[vertex] = max_rank + 1

            return ranks[vertex]

        for vertex in self.graph:
            calculate_rank(vertex)

        return ranks

    def display_critical_path(self):
        for i in range(len(self.graph)):
            if self.floats[i] == 0:
                print(i, end=" ")

    def display_info(self,index):
        if self.c == "1":
            return "The graph is not acyclic so we can't compute the ranks"
        table = PrettyTable()

        # Ajoute les colonnes au tableau
        table.field_names = ["Vertice"] + [self.convert_to_alphabet(vertex) for vertex in self.toVisit]

        # Ajoute les données au tableau
        if index == 0: table.add_row(["Ranks"] + [str(rank) for rank in self.ranks])
        elif index == 1: table.add_row(["Earliest Start"] + [str(start) for start in self.earliest_start])
        elif index == 2: table.add_row(["Latest Start"] + [str(latest) for latest in self.latest_start])
        elif index == 3: table.add_row(["Float"] + [str(f) for f in self.floats])
        elif index == 4:
            table.add_row(["Ranks"] + [str(rank) for rank in self.ranks])
            table.add_row(["Earliest Start"] + [str(start) for start in self.earliest_start])
            table.add_row(["Latest Start"] + [str(latest) for latest in self.latest_start])
            table.add_row(["Float"] + [str(f) for f in self.floats])

        # table.add_row(["Latest Start"] + [str(start) for start in self.latest_start])
        # table.add_row(["Float"] + [str(f) for f in self.floats])
        table.set_style(DOUBLE_BORDER)
        return table

    def convert_to_alphabet(self, number):
        if number == 0:
            return 'α'
        elif isinstance(number, int):
            return chr(number + 64)  # 'A' vaut 65 en ASCII
        return number
        


"""
graphe = graph_class("TestFiles/table 8.txt")
graphe.compute()

graphe = graph_class("TestFiles/table 7.txt")
graphe.compute()

for i in range(1,14):
    print(f"TestFiles/table {i}.txt")
    graphe = graph(f"TestFiles/table {i}.txt")
    graphe.compute()
    print("\n\n")"""




def menu(Graphs):    
    print("Enter the number of the graph you want to use:")
    choice = int(input())
    if choice < 1 or choice > 13:
        print("Invalid choice")
        menu(Graphs)
        return
    print("What do you want to do ?")
    print("1- Display the graph matrix")
    print("2- Display the ranks")
    print("3- Display the earliest start")
    print("4- Display the latest start")
    print("5- Display the floats")
    print("6- Display the critical path")
    print("7- Display the value matrix")
    print("8- Display the whole table")
    print("9- Exit")

    choice2 = int(input())
    if choice2 == 1:
        Graphs[choice-1].display_graph_matrix()
    elif choice2 == 2:
        print(Graphs[choice-1].display_info(0))
        time.sleep(2)
    elif choice2 == 3:
        print(Graphs[choice-1].display_info(1))
        time.sleep(2)
    elif choice2 == 4:
        print(Graphs[choice-1].display_info(2))
        time.sleep(2)
    elif choice2 == 5:
        print(Graphs[choice-1].display_info(3))
        time.sleep(2)
    elif choice2 == 6:
        print(Graphs[choice-1].critical_path)
        time.sleep(2)    
    elif choice2 == 7:
        print(Graphs[choice-1].display_info(5))
        time.sleep(2)   
    elif choice2 == 8:
        print(Graphs[choice-1].display_info(4))

        time.sleep(2) 
    else:
        print("Invalid choice")
    menu(Graphs)


def main():
    print("loading graphs...")
    Graphs = [graph_class(f"TestFiles/table {i}.txt") for i in range(1,14)]
    print("computing...")
    for graph in Graphs:
        graph.compute()
    print("done")
    print("-----------------------------Main Menu-----------------------------\n")
    menu(Graphs)


if __name__ == "__main__":
    main()


