import board, pieces, numpy

class Heuristics:

    # The tables denote the points scored for the position of the pieces on the board.

    SPHERE_TABLE = numpy.array([
        [ 0,  0,  0,  0,  0,  0,  0,  0],
        [ 5, 10, 10,-20,-20, 10, 10,  5],
        [ 5, -5,-10,  0,  0,-10, -5,  5],
        [ 0,  0,  0, 20, 20,  0,  0,  0],
        [ 5,  5, 10, 25, 25, 10,  5,  5],
        [10, 10, 20, 30, 30, 20, 10, 10],
        [50, 50, 50, 50, 50, 50, 50, 50],
        [ 0,  0,  0,  0,  0,  0,  0,  0]
    ])


    @staticmethod
    def evaluate(board):
        material = Heuristics.get_material_score(board)

        sphere = Heuristics.get_piece_position_score(board, pieces.Sphere.PIECE_TYPE, Heuristics.SPHERE_TABLE)

        return material + sphere

    # Returns the score for the position of the given type of piece.
    # The table is the 2d numpy array used for the scoring. Example: Heuristics.SPHERE_TABLE
    @staticmethod
    def get_piece_position_score(board, piece_type, table):
        white = 0
        black = 0
        for x in range(7):
            for y in range(7):
                piece = board.Spherepieces[x][y]
                if (piece != 0):
                    if (piece.piece_type == piece_type):
                        if (piece.color == pieces.Piece.PURPLE):
                            white += table[x][y]
                        else:
                            black += table[7 - x][y]

        return white - black

    @staticmethod
    def get_material_score(board):
        white = 0
        black = 0
        for x in range(7):
            for y in range(7):
                piece = board.Spherepieces[x][y]
                if (piece != 0):
                    if (piece.color == pieces.Piece.PURPLE):
                        white += piece.value
                    else:
                        black += piece.value

        return white - black


class AI:

    INFINITE = 10000000

    @staticmethod
    def get_ai_move(Sphereboard, invalid_moves,alg_no,game_type):
        
        if game_type == '1' and alg_no == '0':
            pcs = pieces.Piece.RED
        elif game_type == '1' and alg_no == '1':  
            pcs = pieces.Piece.PURPLE
        else :
            pcs = pieces.Piece.RED
        
        best_move = 0
        best_score = AI.INFINITE
        for move in Sphereboard.get_possible_moves(pcs):
            if (AI.is_invalid_move(move, invalid_moves)):
                continue

            copy = board.Board.clone(Sphereboard)
            copy.perform_move(move)
            
            if alg_no == 1:
                score = AI.alphabeta(copy, 2, -AI.INFINITE, AI.INFINITE, True) 
            else:  
                score = AI.minimax(copy, 2, True)

            if (score < best_score):
                best_score = score
                best_move = move

        # Checkmate.
        if (best_move == 0):
            return 0

        copy = board.Board.clone(Sphereboard)
        copy.perform_move(best_move)
        if (copy.is_check(pcs)):
            invalid_moves.append(best_move)
            return AI.get_ai_move(Sphereboard, invalid_moves,alg_no, game_type)

        return best_move

    @staticmethod
    def is_invalid_move(move, invalid_moves):
        for invalid_move in invalid_moves:
            if (invalid_move.equals(move)):
                return True
        return False

    @staticmethod
    def minimax(Sphereboard, depth, maximizing):
        if (depth == 0):
            return Heuristics.evaluate(Sphereboard)

        if (maximizing):
            best_score = -AI.INFINITE
            for move in Sphereboard.get_possible_moves(pieces.Piece.PURPLE):
                copy = board.Board.clone(Sphereboard)
                copy.perform_move(move)

                score = AI.minimax(copy, depth-1, False)
                best_score = max(best_score, score)

            return best_score
        else:
            best_score = AI.INFINITE
            for move in Sphereboard.get_possible_moves(pieces.Piece.RED):
                copy = board.Board.clone(Sphereboard)
                copy.perform_move(move)

                score = AI.minimax(copy, depth-1, True)
                best_score = min(best_score, score)

            return best_score

    @staticmethod
    def alphabeta(Sphereboard, depth, a, b, maximizing):
        if (depth == 0):
            return Heuristics.evaluate(Sphereboard)

        if (maximizing):
            best_score = -AI.INFINITE
            for move in Sphereboard.get_possible_moves(pieces.Piece.PURPLE):
                copy = board.Board.clone(Sphereboard)
                copy.perform_move(move)

                best_score = max(best_score, AI.alphabeta(copy, depth-1, a, b, False))
                a = max(a, best_score)
                if (b <= a):
                    break
            return best_score
        else:
            best_score = AI.INFINITE
            for move in Sphereboard.get_possible_moves(pieces.Piece.RED):
                copy = board.Board.clone(Sphereboard)
                copy.perform_move(move)

                best_score = min(best_score, AI.alphabeta(copy, depth-1, a, b, True))
                b = min(b, best_score)
                if (b <= a):
                    break
            return best_score


class Move:

    def __init__(self, xfrom, yfrom, xto, yto, castling_move):
        self.xfrom = xfrom
        self.yfrom = yfrom
        self.xto = xto
        self.yto = yto
        self.castling_move = castling_move

    # Returns true iff (xfrom,yfrom) and (xto,yto) are the same.
    def equals(self, other_move):
        return self.xfrom == other_move.xfrom and self.yfrom == other_move.yfrom and self.xto == other_move.xto and self.yto == other_move.yto

    def to_string(self):
        return "(" + str(self.xfrom) + ", " + str(self.yfrom) + ") -> (" + str(self.xto) + ", " + str(self.yto) + ")"
