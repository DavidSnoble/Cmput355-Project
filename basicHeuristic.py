import board
import math


def getDist(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)

def getMinimaxHeuristic(board, color):

    
    halfBoard = board.size/2
    if(type(halfBoard) != int):
        int(halfBoard)


    tile = (0, int(halfBoard))
    firstgoal = (int(halfBoard), int(board.size-1))

    secondgoal = (int(halfBoard - 1), int(halfBoard))
    
    next_tile = (-1,-1)

    if(board.GetValue(tile) == color):
        score = 0
    else:
        score = 1


    goals = (firstgoal, secondgoal)
    for goal in goals:
        print("The Goal is " + str(goal))
        searched = []
        while (tile != goal):
            
            searched.append(tile)


            neighbors = board.GetNeighbors(tile)
            print(neighbors)
    
            best_val = 10000
            
            for neighbor in neighbors:

                if (neighbor == goal):
                    next_tile = neighbor 
                    break

                if (neighbor in searched):
                    #print("ALREADY SEARCHED")
                    continue


                if (board.GetValue(neighbor) != (color) and board.GetValue(neighbor) != board.EMPTY):
                    #print("Invalid COLOR " + str(board.GetValue(neighbor)))
                    continue

                dist = getDist(neighbor, goal)

                if (board.GetValue(neighbor) == color):
                    dist = dist - 1

                if (dist < best_val):
                    best_val = dist
                    next_tile = neighbor


            print("Current tile" + str(tile))

            tile = next_tile

            print("Next tile " + str(tile))

            if (board.GetValue(tile) == color):
                pass
            else:
                score = score + 1

        print("Reached the Goal!")
        
     
    return score



