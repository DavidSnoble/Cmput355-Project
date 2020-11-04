

def GenerateBoard(n):
    output = []

    for i in range(n):
        output.append([0 for _ in range(i + 1)])

    return output

def GetValue(B, x, y):
    if (x < 0) or (y < 0): return None
    if (x >= len(B)): return None
    if (y > len(B[x])): return None
    return B[y][x]

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


new_board = GenerateBoard(4)

neighbors = FindAllNeighbors(new_board, 1, 2)

print(new_board)
print(neighbors)

print("game solved")