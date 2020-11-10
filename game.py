import re

from board import Board
from player import Player


class Prompt:
    def DisplayBoardState(board, player_to_move, move_num):
        print("\n{}\n".format(board))
        print("Move number: {}".format(move_num))
        print("It is now {}'s turn:".format(player_to_move))
        return

    def ReportMove(board, player_to_move, move):
        print("{} plays {}".format(player_to_move, move))
        print("This is the result:")
        print("\n{}\n".format(board))
        return

    def PromptAndPlayMove(board, player_to_move, move_num):
        context = "Playing as {}:".format(player_to_move)
        instructions = "Please input your move (2 numbers seperated by spaces)"
        example = "Example: \'0 2\' to play on the left-most tile on row 2"

        prompt = "{}\n{}\n{}".format(context, instructions, example)

        point = None
        while (point is None) and len(board.legal_moves) != 0:
            point = Prompt.OptionPointPrompt(prompt, board)
            if (point is None):
                Prompt.DisplayBoardState(board, player_to_move, move_num)
                print("\n{}\n".format("Invalid input: Please try again."))
        
        return point

    def OptionListPrompt(prompt_text, options, q_option="Back"):
        print(prompt_text)
        for i in range(len(options)):
            print("{}) {}".format(i + 1, options[i]))
        print("q) {}".format(q_option))
        user_input = input("> ").strip().lower()

        if user_input == 'q':
            return 0
        
        if not user_input.isnumeric():
            return -1

        selection = int(user_input)
        if (selection > len(options)) or (selection <= 0):
            return -1

        return selection

    def OptionPointPrompt(prompt_text, board):
        print(prompt_text)
        user_input = input("> ").strip().lower()
        
        nums = re.findall(r'\d+', user_input)

        if len(nums) != 2:
            print("Invalid input!")
            return None
        
        legal_moves = board.legal_moves

        pt = (int(nums[0]), int(nums[1]))
        
        print(pt)
        print(legal_moves)

        if not (pt in legal_moves):
            print("Move is not legal!")
            return None

        return pt

    def ShowBanner():
        text = [' /$$     /$$                      /$$$$$$                                   ',
                '|  $$   /$$/                     /$$__  $$                                  ',
                ' \  $$ /$$/                     | $$  \__/  /$$$$$$  /$$$$$$/$$$$   /$$$$$$ ',
                '  \  $$$$/         /$$$$$$      | $$ /$$$$ |____  $$| $$_  $$_  $$ /$$__  $$',
                '   \  $$/         |______/      | $$|_  $$  /$$$$$$$| $$ \ $$ \ $$| $$$$$$$$',
                '    | $$                        | $$  \ $$ /$$__  $$| $$ | $$ | $$| $$_____/',
                '    | $$                        |  $$$$$$/|  $$$$$$$| $$ | $$ | $$|  $$$$$$$',
                '    |__/                         \______/  \_______/|__/ |__/ |__/ \_______/']

        print('\n'.join(text))
        return

    def WelcomePrompt():
        prompt_text = "Welcome to Y - Game! Please select an option:"

        options = [
            "Player vs AI",
            "AI vs AI"
        ]

        q_option = "Quit"

        user_input = -2
        while (user_input < 0):
            user_input = Prompt.OptionListPrompt(prompt_text, options, q_option)

        return user_input


class Game:
    ### Built-in Class Methods ###
    def __init__(self, board_size):
        self.board = Board(board_size)

    ### Public Methods ###
    def Start(self):
        Prompt.ShowBanner()
        u_input = Prompt.WelcomePrompt()

        if u_input == 0: 
            print("Quitting.")
            return
        elif u_input == 1:
            self.PlayGame(None, Player(Board.BLACK))
        elif u_input == 2:
            self.PlayGame(Player(Board.WHITE), Player(Board.BLACK))
        else:
            print("Error, unknown option cannot be caught.")
            return
        
        return

    def PlayGame(self, white_player, black_player):
        player_color = (Board.WHITE, Board.BLACK)

        players = {Board.WHITE: white_player, Board.BLACK: black_player}

        moves = 0

        outcome = (False, 0)

        while outcome[0] == False:
            color = player_color[moves % 2]
            player_to_move = Board.Color2Text[color]

            moves += 1

            # Retrieve the player from the dictionary
            cur_player = players[color]
            
            # Display the board state for context
            Prompt.DisplayBoardState(self.board, player_to_move, moves)
            
            # Select point to be played
            point_to_play = None
            if (cur_player is not None):
                point_to_play = cur_player.PlayMove(self.board)
            else:
                point_to_play = Prompt.PromptAndPlayMove(self.board, player_to_move, moves)
            
            # Color the point on the board
            self.board.ColorPoint(point_to_play, color)

            # Report the move
            Prompt.ReportMove(self.board, player_to_move, point_to_play)

            outcome = self.board.DetectGameEnd()

        winner = Board.Color2Text[outcome[1]]
        self._DisplayGameOver(self.board, winner)


if __name__ == "__main__":
    game = Game(4)
    game.Start()