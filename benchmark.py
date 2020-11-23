import copy
import random
from board import Board
from player import Player
from game import *
import agent
import time


class Test:

    def __init__(self):
        self.white_wins = 0
        self.black_wins = 0
    
    def PlayGame(self, white_player, black_player, board):
        player_color = (Board.WHITE, Board.BLACK)

        players = {Board.WHITE: white_player, Board.BLACK: black_player}

        moves = 0

        outcome = (False, 0)
        prompt = Prompt()
        while outcome[0] == False:
            color = player_color[moves % 2]
            player_to_move = Board.Color2Text[color]
         
            moves += 1

            # Retrieve the player from the dictionary
            cur_player = players[color]
            
            
            # Display the board state for context
            
            
            # Select point to be played
            point_to_play = None
            if (cur_player.color == 2):
                point_to_play = cur_player.PlayMove(board)
                
            elif (cur_player.color == 1):
                point_to_play = cur_player.PlayMove(board)
                
            #else:
                #point_to_play = Prompt.PromptAndPlayMove(self.board, player_to_move, moves)
            
            # Color the point on the board
            board.ColorPoint(point_to_play, color)

            # Report the move
            #Prompt.ReportMove(self.board, player_to_move, point_to_play)
            #Prompt.DisplayBoardState(board, player_to_move, moves)
            outcome = board.DetectGameEnd()

        winner = Board.Color2Text[outcome[1]]
        #Prompt.DisplayGameOver(winner)
        return winner

    def run(self):
        f = open("data.csv", "a")
        start_time = time.time()
        for x in range(100):
            board_size = 19
            board = Board(board_size)
            white_p = agent.Agent(Board.WHITE)
            black_p = agent.Agent(Board.BLACK)
            
            outcome = self.PlayGame(white_p, black_p, board)
            if outcome == "W":
                self.white_wins = self.white_wins + 1
                #f.write("White Won game {}\n".format(x))
            else:
                self.black_wins = self.black_wins + 1
                #f.write("Black Won game {}\n".format(x))

        f.write("Astar vs Astar {} White wins vs {} Black wins on board size {}\n".format(self.white_wins, self.black_wins, board_size))
        f.write("run time for 100 games on board of size {} is {} seconds\n".format(board_size, time.time() - start_time))

        f.close

if __name__ == "__main__":
    test = Test()
    test.run()