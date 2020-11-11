import board
import heapq

class AStar:
    nodes = []

    def __init__(self, board):
        for x in range(board.size):
            for y in range(x):
                self.nodes[x][y].color = board.board[x][y]
                self.nodes.pt = (x,y)



    def AStar(self, board, start, goals, color):
        startnode = self.nodes[start[0]][start[1]]
        startnode.h = self.GetClosestGoal(start, goals)
        startnode.f = 0

        frontier = []
        visited = []
        seen = []

        #we're using negative G here to reverse the heap
        heapq.heappush(frontier, (-startnode.GetG, startnode))
        seen.append(startnode)
        current = None

        while (current not in goals):
            current = frontier.pop()
            visited.append(current)

            neighbors = board.GetNeighbors(current)
            for neighbor in neighbors:
                neighbor_node = self.nodes[neighbor[0]][neighbor[1]]

                if neighbor_node not in seen:
                    neighbor_node.h = self.GetClosestGoal(neighbor, goals)

                    if (board.GetValue(neighbor) == color):
                        neighbor_node.f = current.f
                    else:
                        neighbor_node.f = current.f + 1

                    neighbor_node.parent = current

                    seen.append(neighbor_node)
                    frontier.append(neighbor_node)

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
        return closest


class Node:
    pt = None

    parent = None

    f = 0
    h = 0

    def GetG(self):
        return self.f + self.h