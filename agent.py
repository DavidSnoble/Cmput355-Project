import board
import AStar

class Agent:
    color = "EMPTY"
    moves_left = []
    moves_right = []
    moves_bottom = []

    pairs_left = []
    pairs_right = []
    pairs_bottom = []




    def __init__(self,color):
        self.color = color

    def PickStart(self, board):
        x = int(board.size / 4)
        y = int(board.size / 2)
        point = (x,y)
        
        if (board.GetValue(point) == board.EMPTY):
            return point
        else:
            return (x, y+1)

    def MovesFromPath(self, path):
        return [], []



    def FirstTurn(self, board):
        start = self.PickStart(board)

        edges = board.GetBoardEdges(board.size)

        path_left = AStar.AStar(board, start, edges[0], self.color)
        path_right = AStar.AStar(board, start, edges[1], self.color)
        path_bottom = AStar.AStar(board, start, edges[2], self.color)

        self.moves_left, self.pairs_left = self.MovesFromPath(path_left)
        self.moves_right, self.pairs_right = self.MovesFromPath(path_right)
        self.moves_bottom, self.pairs_bottom = self.MovesFromPath(path_bottom)


    def PlayTurn(self):
        pass