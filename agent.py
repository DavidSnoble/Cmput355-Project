from board import *
import AStar
#import board

class Agent:
    color = "EMPTY"
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
        #Path is just the goal so return path and possibly a pair(if applicable)
        if(len(path) == 1):
            common = [value for value in board.GetNeighbors(current) if value in edge]
            if len(common) == 1:
                common = []
            return path, common

        pairs = []
        moves = []

        index = len(path) - 1

        #check if the goal possibly has a pair in it
        second_tile_neighbors = set(board.GetNeighbors(path[index - 1].pt))
        edge_set = set(edge)
        common_goals = second_tile_neighbors & edge_set
        common_goals = list(common_goals)
        if (len(common_goals) == 2):
            pairs.append(common_goals)

            if index > 1:
                index = index - 2
            else:
                moves.append(path[index - 1].pt)


        while (index >= 1):

            #TEMP STATEMENT
            #TODO: check if we exist as a pair between the second move in the path and our first move
            if index == 1:
                moves.append(path[index].pt)
                break

            #check that neighbors don't exist between us and the 2nd step in the path
            common_neighbors = self.GetCommonNbrsBetweenPts(board, path[index].pt, path[index - 2].pt)
            if len(common_neighbors) == 2:
                if common_neighbors not in pairs:
                    moves.append(path[index].pt)
                    pairs.append(common_neighbors)
                    index = index - 2
                    continue

            #check that we don't exist as a pair between the path
            common_neighbors = self.GetCommonNbrsBetweenPts(board, path[index + 1].pt, path[index - 1].pt)
            if len(common_neighbors) == 2:
                if common_neighbors not in pairs:
                    pairs.append(common_neighbors)
                    index = index - 1

            moves.append(path[index].pt)
        
        moves.append(path[0].pt)


            
                

        #This does not work
        '''
        # If there is only one neighbour between two points then increases the index's
        if(len(common) == 1):
            first_index = first_index + 1
            second_index = second_index + 1

        # While not at the end of the path add moves to list and pairs to list
        while(second_index < len(path)):
            # common = (board.GetNeighbours(path[first_index]).union(board.GetNeighbours(path[second_index])))
            # NOTE: THIS IS HENRY'S CHANGE: I HAVE MADE A NEW FUNCTION CALLED GET COMMON NEIGHBORS BETWEEN POINTS
            common = self.GetCommonNbrsBetweenPts(board, path[first_index].pt, path[second_index].pt)
            print("common points between {} and {} are {}".format(path[first_index], path[second_index], common))
            pairs.append(list(common))
            
            moves.append(path[first_index])

            first_index = first_index + 2
            second_index = second_index + 2

        moves.append(path[first_index])
        '''

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

        return moves, pairs



    def FirstTurn(self, board):
        path_finder = AStar.AStar(board)

        start = self.PickStart(board)

        edges = board.board_edges

        path_left = path_finder.GetAStar(board, start, edges[0], self.color)
        path_right = path_finder.GetAStar(board, start, edges[1], self.color)
        path_bottom = path_finder.GetAStar(board, start, edges[2], self.color)

        
        self.moves_left, self.pairs_left = self.MovesFromPath(start, path_left, edges[0], board)
        self.moves_right, self.pairs_right = self.MovesFromPath(start, path_right, edges[1], board)
        self.moves_bottom, self.pairs_bottom = self.MovesFromPath(start, path_bottom, edges[2], board)
        

        return start



    def PrintLists(self):
        #this is for debugging/ getting info
        print("moves lists: (left, right, bottom")
        print(self.moves_left)
        print(self.moves_right)
        print(self.moves_bottom)
        print("pair lists:")
        print(self.pairs_left)
        print(self.pairs_right)
        print(self.pairs_bottom)

    

    def PlayTurn(self, board):
        print("called playturn")
        pairs = []
        pairs.append(self.pairs_left) 
        pairs.append(self.pairs_right) 
        pairs.append(self.pairs_bottom)
        pairs = list(pairs) 

        for pair in self.pairs_left:
            print("pairs left:")
            print(self.pairs_left)

            if board.GetValue(pair[0]) != Board.EMPTY:
                self.pairs_left.remove(pair)
                return pair[1]
            elif board.GetValue(pair[1]) != Board.EMPTY:
                self.pairs_left.remove(pair)
                return pair[0]

        
        if len(self.moves_left) != 0:
            return self.moves_left.pop()

        if len(self.moves_right) != 0:
            return self.moves_right.pop()

        if len(self.moves_bottom) != 0:
            return self.moves_bottom.pop()

        
        if len(self.pairs_left) != 0:
            pair = self.pairs_left.pop()
            return pair[0]

        '''
        if len(self.pairs_right) != 0:
            return self.pairs_right.pop()[0]

        if len(self.pairs_bottom) != 0:
            return self.pairs_bottom.pop()[0]
        '''

        return None

