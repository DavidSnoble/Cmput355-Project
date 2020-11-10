from board import Board
from player import Player


class Game:
    ### Built-in Class Methods ###
    def __init__(self, board_size):
        self.board = Board(board_size)

    ### Public Methods ###
    def Start(self):
        print("1) Player vs AI\n2) AI vs AI")
        option = input(">")

        if (option == '1'):
            # self.PlayGame(None, self.b_player)
            print("WIP, please select option 2 next time")
        elif (option == '2'):
            self.PlayGame(Player(Board.WHITE), Player(Board.BLACK))
        else:
            print("option unsupported, exiting...")
        
        return

    def PlayGame(self, white_player, black_player):
        player_color = (Board.WHITE, Board.BLACK)

        players = {Board.WHITE: white_player, Board.BLACK: black_player}

        moves = 0

        outcome = (False, 0)

        while outcome[0] == False:
            color = player_color[moves % 2]

            moves += 1

            cur_player = players[color]
            
            self._DisplayTurn(self.board, color, moves)
            
            point_to_play = cur_player.PlayMove(self.board)
            self.board.ColorPoint(point_to_play, color)

            self._ReportMove(self.board, color, point_to_play)

            outcome = self.board.DetectGameEnd()

        winner = Board.Color2Text[outcome[1]]
        self._DisplayGameOver(self.board, winner)

    ### Private Methods ###
    def _DisplayTurn(self, board, color, move_num):
        print()
        print(board)
        print()
        print("Move {}".format(move_num))
        print("{} to move.".format(Board.Color2Text[color]))
        return

    def _ReportMove(self, board, color, move):
        print("{} plays {}!".format(Board.Color2Text[color], move))
        print()
        print(board)
        print()
        return
    
    def _DisplayGameOver(self, board, winner):
        print()
        print("Game over!")
        print("The winner is {}! Congrats!".format(winner))
        print()
        return

if __name__ == "__main__":
    game = Game(4)
    game.Start()