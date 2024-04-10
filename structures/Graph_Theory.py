"""

Subject:

You program will perform the following actions:
1.	Reading a constraint table from a .txt file, storing this information in memory and displaying the constraint table on screen. 
2.	Building a graph corresponding to that constraint table.
3.	Checking that this graph has no circuits and that there are no negative arcs.
4.	If all those properties are satisfied, compute the earliest date calendar, the latest date calendar, and the floats. 
When computing the latest date calendar, assume that the latest date of the end of project coincides with its earliest date. As you know, in order to compute the calendars, you must first do a topological sort of the graph, i.e. sort the vertices in the growing order of ranks. Therefore, you must find the ranks for all vertices using an algorithm of your choice among those you’ve seen in this course. 



Any constraint table of the following form (we take as an example the table C01 of the TD Appendix, and we’ve replaced the alphabetic task labels by numbers (A1, B2 etc.). On each line, the first number is the task number, the second is its duration, and the other numbers (if present) are the constraints (predecessors) : 
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

Your program must be capable of importing any constraint table constructed as described above, including the case where the corresponding graph contains cycles or is not connected, and of transforming it into a graph in a matrix form (a value matrix). 




The program
Set up a program that performs the following actions:
1.	Reading a constraint table presented in a .txt file and storing it in memory
2.	Display of the corresponding graph in a matrix form (value matrix). Warning: the display must be done from memory, not directly from reading the .txt file.
The graph must contain the two fictitious tasks  and    (labeled 0 and N+1 where N is the number of tasks). 
3.	Check the necessary properties of the graph such that it can serve as a scheduling graph
- no cycle, 
- no negative edges.

If those properties are satisfied, compute the calendars:

4.	Compute the ranks for all vertices 
5.	Compute the earliest dates, the latest dates, and the floats.
For the computation of the latest dates, assume that the latest date of the end of project coincides with its earliest date. 
6.	Compute the critical path(s) and display it or them

Your program must be capable to « loop » on the constraint tables you’ve prepared. It would be a very bad idea to stop the program and launch it again every time you want to use a different constraint table. If this is the case, it will results in points off. 

The global structure of your program can be described by the following pseudo-code: 



The global structure of your program can be described by the following pseudo-code: 

BEGIN
WHILE the user wants to test a constraint table DO 
Choose the constraint table to work with 
Read it from a file and store it in memory
Create the matrix of the graph corresponding to that constraint table, and display it 
Check the properties necessary for the graph to be a scheduling graph
IF «yes» THEN
Compute the ranks of all vertices and display them 
Compute the earliest dates calendar and the latest dates calendar and display them 
Compute the floats and display them 
Compute the critical path(s) and display it or them
ENDIF
ELSE ask the user if he wants to use another constraint table
ENDWHILE
END

It is evident that it is possible to incorporate detecting the absence/presence of a cycle and finding the ranks in one algorithm. However, you should display the ranks only in the absence of a cycle (s)

"""


class Graph:


    def __init__(self, file=""):
        self.graph = []
        self.durations = []
        self.read_graph(file)


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

    def is_acyclic(self):
        """
        Return True if the graph is acyclic.
        Return False otherwise.
        """
        visited = [False] * len(self.graph)
        stack = [False] * len(self.graph)

        def dfs(node):
            visited[node] = True
            stack[node] = True

            for neighbor in range(len(self.graph)):
                if self.graph[node][neighbor] != 0:
                    if not visited[neighbor]:
                        if dfs(neighbor):
                            return True
                    elif stack[neighbor]:
                        return True

            stack[node] = False
            return False

        for node in range(len(self.graph)):
            if not visited[node]:
                if dfs(node):
                    return False

        return True
Graps=[]
for i in range(1, 14):
    Graps.append(Graph("./TestFiles/table {}.txt".format(i)))
    print(Graps[i-1])
    print("\n\n\n")

for i in range(1, 14):
    print("Graph {} is acyclic: {}".format(i, Graps[i-1].is_acyclic()))