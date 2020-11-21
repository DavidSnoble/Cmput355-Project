import board
import heapq
from queue import PriorityQueue
class AStar:
    nodes = []

    def __init__(self, board):
        '''
        for y in range(board.size-1):
            for x in range(y):
                print("x is " + str(x))
                print("y is " + str(y))
                self.nodes[x][y].color = board.board[x][y]
                self.nodes.pt = (x,y)
        '''
        for i in range(board.size):
            self.nodes.append([Node((x,i)) for x in range(i + 1)])
        


    def GetAStar(self, board, start, goals, color):
    
        x = start[0]
        y = start[1]

        """       
        print(x)
        print(y)
        print(self.nodes)
        print(self.nodes[x][y-1])
        """
     
        startnode = Node((x,y))
        
        startnode.h = self.GetClosestGoal(start, goals)
        
        startnode.f = 0

        frontier = PriorityQueue()
        visited = []
        seen = []

        frontier.put(startnode)
        seen.append(startnode)
        cur_node = startnode

        while (cur_node.pt not in goals and frontier.qsize() != 0):
            cur_node = frontier.get()
            if (cur_node.f == float("inf")):
                return []

            visited.append(cur_node)

            neighbors = board.GetNeighbors(cur_node.pt)

            for neighbor in neighbors:
                x = neighbor[0]
                y = neighbor[1]
                
                neighbor_node = self.nodes[y][x]

                if neighbor_node not in seen:
                    neighbor_node.h = self.GetClosestGoal(neighbor, goals)

                    if (board.GetValue(neighbor) == color):
                        neighbor_node.f = cur_node.f
                    elif (board.GetValue(neighbor) == board.EMPTY):
                        neighbor_node.f = cur_node.f + 1
                    else:
                        neighbor_node.f = float("inf")

                    neighbor_node.parent = cur_node
                    neighbor_node.direction = self.GetDirection(cur_node.pt, neighbor_node.pt)

                    if (cur_node.direction == neighbor_node.direction):
                        neighbor_node.f = neighbor_node.f + 1


                    seen.append(neighbor_node)

                    #once again G is negative to reverse heap properties
                    #heapq.heappush(frontier, (-neighbor_node.GetG(), neighbor_node))
                    frontier.put(neighbor_node)
                    #print("")
                    #print("This is the heap" + str(frontier))


        return self.GetPath(cur_node)

    def GetPath(self, lastnode):
        path = []
        current = lastnode
        while (current.parent != None):
            if (current.pt is not None):
                path.append(current.pt)
            current = current.parent
        
        #print("Path: {}".format(path))
        
        return path



    def GetDist(self, p1, p2):
        return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

    def GetClosestGoal(self, start, goals):
        dist = float('inf')
        closest = None
        for goal in goals:
            current_dist = self.GetDist(start, goal)

            if (current_dist < dist):
                dist = current_dist
                closest = goal
        
        #print("The closest goal to start is ..." + str(start))
        #print(closest)
        return dist

    def GetDirection(self, p1, p2) :
        if (p1[0] == p2[0] - 1):
            if(p1[1] == p2[1] - 1):
                return "NW"
            if(p1[1] == p2[1]):
                return "W"
            else:
                return "SW"

        if (p1[0] == p2[0] + 1):
            if(p1[1] == p2[1] + 1):
                return "NE"
            if(p1[1] == p2[1]):
                return "E"
            else:
                return "SE"


class Node:
    def __init__(self, pt):
        self.pt = pt
        self.parent = None
        self.direction = None
        self.f = 0
        self.h = 0

    def __repr__(self):
        return "Node<{} : {}>".format(self.pt, self.GetG())

    def __gt__(self, rhs):
        return self.GetG() > rhs.GetG()


    def GetG(self):
        
        return self.f + self.h