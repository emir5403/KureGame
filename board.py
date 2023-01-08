import pieces, ai

class Board:

    WIDTH = 7
    HEIGHT = 7

    def __init__(self, Spherepieces):
        self.Spherepieces = Spherepieces
        self.RPeated = 0
        self.PPeated = 0
        self.trans_table = {}


    @classmethod
    def clone(cls, Sphereboard):
        Spherepieces = [[0 for x in range(Board.WIDTH)] for y in range(Board.HEIGHT)]
        for x in range(Board.WIDTH):
            for y in range(Board.HEIGHT):
                piece = Sphereboard.Spherepieces[x][y]
                if (piece != 0):
                    Spherepieces[x][y] = piece.clone()
        return cls(Spherepieces)

    @classmethod
    def new(cls):
        kure_pieces = [[0 for x in range(Board.WIDTH)] for y in range(Board.HEIGHT)]
        # Create pawns.
        for x in range(Board.WIDTH):
            kure_pieces[x][Board.HEIGHT-1] = pieces.Sphere(x, Board.HEIGHT-1, pieces.Piece.PURPLE)
            kure_pieces[x][0] = pieces.Sphere(x, 0, pieces.Piece.RED)

        return cls(kure_pieces)

    def get_possible_moves(self, color):
        moves = []
        for x in range(Board.WIDTH):
            for y in range(Board.HEIGHT):
                piece = self.Spherepieces[x][y]
                if (piece != 0):
                    if (piece.color == color):
                        moves += piece.get_possible_moves(self)

        return moves

    def perform_move(self, move):
        piece = self.Spherepieces[move.xfrom][move.yfrom]
        piece.x = move.xto
        piece.y = move.yto
        self.Spherepieces[move.xto][move.yto] = piece
        self.Spherepieces[move.xfrom][move.yfrom] = 0
        piece.get_eat_piece(self)


    # Returns if the given color is checked.
    def is_check(self, color):
        other_color = pieces.Piece.PURPLE
        if (color == pieces.Piece.PURPLE):
            other_color = pieces.Piece.RED
        for move in self.get_possible_moves(other_color):
            copy = Board.clone(self)
            copy.perform_move(move)
            count = 0
            for x in range(Board.WIDTH):
                for y in range(Board.HEIGHT):
                    piece = copy.Spherepieces[x][y]
                    if (piece != 0):
                        if (piece.color == color):
                            count +=1
            if (count<4):
                return True
        return False

    # Returns piece at given position or 0 if: No piece or out of bounds.
    def get_piece(self, x, y):
        if (not self.in_bounds(x, y)):
            return 0

        return self.Spherepieces[x][y]
    
    def eat_piece(self, x, y):
        if (not self.in_bounds(x, y)):
            return 0
        else:
            eaten = self.Spherepieces[x][y].color
            if eaten == "R":
                self.RPeated += 1
            elif eaten == "P":
                self.PPeated += 1

            self.Spherepieces[x][y] = 0

    def in_bounds(self, x, y):
        return (x >= 0 and y >= 0 and x < Board.WIDTH and y < Board.HEIGHT)

    def to_string(self):
        string =  "    A  B  C  D  E  F  G \n"
        string += "    --------------------\n"
        for y in range(Board.HEIGHT):
            string += str(7 - y) + " | "
            for x in range(Board.WIDTH):
                piece = self.Spherepieces[x][y]
                if (piece != 0):
                    string += piece.to_string()
                else:
                    string += ".. "
            string += "\n"
        return string + "\n"
