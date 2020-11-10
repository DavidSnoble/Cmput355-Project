import copy
import random
from board import Board

EMPTY = 0
BLACK = 1
WHITE = 2

### BOARD FUNCTIONS ###

def GenerateBoard(n):
    output = []

    for i in range(n):
        output.append([0 for _ in range(i + 1)])

    return output

def GetBoardEdges(B):
    # Retrieves the edges of the board that 
    # the player's pieces need to reach in a single segment.
    #
    # Output:
    # [left_side_edge, right_side_edge, bottom_side_edge]
    
    B_length = len(B)

    left_side_edge = [(0, i) for i in range(B_length)]
    right_side_edge = [(i, i) for i in range(B_length)]
    bottom_side_edge = [(i, B_length - 1) for i in range(B_length)]

    return [left_side_edge, right_side_edge, bottom_side_edge]

def GetPointsOnType(B, color):
    # Retrieves the points based on color

    output = []

    for y in range(len(B)):
        for x in range(len(B[y])):
            if (B[y][x] == color):
                output.append((x, y))
    
    return output

def GetSegments(B, color):
    # Get all the points of the current type (color)
    c_pts = GetPointsOnType(B, color)
    s_c_pts = set(c_pts)

    output = []
    while len(s_c_pts) > 0:
        # Pop off the from the valid points to start creating the segment
        start_pt = s_c_pts.pop()

        # Initialize the stack and segment
        stack = [start_pt]
        segment = set([start_pt])

        while len(stack) > 0:
            # Get the current point that we will evaluate for the current segment
            cur_pt = stack.pop()

            # Get the neighbors of the current point and retrieve the points
            # that are of the same color (points within s_c_pts)
            neighbors = set(FindAllNeighbors(cur_pt[0], cur_pt[1], clean_none_types=True))
            intersection = s_c_pts & (neighbors | set([cur_pt])) 

            # Add the valid neighbors onto the stack for further evaluation
            stack += list(intersection)
            # Add the valid neighors ontop of the segment
            segment = segment | intersection

            # Remove the points of that color 
            # (we have already processed them and don't need to deal with them anymore)
            s_c_pts = s_c_pts - intersection
        
        # Add the segment list onto the output
        output.append(segment)

    return output

def DetectGameEnd(B):
    def IsWinner(B, color):
        c_segments = GetSegments(B, color)
        for segment in c_segments:
            if (IsSegmentWin(segment)):
                return True

    def IsSegmentWin(segment):
        if len(segment & s_l_edge) == 0:
            return False
        if len(segment & s_r_edge) == 0:
            return False
        if len(segment & s_b_edge) == 0:
            return False
        return True

    l_edge, r_edge, b_edge = GetBoardEdges(B)
    
    s_l_edge = set(l_edge)
    s_r_edge = set(r_edge)
    s_b_edge = set(b_edge)

    if (IsWinner(B, WHITE)):
        return (True, WHITE)

    if (IsWinner(B, BLACK)):
        return (True, BLACK)
        
    if (len(GetLegalMoves(B)) == 0):
        return (True, EMPTY)

    return (False, EMPTY)

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

def GetTopNeighbors(x, y, clean_none_types = False):
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

def GetMidNeighbors(x, y, clean_none_types = False):
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

def GetBotNeighbors(x, y, clean_none_types = False):
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

def FindAllNeighbors(x, y, clean_none_types = False):
    top_neigbhors = GetTopNeighbors(x, y, clean_none_types)
    mid_neighbors = GetMidNeighbors(x, y, clean_none_types)
    bot_neighbors = GetBotNeighbors(x, y, clean_none_types)

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

    print("legal moves: {}".format(legal_moves))

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
    print("White plays {}".format(point))

    new_B[point[1]][point[0]] = WHITE

    return new_B


def PlayAsBlack(B):
    new_B = copy.deepcopy(B)
    
    point = GetRandomMove(B)

    if (point is None):
        print("pass!")
        return new_B
    print("Black plays {}".format(point))

    new_B[point[1]][point[0]] = BLACK

    return new_B

def PlayMove(B, player_to_move):
    board = None

    if (player_to_move == WHITE):
        board = PlayAsWhite(B)
    elif (player_to_move == BLACK):
        board = PlayAsBlack(B)

    return board

def ColorToText(color):
    text = ""
    if (color == WHITE):
        text = "White"
    elif (color == BLACK):
        text = "Black"
    else:
        text = "Unknown"
    return text

'''
def StartGame():
    board = GenerateBoard(4)

    current_player = WHITE

    moves = 0

    game_end = False
    winner = EMPTY

    while not game_end:
        if ((moves % 2) == 0):
            current_player = WHITE
        else:
            current_player = BLACK

        print("{} to move!".format(ColorToText(current_player)))

        PrintBoard(board)

        new_board = PlayMove(board, current_player)
        board = new_board

        PrintBoard(board)
        print(">>>")

        moves += 1

        (game_end, winner) = DetectGameEnd(board)

    print("Game has ended!")
    print("The winner is {}!".format(ColorToText(winner)))

    return
'''

player = (Board.WHITE, Board.BLACK)

def StartGame():
    b = Board(4)

    player_index = 0
    moves = 0

    outcome = (False, 0)

    while outcome[0] == False:
        player_index = moves % 2
        cur_color = player[player_index]

        color_txt = Board.Color2Text[cur_color]
        print("{} to move!".format(color_txt))
        print(b)
        print("---")

        pt = None
        if (cur_color == Board.WHITE):
            # Generate a legal move from the board
            pt = random.choice(list(b.legal_moves))
        if (cur_color == Board.BLACK):
            # Generate a legal move from the board
            pt = random.choice(list(b.legal_moves))
        # Color the current point
        b.ColorPoint(pt, cur_color)

        print("{} plays {}!".format(color_txt, pt))
        print(b)
        print(">>>")

        moves += 1

        outcome = b.DetectGameEnd()

    print("{} wins!".format(Board.Color2Text[outcome[1]]))

    return

    

StartGame()

# b = GenerateBoard(4)

# white_points = [(0, 1), (1, 1), (1, 3), (2, 3), (3, 3)]
# for w in white_points:
#     b[w[1]][w[0]] = WHITE

# pts = GetPointsOnType(b, WHITE)

# segments = GetSegments(b, WHITE)

# print(b)
# PrintBoard(b)
# print()

# for seg in segments:
#     print(seg)

# print()
# print(DetectGameEnd(b))
