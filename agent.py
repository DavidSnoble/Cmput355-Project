from board import *
import AStar
#import board
import random
import math

class Agent:
    # color = "EMPTY"
    # start = None
    # moves_played = 0

    # moves_list = [[],[],[]]

    # moves_left = []
    # moves_right = []
    # moves_bottom = []

    # pairs_list = [[],[],[]]
    # pairs_left = []
    # pairs_right = []
    # pairs_bottom = []



    def __init__(self,color):
        self.color = color
        self.start = None
        self.moves_played = 0

        self.moves_list = [[],[],[]]

        self.pairs_list = [[],[],[]]


    def PickStart(self, board):
        x = int(board.size / 4)
        y = min(int((board.size + 1) / 2), board.size - 1)
        point = (x,y)

        if (board.GetValue(point) == board.EMPTY):
            return point
        else:
            return random.choice(board.GetNeighbors(point))

    def GetCommonNbrsBetweenPts(self, board, pt1, pt2):
        pt1_neighbors = set(board.GetNeighbors(pt1))
        pt2_neighbors = set(board.GetNeighbors(pt2))

        common_neighbors = list(pt1_neighbors & pt2_neighbors)

        for neighbor in common_neighbors:
            if board.GetValue(neighbor) not in (self.color, board.EMPTY):
                return []

        return common_neighbors


    def SeperatePathToCriticalMovesAndPairs(self, current, path, edge, board):
        pairs = []
        critical_moves = list(path)

        #if the path is only 1 or 0 moves, return what we have
        #TODO check if a pair exists between our one move and the start
        if (len(path) <= 1): 
            return critical_moves, pairs

        index = 1
        #if the path is not currently in the goal
        #print("checking goal and {} at index {}".format(path[index], index))
        if (path[index] not in edge):
            #check common neighbors between 2nd last move and goal
            common = [value for value in board.GetNeighbors(path[index]) if value in edge]
            #print("common neighbors of {} and goal are {}".format(path[index], common))
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
        while (index <= len(path) - 1):
            # For every point, get the common points between that and the one 2 spaces ahead
            common = self.GetCommonNbrsBetweenPts(board, path[index], path[index-2])
            #print("common points between {} and {} are {}".format(path[index], path[index - 2], common))

            # If there 2 common points, then that means they are a 'pair'
            #   We remove the critical point between the current point and the one 2 spaces ahead
            #   Append the pair of points from common

            if (len(common) == 2):
                pairs.append(common)
                critical_moves.remove(path[index - 1])
                if (index == len(path) - 1): return critical_moves, pairs
                index = index + 2
            else:
                index = index + 1

        common = self.GetCommonNbrsBetweenPts(board, path[len(path) - 2], self.start)
        if(len(common) == 2):
            pairs.append(common)
            critical_moves.remove(path[len(path) - 1])

        return critical_moves, pairs
        


    def RdmMove(self, board):
        legal_moves = list(board.legal_moves)
        output = random.choice(legal_moves)
        return output

    def FirstTurn(self, board):
        path_finder = AStar.AStar(board)

        self.start = self.PickStart(board)
        
        #self.start = self.RdmStart(board)

        edges = board.board_edges
        

        for x in range(3):
            path = path_finder.GetAStar(board, self.start, edges[x], self.color)
            self.moves_list[x], self.pairs_list[x] = self.SeperatePathToCriticalMovesAndPairs(self.start, path, edges[x], board)
            path = None
        self.PrintLists()
        
        return self.start



    def PrintLists(self):
        '''
        print("start point is :{}".format(self.start))
        for x in range(len(self.moves_list)):
            print("Moves and pairs list {}".format(x))
            print(self.moves_list[x])
            print(self.pairs_list[x])
            print("")
        '''

    def PlayTurn(self, board):
        path_finder = AStar.AStar(board)
        edges = board.board_edges

        #first check if we have been interrupted in our moves
        for x in range(3):
            moves = self.moves_list[x]
            for move in moves:
                if board.GetValue(move) != board.EMPTY:
                    self.PrintLists()
                    path = path_finder.GetAStar(board, self.start, edges[x], self.color)
                    self.moves_list[x], self.pairs_list[x] = self.SeperatePathToCriticalMovesAndPairs(self.start, path, edges[x], board)
                    print("")

        #then check if any of our pairs have been filled
        for x in range(3):
            pairs = self.pairs_list[x]
            for pair in pairs:
                if board.GetValue(pair[0]) != board.EMPTY:
                    pairs.remove(pair)
                    return pair[1]
                elif board.GetValue(pair[1]) != board.EMPTY:
                    pairs.remove(pair)
                    return pair[0]


        #play from move list
        for moves in self.moves_list:
            if len(moves) != 0:
                return moves.pop()

        #if move list is empty, play from pairs
        for pairs in self.pairs_list:
            if len(pairs) != 0:
                return pairs.pop()[0]

        #if we still don't have anything for some reason, something is wrong, however, we can return a random move
        return self.RdmMove(board)

    def PlayMove(self, board):
        move = None
        if (self.moves_played == 0):
            move = self.FirstTurn(board)
        else:
            move = self.PlayTurn(board)

        self.moves_played += 1
        return move

