import board
import heapq

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

        frontier = []
        visited = []
        seen = []

        #we're using negative G here to reverse the heap 
        # THIS IS A TUPLE 
        #Because of the heap we must access the second element of the tuple
        heapq.heappush(frontier, (startnode.GetG(), startnode))
        seen.append(startnode)
        current = None

        while (current not in goals):
            current = frontier.pop()
            
            visited.append(current)


            neighbors = board.GetNeighbors(current[1].pt)

           
            for neighbor in neighbors:
                print(neighbor)
                for y in range(len(self.nodes)):
                    print("self.nodes at y:" + str(y))
                    print(self.nodes[y])
                x = neighbor[0]
                y = neighbor[1]
                
                neighbor_node = self.nodes[y][x]

                if neighbor_node not in seen:
                    neighbor_node.h = self.GetClosestGoal(neighbor, goals)

                    if (board.GetValue(neighbor) == color):
                        neighbor_node.f = current[1].f
                    else:
                        neighbor_node.f = current[1].f + 1

                    neighbor_node.parent = current[1]

                    seen.append(neighbor_node)

                    #once again G is negative to reverse heap properties
                    heap_element = (-neighbor_node.GetG(), neighbor_node)
                    print("heap element:")
                    print(heap_element)

                    heapq.heappush(frontier, heap_element)
                    print("Frontier now looks like:")
                    print(frontier)

        return self.GetPath(current)

    def GetPath(self, lastnode):
        path = []
        current = lastnode
        while (current.parent != None):
            path.append(current)
            current = current.parent
        
        path.append(current)
        return path



    def GetDist(self, p1, p2):
        return (p1[0] - p2[0])**2 + (p1[1] - p2[1])**2

    def GetClosestGoal(self, start, goals):
        dist = float('inf')
        closest = None
        for goal in goals:
            current_dist = self.GetDist(start, goal)

            if (current_dist < dist):
                dist = current_dist
                closest = goal
        return dist


class Node:
    def __init__(self, pt):
        self.pt = pt
        self.parent = None
        self.f = 0
        self.h = 0

    def __repr__(self):
        return "Node: " + str(self.pt)

    def __gt__(self, rhs):
        return self.GetG() > rhs.GetG()


    def GetG(self):
        
        return self.f + self.h