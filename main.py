import board, pieces, ai

# Returns a move object based on the users input. Does not check if the move is valid.

def get_alg_type():
    print("Choose The Computer AI algorith --> Minimax : 0, alfa-beta : 1")
    out2 = input("Your Choice: ")
    if (out2 != '1') and (out2 != '0'):
        print("Invalid Choice.")
        return get_alg_type
    return out2
    
    
def get_game_type():
    print("Choose The Game Type --> Player vs Computer : 0, Computer(Minimax) vs Computer(alfa-beta) : 1")
    out = input("Your Choice: ")
    out2 = -1
    if out == 'Q':
        return out
    if (out != '1') and (out != '0'):
        print("Invalid Choice.")
        return get_game_type
    elif (out == '0'):
        out2 = get_alg_type()
    return out,out2



# Returns a move object based on the users input. Does not check if the move is valid.
def get_user_move():
    print("Example Move: A1 A2")
    move_str = input("Your Move: ")
    if move_str == 'Q':
        return move_str
    move_str = move_str.replace(" ", "")

    try:
        xfrom = letter_to_xpos(move_str[0:1])
        yfrom = 7 - int(move_str[1:2]) # The board is drawn "upside down", so flip the y coordinate.
        xto = letter_to_xpos(move_str[2:3])
        yto = 7 - int(move_str[3:4]) # The board is drawn "upside down", so flip the y coordinate.
        return ai.Move(xfrom, yfrom, xto, yto, False)
    except ValueError:
        print("Invalid format. Example: A1 A2")
        return get_user_move()

# Returns a valid move based on the users input.
def get_valid_user_move(board):
    while True:
        move = get_user_move()
        if move == 'Q':
            return move
        valid = False
        possible_moves = board.get_possible_moves(pieces.Piece.PURPLE)
        # No possible moves
        if (not possible_moves):
            return 0

        for possible_move in possible_moves:
            if (move.equals(possible_move)):
                move.castling_move = possible_move.castling_move
                valid = True
                break

        if (valid):
            break
        else:
            print("Invalid move.")
    return move

# Converts a letter (A-H) to the x position on the chess board.
def letter_to_xpos(letter):
    letter = letter.upper()
    if letter == 'A':
        return 0
    if letter == 'B':
        return 1
    if letter == 'C':
        return 2
    if letter == 'D':
        return 3
    if letter == 'E':
        return 4
    if letter == 'F':
        return 5
    if letter == 'G':
        return 6

    raise ValueError("Invalid letter.")

# Entry point.
    
game_type,alg_type = get_game_type()

if game_type == '0':
    print("Player vs Computer.")
    board = board.Board.new()
    print(board.to_string())

    while True:
        
        move = get_valid_user_move(board)
        if (move == 'Q'):
            print("QUIT")
            break
        if (move == 0):
            if (board.is_check(pieces.Piece.PURPLE)):
                print("Game Over. RED Wins.")
                break
            else:
                print("Stalemate.")
                break
    
        board.perform_move(move)
    
        print("User move: " + move.to_string())
        print(board.to_string())
    
        ai_move = ai.AI.get_ai_move(board, [],alg_type,game_type)
        if (ai_move == 0):
            if (board.is_check(pieces.Piece.RED)):
                print("Game Over. PURPLE wins.")
                break
            else:
                print("Stalemate.")
                break
    
        board.perform_move(ai_move)
        print("AI move: " + ai_move.to_string())
        print(board.to_string())
        
elif game_type == '1':
    
     print("Computer vs Computer.")
     
     board = board.Board.new()
     print(board.to_string())

     while True:
         inp = input("Press enter to continue: ")
         if inp == '':
             ai_move1 = ai.AI.get_ai_move(board, [],'0',game_type)
             if (ai_move1 == 'Q'):
                 print("QUIT")
                 break
             if (ai_move1 == 0):
                 if (board.is_check(pieces.Piece.PURPLE)):
                     print("Game Over. RED Wins.")
                     break
                 else:
                     print("Stalemate.")
                     break
         
             board.perform_move(ai_move1)
         
             print("Minimax AI move: " + ai_move1.to_string())
             print(board.to_string())
         
             ai_move2 = ai.AI.get_ai_move(board, [],'1',game_type)
             if (ai_move2 == 0):
                 if (board.is_check(pieces.Piece.RED)):
                     print("Game Over. PURPLE wins.")
                     break
                 else:
                     print("Stalemate.")
                     break
         
             board.perform_move(ai_move2)
             print("alfa-beta AI move: " + ai_move2.to_string())
             print("RP = ", board.RPeated, "PP = ", board.PPeated)
             print(board.to_string())
         elif inp == 'Q':
             print("QUIT") 
             break
         

else:
    print("QUIT")    