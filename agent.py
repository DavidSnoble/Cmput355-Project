from board import *
import AStar
#import board
import random

class Agent:
    color = "EMPTY"
    start = None
    moves_left = []
    moves_right = []
    moves_bottom = []

    pairs_left = []
    pairs_right = []
    pairs_bottom = []



    def __init__(self,color):
        self.color = color


    def PickStart(self, board):
        x = int(board.size / 4)
        y = int(board.size / 2)
        point = (x,y)

        if (board.GetValue(point) == board.EMPTY):
            return point
        else:
            return (x, y+1)

    def GetCommonNbrsBetweenPts(self, board, pt1, pt2):
        pt1_neighbors = set(board.GetNeighbors(pt1))
        pt2_neighbors = set(board.GetNeighbors(pt2))

        common_neighbors = list(pt1_neighbors & pt2_neighbors)

        for neighbor in common_neighbors:
            if board.GetValue(neighbor) not in (self.color, board.EMPTY):
                return []

        return common_neighbors


    def SeperatePathToCriticalMovesAndPairs(self, current, path, edge, board):
        print("recieved path {}".format(path))
        pairs = []
        critical_moves = path

        #if the path is only 1 or 0 moves, return what we have
        #TODO check if a pair exists between our one move and the start
        if (len(path) <= 1): 
            print("small path {}, returning".format(path))
            return critical_moves, pairs

        index = 1
        print("path: {} length {}".format(path, len(path)))
        #if the path is not currently in the goal
        print("checking goal and {} at index {}".format(path[index], index))
        if (path[index] not in edge):
            #check common neighbors between 2nd last move and goal
            common = [value for value in board.GetNeighbors(path[index]) if value in edge]
            print("common neighbors of {} and goal are {}".format(path[index], common))
            #if 2 goals exist, set them as a pair, remove the goal from critical moves, and decrement the index
            if (len(common) == 2):
                pairs.append(common)
                critical_moves.remove(path[0])
                if (len(path) == 2):
                    index = len(path) - 1
                index = index + 2
            else:
                index = index + 1


        ### Removes "Pair Points" within path so that the critical moves remain ###
        print("index before the main loop is {}".format(index))
        while (index < len(path) - 1):
            print("path is size {}, current index = {}".format(len(path) - 1, index))
            # For every point, get the common points between that and the one 2 spaces ahead
            common = self.GetCommonNbrsBetweenPts(board, path[index], path[index-2])

            # If there 2 common points, then that means they are a 'pair'
            #   We remove the critical point between the current point and the one 2 spaces ahead
            #   Append the pair of points from common
            if (common == 2):
                pairs.append(common)
                critical_moves.remove(path[index - 1])
                if (index < 2): break
                index = index + 2
            else:
                index = index + 1

        common = self.GetCommonNbrsBetweenPts(board, path[len(path) - 2], self.start)
        if(common == 2):
            pairs.append(common)
            critical_moves.remove(path[len(path) - 1])

        print("full search finished, returning {} and {}".format(critical_moves, pairs))
        return critical_moves, pairs
        


    def RdmStart(self, board):
        legal_moves = list(board.legal_moves)
        output = random.choice(legal_moves)
        return output

    def FirstTurn(self, board):
        path_finder = AStar.AStar(board)

        self.start = self.PickStart(board)
        
        #self.start = self.RdmStart(board)

        edges = board.board_edges

        path_left = path_finder.GetAStar(board, self.start, edges[0], self.color)
        path_right = path_finder.GetAStar(board, self.start, edges[1], self.color)
        path_bottom = path_finder.GetAStar(board, self.start, edges[2], self.color)


        self.moves_left, self.pairs_left = self.SeperatePathToCriticalMovesAndPairs(self.start, path_left, edges[0], board)
        self.moves_right, self.pairs_right = self.SeperatePathToCriticalMovesAndPairs(self.start, path_right, edges[1], board)
        self.moves_bottom, self.pairs_bottom = self.SeperatePathToCriticalMovesAndPairs(self.start, path_bottom, edges[2], board)

        return self.start



    def PrintLists(self):
        #this is for debugging/ getting info
        print("for {}".format(self.color))
        print("moves lists: (left, right, bottom")
        print(self.moves_left)
        print(self.moves_right)
        print(self.moves_bottom)
        print("")
        print("pair lists:")
        print(self.pairs_left)
        print(self.pairs_right)
        print(self.pairs_bottom)
        print("")



    def PlayTurn(self, board):

        path_finder = AStar.AStar(board)
        edges = board.board_edges


        #check that opponent has not interrupted our move lists
        for move in self.moves_left:
            if board.GetValue(move) != board.EMPTY:
                print("{} has been been interrupted! there is an opponent at {}".format(self.color, move))
                path = path_finder.GetAStar(board, self.start, edges[0], self.color)
                print("new path is {}".format(path))
                self.moves_left, self.pairs_left = self.SeperatePathToCriticalMovesAndPairs(self.start, path, edges[0], board)
                print("")

        for move in self.moves_right:
            if board.GetValue(move) != board.EMPTY:
                print("{} has been been interrupted! there is an opponent at {}".format(self.color, move))
                path = path_finder.GetAStar(board, self.start, edges[1], self.color)
                print("new path is {}".format(path))
                self.moves_right, self.pairs_right = self.SeperatePathToCriticalMovesAndPairs(self.start, path, edges[1], board)
                print("")

        for move in self.moves_bottom:
            if board.GetValue(move) != board.EMPTY:
                print("{} has been been interrupted! there is an opponent at {}".format(self.color, move))
                path = path_finder.GetAStar(board, self.start, edges[2], self.color)
                print("new path is {}".format(path))
                self.moves_bottom, self.pairs_bottom = self.SeperatePathToCriticalMovesAndPairs(self.start, path, edges[2], board)
                print("")


        #check that opponent has not played in our pairs
        for pair in self.pairs_left:
            if board.GetValue(pair[0]) != board.EMPTY:
                self.pairs_left.remove(pair)
                return pair[1]
            elif board.GetValue(pair[1]) != board.EMPTY:
                self.pairs_left.remove(pair)
                return pair[0]

        for pair in self.pairs_right:
            if board.GetValue(pair[0]) != board.EMPTY:
                self.pairs_right.remove(pair)
                return pair[1]
            elif board.GetValue(pair[1]) != board.EMPTY:
                self.pairs_right.remove(pair)
                return pair[0]

        for pair in self.pairs_bottom:
            if board.GetValue(pair[0]) != board.EMPTY:
                self.pairs_bottom.remove(pair)
                return pair[1]
            elif board.GetValue(pair[1]) != board.EMPTY:
                self.pairs_bottom.remove(pair)
                return pair[0]


        #all cases checked, return from move list
        if len(self.moves_left) != 0:
            return self.moves_left.pop()

        if len(self.moves_right) != 0:
            return self.moves_right.pop()

        if len(self.moves_bottom) != 0:
            return self.moves_bottom.pop()

        #all moves empty, start playing pairs
        if len(self.pairs_left) != 0:
            return self.pairs_left.pop()[0]

        if len(self.pairs_right) != 0:
            return self.pairs_right.pop()[0]

        if len(self.pairs_bottom) != 0:
            return self.pairs_bottom.pop()[0]
    


        """
        if len(self.moves_left) != 0:
            l = self.moves_left.pop()
            if board.GetValue(l) == board.EMPTY:
                return l
            else:
                for pair in self.pairs_left:
                    if board.GetValue(pair[0]) != board.EMPTY:
                        self.pairs_left.remove(pair)
                        return pair[1]
                    elif board.GetValue(pair[1]) != board.EMPTY:
                        self.pairs_left.remove(pair)
                        return pair[0]

        if len(self.moves_right) != 0:
            r = self.moves_right.pop()
            if board.GetValue(r) == board.EMPTY:
                return r
            else:
                for pair in self.pairs_right:
                    if board.GetValue(pair[0]) != board.EMPTY:
                        self.pairs_right.remove(pair)
                        return pair[1]
                    elif board.GetValue(pair[1]) != board.EMPTY:
                        self.pairs_right.remove(pair)
                        return pair[0]

        if len(self.moves_bottom) != 0:
            btm = self.moves_bottom.pop()
            if board.GetValue(btm) == board.EMPTY:
                return btm
            else:
                for pair in self.pairs_bottom:
                    if board.GetValue(pair[0]) != board.EMPTY:
                        self.pairs_bottom.remove(pair)
                        return pair[1]
                    elif board.GetValue(pair[1]) != board.EMPTY:
                        self.pairs_bottom.remove(pair)
                        return pair[0]

        #print(len(self.pairs_left))
        #print(len(self.pairs_right))
        #print(len(self.pairs_bottom))
        """

        return None
