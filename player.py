from board import Board
from agent import Agent

import random

class RandPlayerUtils:
    def PlayMove(player, board):
        legal_moves = list(board.legal_moves)
        output = random.choice(legal_moves)
        return output


class Player:
    ### Built-in Class Methods ###
    def __init__(self, color):
        self.color = color
        pass

    ### Public Methods ###
    def PlayMove(self, b):
        pt = RandPlayerUtils.PlayMove(self, b)
        return pt

    def Evaluate(self, b):
        (is_end, winner_color) = b.DetectGameEnd()

        score = 0

        if (is_end):
            if (winner_color == self.color):
                score = 1
            else:
                score = 0
        else:
            score = 0.5

        return score
    '''
    def minimax(self, curr_position, b, end_node_depth, maximizing_player):
        # tutorial from https://www.youtube.com/watch?v=l-hh51ncgDI&ab_channel=SebastianLague

        # current player looks to maximize (temp heuristic -> see if win)
        # opponent looks to minimize
        # need to perform static heuristic to get last node values
        if end_node_depth == 0 or self.Evaluate(b) == 1:
            # perform heuristic on position
            #(left, right, bottom) = b.board_edges
            #print(left)
            #print(right)
            #print(bottom)

            # calculate heuristic here
            #return heuristic
            return 0

        # get the list of legal moves after current move has been played
        legal_moves = list(b.legal_moves)

        if maximizing_player:
            # current player
            maxVal = -99999
            for move in legal_moves:
                # call minimax on child node, one up from final checked node
                # set maximizing_player to false, as this is opponent's turn
                # and is looking to minimize
                cur_val = self.minimax(move, b, end_node_depth - 1, False)
                maxVal = max(maxVal, val)
            return maxVal
        else:
            # opponent
            minVal = 99999
            for move in legal_moves:
                cur_val = self.minimax(move, b, end_node_depth - 1, True)
                minVal = min(minVal, val)
            return minVal
'''
    ### Private Methods ###




if __name__ == "__main__":
    b = Board(4)



    w_player = Agent(b.WHITE)
    b_player = Player(b.BLACK)


    w_move = w_player.FirstTurn(b)
    #b_move = RandPlayerUtils.PlayMove(b_player, b)

    while(self.Evaluate(b) == 0.5):
        w_move = w_player.PlayTurn(b)
        #b_move = RandPlayerUtils.PlayMove(b_player, b)
        

    #w_move = RandPlayerUtils.PlayMove(w_player, b)
    #b_move = RandPlayerUtils.PlayMove(b_player, b)
    #print(w_move)
    #print(b_move)

    
    pass
