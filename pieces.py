import board, ai

class Piece():

    PURPLE = "P" 
    RED = "R"

    def __init__(self, x, y, color, piece_type, value):
        self.x = x
        self.y = y
        self.color = color
        self.piece_type = piece_type
        self.value = value



    # Returns all diagonal moves for this piece. 
    def get_possible_diagonal_moves(self, board):
        moves = []

        for i in range(1, 8):
            if (not board.in_bounds(self.x+i, self.y+i)):
                break

            piece = board.get_piece(self.x+i, self.y+i)
            moves.append(self.get_move(board, self.x+i, self.y+i))
            if (piece != 0):
                break

        for i in range(1, 8):
            if (not board.in_bounds(self.x+i, self.y-i)):
                break

            piece = board.get_piece(self.x+i, self.y-i)
            moves.append(self.get_move(board, self.x+i, self.y-i))
            if (piece != 0):
                break

        for i in range(1, 8):
            if (not board.in_bounds(self.x-i, self.y-i)):
                break

            piece = board.get_piece(self.x-i, self.y-i)
            moves.append(self.get_move(board, self.x-i, self.y-i))
            if (piece != 0):
                break

        for i in range(1, 8):
            if (not board.in_bounds(self.x-i, self.y+i)):
                break

            piece = board.get_piece(self.x-i, self.y+i)
            moves.append(self.get_move(board, self.x-i, self.y+i))
            if (piece != 0):
                break

        return self.remove_null_from_list(moves)

    # Returns all horizontal moves for this piece.
    def get_possible_horizontal_moves(self, board):
        moves = []

        # Moves to the right of the piece.
        for i in range(1, 8 - self.x):
            piece = board.get_piece(self.x + i, self.y)
            moves.append(self.get_move(board, self.x+i, self.y))

            if (piece != 0):
                break

        # Moves to the left of the piece.
        for i in range(1, self.x + 1):
            piece = board.get_piece(self.x - i, self.y)
            moves.append(self.get_move(board, self.x-i, self.y))
            if (piece != 0):
                break

        # Downward moves.
        for i in range(1, 8 - self.y):
            piece = board.get_piece(self.x, self.y + i)
            moves.append(self.get_move(board, self.x, self.y+i))
            if (piece != 0):
                break

        # Upward moves.
        for i in range(1, self.y + 1):
            piece = board.get_piece(self.x, self.y - i)
            moves.append(self.get_move(board, self.x, self.y-i))
            if (piece != 0):
                break

        return self.remove_null_from_list(moves)

    # Returns a Move object with (xfrom, yfrom) set to the piece current position.
    # (xto, yto) is set to the given position. If the move is not valid 0 is returned.
    # A move is not valid if it is out of bounds, or a piece of the same color is
    # being eaten.
    def get_move(self, board, xto, yto):
        move = 0
        if (board.in_bounds(xto, yto)):
            piece = board.get_piece(xto, yto)
            if (piece != 0):
                if (piece.color != self.color):
                    move = ai.Move(self.x, self.y, xto, yto, False)
            else:
                move = ai.Move(self.x, self.y, xto, yto, False)
        return move

    # Returns the list of moves cleared of all the 0's.
    def remove_null_from_list(self, l):
        return [move for move in l if move != 0]

    def to_string(self):
        return self.color + self.piece_type + " "



class Sphere(Piece):

    PIECE_TYPE = "P"
    VALUE = 100

    def __init__(self, x, y, color):
        super(Sphere, self).__init__(x, y, color, Sphere.PIECE_TYPE, Sphere.VALUE)

    def is_starting_position(self):
        if (self.color == Piece.RED):
            return self.y == 1
        else:
            return self.y == 8 - 2

    #Save board state and move to the transposition table if not present.
    #If same action taken previously, deny the move.
    def checkTransposition(self, board, move):
        
        if tuple([board.to_string(), move.to_string()]) in board.trans_table:
            return False
        else:
            board.trans_table[tuple([board.to_string(), move.to_string()])] = True
        return True

    #Check if there will be 4 of the same color pieces linearly, horizontally or diagonally after the movement
    def check4alignment(self, board, mMove):

        count = 1
        if isinstance(mMove, int):
            return False

        x = mMove.xto
        y = mMove.yto

        for i in range(0, 6):
            piece = board.get_piece(x, i)
            if (piece != 0):
                if (piece.color == self.color):
                    count += 1
        
        if count >= 4:
            return False
        else:
            count = 1

        for i in range(0, 6):
            piece = board.get_piece(i, y)
            if (piece != 0):
                if (piece.color == self.color):
                    count += 1
        
        if count >= 4:
            return False
        else:
            count = 1

        for i in range(0, 6):
            if x + i < 7 and y + i < 7:
                piece = board.get_piece(x+i, y+i)
                if (piece != 0):
                    if (piece.color == self.color):
                        count += 1

            if x - i >= 0 and y - i >= 0:
                piece = board.get_piece(x-i, y-i)
                if (piece != 0):
                    if (piece.color == self.color):
                        count += 1
        
        if count >= 4:
            return False
        else:
            count = 1

        for i in range(0, 6):
            if x - i >= 0 and y + i < 7:
                piece = board.get_piece(x-i, y+i)
                if (piece != 0):
                    if (piece.color == self.color):
                        count += 1

            if x + i < 7 and y - i >= 0:
                piece = board.get_piece(x+i, y-i)
                if (piece != 0):
                    if (piece.color == self.color):
                        count += 1

        if count >= 4:
            return False
        
        return True

    def get_possible_moves(self, board):
        moves = []

        ############
        # Direction the piece can move in.
        #     x+1  x-1  x
        #     y+1, y-1, y
        direction = -1
        ref = 6
        if (self.color == Piece.RED):
            direction = 1
            ref = 0

        # The general 1 step forward move.
        if (board.get_piece(self.x, self.y+direction) == 0):
            mMove = self.get_move(board, self.x, self.y + direction)
            if self.check4alignment(board, mMove) and self.checkTransposition(board, mMove):
                moves.append(mMove)

        if (board.get_piece(self.x+1, self.y+direction) == 0):
            mMove = self.get_move(board, self.x+1, self.y + direction)
            if self.check4alignment(board, mMove) and self.checkTransposition(board, mMove):
                moves.append(mMove)
            
        if (board.get_piece(self.x-1, self.y+direction) == 0):
            mMove = self.get_move(board, self.x-1, self.y + direction)
            if self.check4alignment(board, mMove) and self.checkTransposition(board, mMove):
                moves.append(mMove)
        if (board.get_piece(self.x+1, self.y) == 0) and self.y != ref:
            mMove = self.get_move(board, self.x+1, self.y)
            if self.check4alignment(board, mMove) and self.checkTransposition(board, mMove):
                moves.append(mMove)
        if (board.get_piece(self.x-1, self.y) == 0) and self.y != ref:
            mMove = self.get_move(board, self.x-1, self.y)
            if self.check4alignment(board, mMove) and self.checkTransposition(board, mMove):
                moves.append(mMove)

        if (self.y-direction != ref):    
            if (board.get_piece(self.x, self.y-direction) == 0):
                mMove = self.get_move(board, self.x, self.y - direction)
                if self.check4alignment(board, mMove) and self.checkTransposition(board, mMove):
                    moves.append(mMove)       

            if (board.get_piece(self.x+1, self.y-direction) == 0):
                mMove = self.get_move(board, self.x+1, self.y - direction)
                if self.check4alignment(board, mMove) and self.checkTransposition(board, mMove):
                    moves.append(mMove)

            if (board.get_piece(self.x-1, self.y-direction) == 0):
                mMove = self.get_move(board, self.x-1, self.y - direction)
                if self.check4alignment(board, mMove) and self.checkTransposition(board, mMove):
                    moves.append(mMove)           
            
        return self.remove_null_from_list(moves)   
         
    
    def get_eat_piece(self, board):
        
        direction = -1
        if (self.color == Piece.RED):
            direction = 1
            
        # Eating pieces. right forward cross
        piece = board.get_piece(self.x + 1, self.y + direction)
        if (piece != 0): 
            if (piece.color != self.color):
                piece2 = board.get_piece(self.x + 2, self.y + 2*direction)
                if (piece2 != 0):
                    if (piece2.color == self.color):
                        board.eat_piece(self.x + 1, self.y + direction)
        # Eating pieces. left forward cross
        piece = board.get_piece(self.x - 1, self.y + direction)
        if (piece != 0):
            if (piece.color != self.color):
                piece2 = board.get_piece(self.x - 2, self.y + 2*direction)
                if (piece2 != 0):
                    if (piece2.color == self.color):
                        board.eat_piece(self.x - 1, self.y + direction)

        # Eating pieces. right backward cross
        piece = board.get_piece(self.x + 1, self.y - direction)
        if (piece != 0):
            if (piece.color != self.color):
                piece2 = board.get_piece(self.x + 2, self.y - 2*direction)
                if (piece2 != 0):
                    if (piece2.color == self.color):
                        board.eat_piece(self.x + 1, self.y - direction)

        # Eating pieces. left backward cross
        piece = board.get_piece(self.x - 1, self.y - direction)
        if (piece != 0):
            if (piece.color != self.color):
                piece2 = board.get_piece(self.x - 2, self.y - 2*direction)
                if (piece2 != 0):
                    if (piece2.color == self.color):
                        board.eat_piece(self.x - 1, self.y - direction)
                        
        # Eating pieces. right 
        piece = board.get_piece(self.x + 1, self.y)
        if (piece != 0):
            if (piece.color != self.color):
                piece2 = board.get_piece(self.x + 2, self.y )
                if (piece2 != 0):
                    if (piece2.color == self.color):
                        board.eat_piece(self.x + 1, self.y )

        # Eating pieces. left 
        piece = board.get_piece(self.x - 1, self.y )
        if (piece != 0):
            if (piece.color != self.color):
                piece2 = board.get_piece(self.x - 2, self.y )
                if (piece2 != 0):
                    if (piece2.color == self.color):
                        board.eat_piece(self.x - 1, self.y)
                        
        # Eating pieces. up 
        piece = board.get_piece(self.x , self.y + direction)
        if (piece != 0):
            if (piece.color != self.color):
                piece2 = board.get_piece(self.x , self.y +2*direction )
                if (piece2 != 0):
                    if (piece2.color == self.color):
                        board.eat_piece(self.x , self.y + direction )

        # Eating pieces. down 
        piece = board.get_piece(self.x , self.y - direction)
        if (piece != 0):
            if (piece.color != self.color):
                piece2 = board.get_piece(self.x , self.y -2*direction )
                if (piece2 != 0):
                    if (piece2.color == self.color):
                        board.eat_piece(self.x, self.y -direction)                        
                

    def clone(self):
        return Sphere(self.x, self.y, self.color)
