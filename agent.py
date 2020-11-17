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

    def MovesFromPath(self, current, path, edge, board):

        pairs = []
        moves = []
        
        print(len(path))
        if(len(path) == 0):
            return moves, pairs
        if(len(path) == 1):
            moves.append(path[0])
            return moves, pairs

        index = len(path) - 2
    
        common = [value for value in board.GetNeighbors(path[index]) if value in edge]

        if(len(common) == 2):
            pairs.append(common)
            path[index + 1] = None
        

        if(index > 1):
            index = index - 2
        elif(index == 1):
            index = index - 1
        else:
            moves.append(path[index])
            return moves, pairs

        while(index > 0):
            common = self.GetCommonNbrsBetweenPts(board, path[index], path[index + 2])
            if(common == 2):
                pairs.append(common)
                path[index + 1] = None
                index = index - 2
            else:
                index = index - 1
        
        common = self.GetCommonNbrsBetweenPts(board, path[index+1], self.start)
        if(common == 2):
            pairs.append(common)
            path[index] = None
        
        for move in path:
            if(move != None):
                moves.append(move)
                

        return moves, pairs
        

            
        #print("this is our starting index: {}".format(index))
        #print("our current path is {}".format(path))

        # get all the pairs
        

        """
        while(index > 1):
            if (board.GetValue(path[index].pt) == self.color):
                index = index - 1
                continue

            common_neighbors = self.GetCommonNbrsBetweenPts(board, path[index].pt, path[index - 2].pt)
            #print("index {} and index {}'s common neighbours={}".format(index, index - 1, common_neighbors))
            #pairs.append(common_neighbors)
            if (len(common_neighbors) == 2):
                pairs.append(common_neighbors)
                path.remove(path[index])
                index = index - 1
            index = index - 1

        index = len(path) - 1

        while(index >= 0):
            #print("path is {}".format(path[index].pt))
            #print(board.GetValue(path[index].pt))
            #print(self.color)
            #print(board.EMPTY)
            # if the spot is empty place the move
            if (board.GetValue(path[index].pt) == board.EMPTY):
                moves.append(path[index].pt)

            index = index - 1


        if False:
        ### DEBUG FUNCTION ###
            print("DEBUG STATEMENT: BLACK represents MOVES, and WHITE represents PAIRS")
            print()
            board_clone = board.Clone()

            for move_node in moves:
                pt = move_node.pt
                board_clone.ColorPoint(pt, Board.BLACK)

            for pair_node in pairs:
                for pt in pair_node:
                    board_clone.ColorPoint(pt, Board.WHITE)

            print(board_clone)
            print()
        """
        


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


        self.moves_left, self.pairs_left = self.MovesFromPath(self.start, path_left, edges[0], board)
        self.moves_right, self.pairs_right = self.MovesFromPath(self.start, path_right, edges[1], board)
        self.moves_bottom, self.pairs_bottom = self.MovesFromPath(self.start, path_bottom, edges[2], board)

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
                self.moves_left, self.pairs_left = self.MovesFromPath(self.start, path, edges[0], board)
                print("")

        for move in self.moves_right:
            if board.GetValue(move) != board.EMPTY:
                print("{} has been been interrupted! there is an opponent at {}".format(self.color, move))
                path = path_finder.GetAStar(board, self.start, edges[1], self.color)
                print("new path is {}".format(path))
                self.moves_right, self.pairs_right = self.MovesFromPath(self.start, path, edges[1], board)
                print("")

        for move in self.moves_bottom:
            if board.GetValue(move) != board.EMPTY:
                print("{} has been been interrupted! there is an opponent at {}".format(self.color, move))
                path = path_finder.GetAStar(board, self.start, edges[2], self.color)
                print("new path is {}".format(path))
                self.moves_bottom, self.pairs_bottom = self.MovesFromPath(self.start, path, edges[2], board)
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
