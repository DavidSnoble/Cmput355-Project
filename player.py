from board import Board

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


    ### Private Methods ###




if __name__ == "__main__":
    pass
