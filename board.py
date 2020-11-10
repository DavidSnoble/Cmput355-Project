import copy

class BoardUtils:
    def GetSegments(points_colored):
        # Convert the list points of the current type (color) into a set
        s_c_pts = set(points_colored)

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
                neighbors = set(BoardUtils.GetNeighbors(cur_pt, clean_none_types=True))
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

    def GetBoardEdges(board_size):
        # Retrieves the edges of the board that 
        # the player's pieces need to reach in a single segment.
        #
        # Output:
        # [left_side_edge, right_side_edge, bottom_side_edge]

        left_side_edge = [(0, i) for i in range(board_size)]
        right_side_edge = [(i, i) for i in range(board_size)]
        bottom_side_edge = [(i, board_size - 1) for i in range(board_size)]

        return [set(left_side_edge), set(right_side_edge), set(bottom_side_edge)]

    def GetNeighbors(pt, clean_none_types = False):
        top_neighbors = BoardUtils.GetTopNeighbors(pt, clean_none_types)
        mid_neighbors = BoardUtils.GetMidNeighbors(pt, clean_none_types)
        bot_neighbors = BoardUtils.GetBotNeighbors(pt, clean_none_types)

        output = top_neighbors + mid_neighbors + bot_neighbors
        return output

    def GetTopNeighbors(pt, clean_none_types = False):
        x, y = pt
        top_y = y - 1
        ### If the current point is at the top of the board ###
        if (top_y < 0):
            if clean_none_types: return []
            else: return [None, None]

        top_left_x = x - 1
        top_left_pt = None

        ### GENERATE TOP LEFT POINT IF ITS WITHIN BOUNDS   ###
        ### If the new top left x is valid (not negative), ###
        ### then we create the point for top_left          ###
        if not (top_left_x < 0): top_left_pt = (top_left_x, top_y)

        top_right_x = x
        top_right_pt = None

        ### GENERATE TOP RIGHT POINT IF ITS WITHIN BOUNDS            ###
        ### If the new top left x is valid (not equal to current y), ###
        ### then we create the point for top_right                   ###
        if not (top_right_x >= y): top_right_pt = (top_right_x, top_y)

        output = []

        if clean_none_types:
            # Append the points IF it isn't None
            if (top_left_pt is not None):
                output.append(top_left_pt)
            if (top_right_pt is not None):
                output.append(top_right_pt)
        else:
            # Compile the output
            output = [top_left_pt, top_right_pt]

        return output

    def GetMidNeighbors(pt, clean_none_types = False):
        x, y = pt

        mid_left_x = x - 1
        mid_left_pt = None

        ### GENERATE MIDDLE LEFT POINT IF ITS WITHIN BOUNDS ###
        ### If the new mid left x is valid (not negative),  ###
        ### then we create the point for mid_left           ###
        if not (mid_left_x < 0): mid_left_pt = (mid_left_x, y)

        mid_right_x = x + 1
        mid_right_pt = None

        ### GENERATE MIDDLE RIGHT POINT IF ITS WITHIN BOUNDS          ###
        ### If the new mid right x is valid (not greater than mid y), ###
        ### then we create the point for top_right                    ###
        if not (mid_right_x > y): mid_right_pt = (mid_right_x, y)

        output = []

        if clean_none_types:
            # Append the points IF it isn't None
            if (mid_left_pt is not None):
                output.append(mid_left_pt)
            if (mid_right_pt is not None):
                output.append(mid_right_pt)
        else:
            # Compile the output
            output = [mid_left_pt, mid_right_pt]

        return output

    def GetBotNeighbors(pt, clean_none_types = False):
        x, y = pt
        bot_y = y + 1
        ### If the current point is at the bottom of the board ###
        if (bot_y < 0):
            if clean_none_types: return [] 
            else: return [None, None]
        
        bot_left_x = x
        bot_left_pt = None

        ### GENERATE BOTTOM LEFT POINT IF ITS WITHIN BOUNDS   ###
        ### If the new bottom left x is valid (not negative), ###
        ### then we create the point for bot_left             ###
        if not (bot_left_x < 0): bot_left_pt = (bot_left_x, bot_y)

        bot_right_x = x + 1
        bot_right_pt = None

        ### GENERATE BOTTOM RIGHT POINT IF ITS WITHIN BOUNDS         ###
        ### If the new top left x is valid (not greater than bot y), ###
        ### then we create the point for top_right                   ###
        if not (bot_right_x > bot_y): bot_right_pt = (bot_right_x, bot_y)

        output = []
        
        if clean_none_types:
            # Append the points IF it isn't None
            if (bot_left_pt is not None):
                output.append(bot_left_pt)
            if (bot_right_pt is not None):
                output.append(bot_right_pt)
        else:
            # Compile the output
            output = [bot_left_pt, bot_right_pt]

        return output


class Board:
    EMPTY, BLACK, WHITE = (0, 1, 2)
    Color2Text = {EMPTY: "0", BLACK: "B", WHITE: "W"}

    ### Built-in Class Methods ###
    def __init__(self, n):
        # The size of the board
        self.size = n

        # A list of lists that is shaped like a triangle.
        self.board = self._GenerateBoard(n)
        
        # A list of the set of points that is the edge of the board.
        # [top_left_side, top_right_side, bottom_side]
        self.board_edges = self._GetBoardEdges(n)

        # Initialize legal moves.
        # (Should start with all the points on the board)
        self.legal_moves = set(self.GetLegalMoves())

        # Initialize the points that white and black are in control of.
        # (Should start with empty lists, since the players have not started playing)
        self.w_points = self._GetPointsOnType(Board.WHITE)
        self.b_points = self._GetPointsOnType(Board.BLACK)

        self.w_segments = []
        self.b_segments = []

    def __repr__(self):
        return self.BoardPretty()

    ### Public Methods ###
    def ColorPoint(self, pt, color):
        # Perform pre-operation checks
        if not pt in self.legal_moves:
            return False
        if not color in self.Color2Text.keys():
            return False

        # Color point on board
        x, y = pt
        self.board[y][x] = color

        # Update the board's state
        # Exhaust a legal_move (remove pt from the set)
        self.legal_moves.remove(pt)

        # Add the point to the list of the corresponding player &
        # Update the segments
        if (color == Board.WHITE):
            self.w_points.append(pt)
            self._UpdateSegments(pt, self.w_segments)
        elif (color == Board.BLACK):
            self.b_points.append(pt)
            self._UpdateSegments(pt, self.b_segments)
        

        return True

    def DetectGameEnd(self):
        if (self._IsWinner(Board.WHITE)):
            return (True, Board.WHITE)

        if (self._IsWinner(Board.BLACK)):
            return (True, Board.BLACK)
        
        if (len(self.legal_moves) == 0):
            return (True, Board.EMPTY)
        
        return (False, Board.EMPTY)

    def GetValue(self, pt):
        x, y = pt
        if (x < 0) or (y < 0): return None
        if (x >= len(self.board)): return None
        if (y > len(self.board[y])): return None
        return self.board[y][x]

    def GetLegalMoves(self):
        output = list()
        for y in range(len(self.board)):
            for x in range(len(self.board[y])):
                pt = (x, y)
                value = self.GetValue(pt)
                if (value is not None) and (value != Board.WHITE) and (value != Board.BLACK):
                    output.append(pt)
        return output

    def GetNeighbors(self, pt, clean_none_types = True):
        return BoardUtils.GetNeighbors(pt, clean_none_types)

    def GetSegments(self, color):
        # Get all the points of the current type (color)
        c_pts = self._GetPointsOnType(color)
        return BoardUtils.GetSegments(c_pts)

    def BoardPretty(self):
        length = len(self.board)

        padding = " "
        spacer = " "

        output = ""
        for y in range(length):
            # Retrieve the values on the board and turn it into text
            values = ""
            for x in range(len(self.board[y])):
                symbol = '0'
                if (self.board[y][x] in self.Color2Text.keys()):
                    symbol = str(self.Color2Text[self.board[y][x]])
                values += symbol + " "
            
            # Create the spacers to help center the values on the board
            # (This is because the board is triangular).
            spacers = spacer * (length - (y + 1))

            # Append the line into the output
            output += padding + (spacers + values.strip() + spacers) + "\n"
        
        return output.rstrip()

    def Clone(self):
        b = Board(self.size)
        
        b.size = self.size
        
        b.board = copy.deepcopy(self.board)
        
        b.board_edges = copy.deepcopy(self.board_edges)
        
        b.legal_moves = copy.deepcopy(self.legal_moves)
        
        b.w_points = copy.deepcopy(self.w_points)
        b.b_points = copy.deepcopy(self.b_points)

        b.w_segments = copy.deepcopy(self.w_segments)
        b.b_segments = copy.deepcopy(self.b_segments)

        return b

    ### Private Methods ###
    def _IsWinner(self, color):
        c_segments = []

        # Select the segment list that corresponds to the color
        # If the color is not valid (not BLACK nor WHITE), then return False
        if (color == Board.WHITE): 
            c_segments = self.w_segments
        elif (color == Board.BLACK): 
            c_segments = self.b_segments
        else: 
            return False
        
        # If any segment within the segment list 
        # is considered a 'winning' segment, then return True
        for segment in c_segments:
            if (self._IsSegmentWin(segment)):
                return True

        return False
    
    def _IsSegmentWin(self, segment):
        # If the segment doesn't have a common point with ANY board_edge, 
        # Then immediately return False. (Segment must touch all edges to be True)
        for board_edge in self.board_edges:
            if len(segment & board_edge) == 0:
                return False
        return True

    def _GenerateBoard(self, n):
        output = []
        for i in range(n):
            output.append([self.EMPTY for _ in range(i + 1)])
        return output

    def _GetBoardEdges(self, n):
        return BoardUtils.GetBoardEdges(self.size)

    def _GetPointsOnType(self, color):
        # Retrieves the points based on color
        output = []
        for y in range(len(self.board)):
            for x in range(len(self.board[y])):
                pt = (x, y)
                if (self.GetValue(pt) == color):
                    output.append(pt)
        return output

    def _UpdateSegments(self, pt, pt_segments):
        new_segment = set([pt])

        neighbors = self.GetNeighbors(pt)
        pts_of_interest = set(neighbors) | new_segment

        # Identify which segments to remove,
        # and add the segments that will be removed to a new segment
        segments_to_remove = []
        for i in range(len(pt_segments)):
            cur_segment = pt_segments[i]
            if len(pts_of_interest & cur_segment) > 0:
                segments_to_remove.append(i)
                new_segment = new_segment | cur_segment
        
        # Remove the unneeded segments
        segments_to_remove.reverse()
        for i in segments_to_remove:
            pt_segments.pop(i)
        
        # Add the new segment into pt_segments
        pt_segments.append(new_segment)

        return


def TestBoardClass():
    b = Board(4)
    
    print(b)
    print()

    pts = [(0, 1), (1, 1), (1, 3), (2, 3)] 
    color = b.WHITE
    for p in pts:
        b.ColorPoint(p, color)
    
    print(b)
    # segments = b.GetSegments(color)
    segments = b.w_segments
    # segments = b.b_segments
    for s in segments:
        print(s)
    print()

    new_b = b.Clone()

    new_pts = [(1, 2)]
    # new_pts = [(0, 3), (3, 3)]
    for p in new_pts:    
        new_b.ColorPoint(p, color)

    print(b)
    print("vs")
    print(new_b)
    # segments = b.GetSegments(color)
    segments = new_b.w_segments
    # segments = b.b_segments
    for s in segments:
        print(s)
    print()
    
    outcome = new_b.DetectGameEnd()

    text = ""
    if (outcome[0]): text = "Game End" 
    else: text = "Game Ongoing"
    print("{} {}".format(text, Board.Color2Text[outcome[1]]))

    outcome = b.DetectGameEnd()

    text = ""
    if (outcome[0]): text = "Game End" 
    else: text = "Game Ongoing"
    print("{} {}".format(text, Board.Color2Text[outcome[1]]))

    pass


if __name__ == "__main__":
    TestBoardClass()
