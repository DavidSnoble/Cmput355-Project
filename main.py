import copy
import random
from board import Board
from player import Player
from game import Game

w_player = Player(Board.WHITE)
b_player = Player(Board.BLACK)

player = (w_player, b_player)

def StartGame():
    b = Board(4)

    player_index = 0
    moves = 0

    outcome = (False, 0)

    while outcome[0] == False:
        player_index = moves % 2
        cur_player = player[player_index]

        color_txt = Board.Color2Text[cur_player.color]
        print("{} to move!".format(color_txt))
        print(b)
        print("---")

        # Get the point that the current player is going to play
        pt = cur_player.PlayMove(b)
        # Color the current point
        b.ColorPoint(pt, cur_player.color)

        print("{} plays {}!".format(color_txt, pt))
        print(b)
        print(">>>")

        moves += 1

        outcome = b.DetectGameEnd()

    print("{} wins!".format(Board.Color2Text[outcome[1]]))

    return

    

# StartGame()

game = Game(11)
game.Start()