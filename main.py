import copy
import random


EMPTY = 0
BLACK = 1
WHITE = 2

### BOARD FUNCTIONS ###

def GenerateBoard(n):
    output = []

    for i in range(n):
        output.append([0 for _ in range(i + 1)])

    return output

def GetValue(B, x, y):
    if (x < 0) or (y < 0): return None
    if (x >= len(B)): return None
    if (y > len(B[y])): return None
    return B[y][x]

def GetLegalMoves(B):
    output = list()

    for y in range(len(B)):
        for x in range(len(B[y])):
            value = GetValue(B, x, y)
            if (value is not None) and (value != WHITE) and (value != BLACK):
                output.append((x, y))

    return output

def GetTopNeighbors(B, x, y, clean_none_types = False):
    top_y = y - 1
    ### If the current point is at the top of the board ###
    if (top_y < 0):
        if clean_none_types:
            return []
        else:
            return [None, None]

    top_left_x = x - 1
    top_left_pt = None

    ### If the new top left x is valid (not negative), then we create the point for top_left ###
    if not (top_left_x < 0): 
        top_left_pt = (top_left_x, top_y)

    top_right_x = x
    top_right_pt = None

    ### If the new top left x is valid (not equal to current y), then we create the point for top_right ###
    if not (top_right_x >= y):
        top_right_pt = (top_right_x, top_y)

    output = []

    if clean_none_types:
        # Append the points IF it isn't long
        if (top_left_pt is not None):
            output.append(top_left_pt)
        if (top_right_pt is not None):
            output.append(top_right_pt)
    else:
        # Compile the output
        output = [top_left_pt, top_right_pt]

    return output

def GetMidNeighbors(B, x, y, clean_none_types = False):
    mid_left_x = x - 1
    mid_left_pt = None

    ### If the new mid left x is valid (not negative), then we create the point for mid_left ###
    if not (mid_left_x < 0):
        mid_left_pt = (mid_left_x, y)

    mid_right_x = x + 1
    mid_right_pt = None

    ### If the new mid right x is valid (not equal to current y), then we create the point for top_right ###
    if not (mid_right_x > y):
        mid_right_pt = (mid_right_x, y)

    output = []

    if clean_none_types:
        # Append the points IF it isn't long
        if (mid_left_pt is not None):
            output.append(mid_left_pt)
        if (mid_right_pt is not None):
            output.append(mid_right_pt)
    else:
        # Compile the output
        output = [mid_left_pt, mid_right_pt]

    return output

def GetBotNeighbors(B, x, y, clean_none_types = False):
    bot_y = y + 1
    ### If the current point is at the bot of the board ###
    if (bot_y < 0):
        if clean_none_types:
            return []
        else:
            return [None, None]
    
    bot_left_x = x
    bot_left_pt = None

    ### If the new top left x is valid (not negative), then we create the point for top_left ###
    if not (bot_left_x < 0):
        bot_left_pt = (bot_left_x, bot_y)

    bot_right_x = x + 1
    bot_right_pt = None

    ### If the new top left x is valid (not equal to current y), then we create the point for top_right ###
    if not (bot_right_x > bot_y):
        bot_right_pt = (bot_right_x, bot_y)

    output = []

    if clean_none_types:
        # Append the points IF it isn't long
        if (bot_left_pt is not None):
            output.append(bot_left_pt)
        if (bot_right_pt is not None):
            output.append(bot_right_pt)
    else:
        # Compile the output
        output = [bot_left_pt, bot_right_pt]

    return output

def FindAllNeighbors(B, x, y):
    print(GetValue(B, x, y))
    if (GetValue(B, x, y) is None): return None

    top_neigbhors = GetTopNeighbors(B, x, y)
    mid_neighbors = GetMidNeighbors(B, x, y)
    bot_neighbors = GetBotNeighbors(B, x, y)

    output = top_neigbhors + mid_neighbors + bot_neighbors

    return output

def PrintBoard(B):
    width = len(B)

    padding = "  "

    output = "\n"
    for y in range(len(B)):
        spacers = " " * (width - (y + 1))
        
        values = ""
        for x in range(len(B[y])):
            symbol = '0'
            if (B[y][x] == BLACK):
                symbol = "B"
            elif (B[y][x] == WHITE):
                symbol = "W"
            values += str(symbol) + " "

        output += padding + (spacers + values.strip() + spacers) + "\n"
    
    print(output)
    return



### PLAYER FUNCTIONS ###

def GetRandomMove(B):
    legal_moves = GetLegalMoves(B)

    print(legal_moves)

    if (len(legal_moves) == 0):
        return None

    point = random.choice(legal_moves)

    return point

def PlayAsWhite(B):
    new_B = copy.deepcopy(B)

    point = GetRandomMove(B)

    if (point is None):
        print("pass!")
        return new_B
    print("W plays {}".format(point))

    new_B[point[1]][point[0]] = WHITE

    return new_B


def PlayAsBlack(B):
    new_B = copy.deepcopy(B)
    
    point = GetRandomMove(B)

    if (point is None):
        print("pass!")
        return new_B
    print("B plays {}".format(point))

    new_B[point[1]][point[0]] = BLACK

    return new_B

def PlayMove(B, player_to_move):
    board = None

    if (player_to_move == WHITE):
        board = PlayAsWhite(B)
    elif (player_to_move == BLACK):
        board = PlayAsBlack(B)

    return board

def StartGame():
    board = GenerateBoard(4)

    current_player = WHITE

    moves = 0
    while (moves <= 10):
        if ((moves % 2) == 0):
            current_player = WHITE
        else:
            current_player = BLACK

        print("{} to move!".format(current_player))

        PrintBoard(board)

        new_board = PlayMove(board, current_player)
        board = new_board

        PrintBoard(board)
        print(">>>")

        moves += 1
        

    return


StartGame()


print("game solved")