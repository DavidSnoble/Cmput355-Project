import board
import math


def getDist(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)

def getMinimaxHeuristic(board, color):
    tile = (0, math.ceil(board.size()/2))
    firstgoal = (math.ceil(board.size()/2), board.size()-1)
    secondgoal = (math.ceil(board.size()/2 - 1), math.ceil(board.size()/2))
    next_tile = (0,0)
    score = 0

    while (tile != firstgoal):
        neighbors = board.GetNeighbors(tile)
        best_val = 10000

        for neighbor in neighbors:
            if (board.GetValue(neighbor) != (color or 0)):
                break

            dist = getDist(neighbor, firstgoal)
            if (board.GetValue(neighbor) == color):
                dist = dist - 1

            if (dist < best_val):
                best_val = dist
                next_tile = neighbor
        
        tile = next_tile
        if (board.GetValue(neighbor) == color):
            pass
        else:
            score = score + 1

    while (tile != secondgoal):
        neighbors = board.GetNeighbors(tile)
        best_val = 10000

        for neighbor in neighbors:
            if (board.GetValue(neighbor) != (color or 0)):
                break

            dist = getDist(neighbor, secondgoal)
            if (board.GetValue(neighbor) == color):
                dist = dist - 1

            if (dist < best_val):
                best_val = dist
                next_tile = neighbor
        
        tile = next_tile
        if (board.GetValue(neighbor) == color):
            pass
        else:
            score = score + 1
    
    return score



