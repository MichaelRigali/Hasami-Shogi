# Author: Michael Rigali
# Date: 11/21/2021
# Description: An abstract board game called hasami shogi (japanese chess) where the rules can be found here:
# https://en.wikipedia.org/wiki/Hasami_shogi


class HasamiShogiGame:
    """
    A class named HasamiShogiGame for playing an abstract board game called hasami shogi.
    The rules:
    see https://en.wikipedia.org/wiki/Hasami_shogi

    Variant 1

    Play is on a traditional shogi board, with each player having nine men. Traditional shogi pawns (fu) can be used as
    men; unpromoted pawns (歩) for Black (先手 sente), promoted pawns (と) for White (後手 gote). At the start of the game
    each player's pieces fill their first rank, with Black's men on the lower side of the board. Black moves first,
    then players alternate turns. A player wins by capturing all but one of their opponent's men.

    Moving
    All pieces move the same as a rook in shogi. (That is, any number of empty cells vertically or horizontally.)
    A move consists of moving a piece to an empty cell of the board. As in shogi there is no jumping,
    so a piece can move no further than adjacent to a friendly or enemy piece in its path.

    Capturing
    An opponent's piece is captured using the custodian method: the player occupies the two cells adjacent to the piece
    either horizontally (on a rank) or vertically (on a file). An enemy piece in a corner cell can be captured by
    occupying the two cells that orthogonally surround it. Captured pieces are removed from the game. Multiple pieces
    can be captured in a single move if all the cells between the capturing player's two pieces are filled by enemy men.

    A player can safely move a piece to a cell between two enemy pieces without being captured. Likewise, it is safe to
    move a piece to complete a chain of friendly pieces flanked by two opponent pieces—none of the "sandwiched" pieces
    are captured.
    """

    def __init__(self):
        """
        The constructor method for the HasamiShogiGame class Takes no parameters. Initializes the required data
        members. All data members are private.
        """
        # create board 9 x 9
        self._board = [[letter + str(index) for index in range(1, 10)] for letter in "abcdefghi"]
        self._board_status = [['NONE'] * 9 for x in range(9)]
        # black and red pieces
        self._board_status[0] = ['BLACK'] * 9
        self._board_status[-1] = ['RED'] * 9
        self._current_player = 'BLACK'
        self._captured_pieces = {'BLACK': 0, 'RED': 0}

    def __str__(self):
        """
        Alters the foreground and background of strings to make the board look better.
        """
        board_str = self.bluen("  1 2 3 4 5 6 7 8 9 ") + "\n"
        board = self._board_status
        for row in range(len(board)):
            board_str += self.bluen(chr(ord('a') + row) + " ")
            for col in range(len(board[row])):
                if board[row][col] == "NONE":
                    board_str += "\x1b[1;43m" + ". " + "\x1b[0m"
                else:
                    if board[row][col] == "RED":
                        ch = self.redden('R ')
                    else:
                        ch = self.blacken('B ')
                    board_str += ch
            board_str += "\n"
        return board_str + "\x1b[0m"

    def get_game_state(self):
        """
        A method called get_game_state that takes no parameters and returns 'UNFINISHED', 'RED_WON' or 'BLACK_WON'.
        """
        black_pieces = 0
        red_pieces = 0
        for row in range(len(self._board_status)):
            for col in range(len(self._board_status[row])):
                if self._board_status[row][col] == "RED":
                    red_pieces += 1
                elif self._board_status[row][col] == "BLACK":
                    black_pieces += 1
        if black_pieces > 1 and red_pieces > 1:
            return 'UNFINISHED'
        elif black_pieces > 1:
            return 'BLACK_WON'
        else:
            return 'RED_WON'

    def get_active_player(self):
        """
        A method called get_active_player that takes no parameters and returns whose turn it is - either 'RED' or
        'BLACK'.
        """
        return self._current_player

    def get_num_captured_pieces(self, color):
        """
        A method called get_num_captured_pieces that takes one parameter, 'RED' or 'BLACK', and returns the number
         of pieces of that color that have been captured.
        """
        return self._captured_pieces[color]

    def position_to_coords(self, position):
        """
        a method to translate the position into x_coordinate, y coordinates
        """
        x_coordinate = ord(position[0]) - ord('a')
        y_coordinate = int(position[1]) - 1
        return x_coordinate, y_coordinate

    def coords_to_position(self, x_coordinate, y_coordinate):
        """
        A method that takes as a parameter an x and y coordinate to translate the x, y coordinates to board position
        """
        return chr(ord('a') + x_coordinate) + str(y_coordinate + 1)

    def get_square_occupant(self, position):
        """
        A method called get_square_occupant that takes one parameter, a string representing a square (such as 'i7'),
        and returns 'RED', 'BLACK', or 'NONE', depending on whether the specified square is occupied by a red piece,
        a black piece, or neither.
        """
        x_coordinate, y_coordinate = self.position_to_coords(position)
        return self._board_status[x_coordinate][y_coordinate]

    def _set_square_status(self, position, piece):
        """
        A method that takes in as a parameter the following data members, position and piece. It is a function that
        takes in the Position as a destination, Modifies and restructures the board to replace origin
        with "NONE" and updates new position with piece.
        """
        # a = lowest row. ord('a') = 97, ord('b') = 98 ect. Used to find the coordinate in the list.
        x_coordinate, y_coordinate = self.position_to_coords(position)
        self._board_status[x_coordinate][y_coordinate] = piece

    def make_move(self, string_moved_from, string_moved_to):
        """
        A method called make_move that takes three parameters that represent the square moved from and the square moved
        to, as well as which players turn it is. For example, make_move('b3', 'b9'). If the square being moved from does
        not contain a piece belonging to the player whose turn it is, or if the indicated move is not legal, or if the
        game has already been won, then it just returns False. Otherwise it makes the indicated move, remove any
        captured pieces, updates the game state if necessary, updates whose turn it is, and returns True.
        """
        if self.get_game_state() != 'UNFINISHED':
            print("game already won")
            return False
        if not self.is_valid_move(string_moved_from, string_moved_to):
            print("illegal move")
            return False

        piece = self.get_square_occupant(string_moved_from)
        self._set_square_status(string_moved_to, piece)
        self._set_square_status(string_moved_from, "NONE")
        self.piece_capture(string_moved_to, piece)

        if self._current_player == "RED":
            self._current_player = "BLACK"
        else:
            self._current_player = "RED"
        return True

    def try_capture(self, color, enemy, x_coordinate, y_coordinate, direction):
        """
        This function tries to capture an enemy piece if possible. It takes in a parameter color, enemy, x coordinates,
        y coordinates, and direction. Starts the game with the number of captured pieces to 0.
        """
        captured_piece = 0
        do_capture = False
        if direction == 'rowminus':
            save_y = y_coordinate
            while y_coordinate >= 0:
                position = self.coords_to_position(x_coordinate, y_coordinate)
                piece = self.get_square_occupant(position)
                if piece == "NONE":
                    return
                elif piece == enemy:
                    captured_piece += 1
                    y_coordinate -= 1
                # hit my own piece
                elif piece == color:
                    do_capture = True
                    break
            if do_capture:
                for index in range(save_y, save_y - captured_piece, -1):
                    position = self.coords_to_position(x_coordinate, index)
                    self._set_square_status(position, "NONE")
        if direction == 'rowplus':
            save_x = y_coordinate
            while y_coordinate < 9:
                position = self.coords_to_position(x_coordinate, y_coordinate)
                piece = self.get_square_occupant(position)
                if piece == "NONE":
                    return
                elif piece == enemy:
                    captured_piece += 1
                    y_coordinate += 1
                # hit my own piece
                elif piece == color:
                    do_capture = True
                    break
            if do_capture:
                for index in range(save_y, save_y + captured_piece, 1):
                    position = self.coords_to_position(x_coordinate, index)
                    self._set_square_status(position, "NONE")
        if direction == 'colminus':
            save_x = x_coordinate
            while x_coordinate >= 0:
                position = self.coords_to_position(x_coordinate, y_coordinate)
                piece = self.get_square_occupant(position)
                if piece == "NONE":
                    return
                elif piece == enemy:
                    captured_piece += 1
                    x_coordinate -= 1
                # hit my own piece
                elif piece == color:
                    do_capture = True
                    break
            if do_capture:
                for index in range(save_x, save_x - captured_piece, -1):
                    position = self.coords_to_position(index, y_coordinate)
                    self._set_square_status(position, "NONE")
        if direction == 'colplus':
            save_x = x_coordinate
            while x_coordinate < 9:
                position = self.coords_to_position(x_coordinate, y_coordinate)
                piece = self.get_square_occupant(position)
                if piece == "NONE":
                    return
                elif piece == enemy:
                    captured_piece += 1
                    x_coordinate += 1
                # hit my own piece
                elif piece == color:
                    do_capture = True
                    break
            if do_capture:
                for index in range(save_x, save_x + captured_piece, 1):
                    position = self.coords_to_position(index, y_coordinate)
                    self._set_square_status(position, "NONE")

        self._captured_pieces[enemy] += captured_piece

    def piece_capture(self, string_moved_to, color):
        """
        A method that takes in string_moved_to and color to look around for enemy pieces to capture.
        """
        enemy = "BLACK"
        if color == "BLACK":
            enemy = "RED"
        # take care of all the corner capture cases first
        if string_moved_to == 'a2' and self.get_square_occupant('b1') == color and self.get_square_occupant(
                'a1') == enemy:
            self._set_square_status('a1', 'NONE')
            self._captured_pieces[enemy] += 1
        elif string_moved_to == 'a8' and self.get_square_occupant('b9') == color and self.get_square_occupant(
                'a9') == enemy:
            self._set_square_status('a9', 'NONE')
            self._captured_pieces[enemy] += 1
        elif string_moved_to == 'i2' and self.get_square_occupant('h1') == color and self.get_square_occupant(
                'i1') == enemy:
            self._set_square_status('i1', 'NONE')
            self._captured_pieces[enemy] += 1
        elif string_moved_to == 'i8' and self.get_square_occupant('h9') == color and self.get_square_occupant(
                'i9') == enemy:
            self._set_square_status('i9', 'NONE')
            self._captured_pieces[enemy] += 1
        elif string_moved_to == 'b1' and self.get_square_occupant('a2') == color and self.get_square_occupant(
                'a1') == enemy:
            self._set_square_status('a1', 'NONE')
            self._captured_pieces[enemy] += 1
        elif string_moved_to == 'b9' and self.get_square_occupant('a8') == color and self.get_square_occupant(
                'a9') == enemy:
            self._set_square_status('a9', 'NONE')
            self._captured_pieces[enemy] += 1
        elif string_moved_to == 'h1' and self.get_square_occupant('i2') == color and self.get_square_occupant(
                'i1') == enemy:
            self._set_square_status('i1', 'NONE')
            self._captured_pieces[enemy] += 1
        elif string_moved_to == 'h9' and self.get_square_occupant('i8') == color and self.get_square_occupant(
                'i9') == enemy:
            self._set_square_status('i9', 'NONE')
            self._captured_pieces[enemy] += 1
        # How to have sense of direction, we search in all 4 directions
        # Plus or minus in the row direction
        # Plus or minus in the col direction
        x_coordinate, y_coordinate = self.position_to_coords(string_moved_to)
        if y_coordinate > 1:
            self.try_capture(color, enemy, x_coordinate, y_coordinate - 1, 'rowminus')
        if y_coordinate < 8:
            self.try_capture(color, enemy, x_coordinate, y_coordinate + 1, 'rowplus')
        if x_coordinate > 1:
            self.try_capture(color, enemy, x_coordinate - 1, y_coordinate, 'colminus')
        if x_coordinate < 8:
            self.try_capture(color, enemy, x_coordinate + 1, y_coordinate, 'colplus')

    def is_valid_move(self, string_moved_from, string_moved_to):
        """
        A method that takes as a parameter a destination and the piece to determine if the move is valid or not.
        i.e.
        A piece moving to an occupied piece
        An empty space
        Not the current player's turn
        Moving an enemy piece
        Destination of piece not found on board
        Moving diagonally
        """
        characters = "abcdefghi"
        current_player = self.get_active_player()
        if len(string_moved_to) != 2:
            print("Not valid string_moved_to")
            return False
        if len(string_moved_from) != 2:
            print("Not valid string_moved_from")
            return False
        if not string_moved_to[0] in characters:
            print("Invalid move to row: ", string_moved_to)
            return False
        if not string_moved_from[0] in characters:
            print("Invalid move from row: ", string_moved_from)
            return False
        if string_moved_to[1] != string_moved_from[1] and string_moved_to[0] != string_moved_from[0]:
            print("No diagonal movement")
            return False
        if int(string_moved_to[1]) < 1 or int(string_moved_to[1]) > 9:
            print("Invalid column to")
            return False
        if int(string_moved_from[1]) < 1 or int(string_moved_from[1]) > 9:
            print("Invalid column from")
            return False
        piece = self.get_square_occupant(string_moved_from)
        destination = self.get_square_occupant(string_moved_to)
        if destination != "NONE":
            print(f"piece in destination {string_moved_to}.")
            return False
        if piece == "NONE":
            print(f"no piece in source {string_moved_from}.")
            return False
        if piece != current_player:
            print(f"piece {piece} in source {string_moved_from} does not belong to {current_player}.")
            return False
        x_from, y_from = self.position_to_coords(string_moved_from)
        # destination
        x_to, y_to = self.position_to_coords(string_moved_to)
        # check that the spaces between from origin and destination are clear
        if x_to == x_from:
            step = 1
            start = y_from + 1
            if y_from > y_to:
                step = -1
                start = y_from - 1
            for i in range(start, y_to, step):
                position = self.coords_to_position(x_to, i)
                if self.get_square_occupant(position) != "NONE":
                    print(f"{position} is occupied already")
                    return False
        elif y_to == y_from:
            step = 1
            start = x_from + 1
            if x_from > x_to:
                step = -1
                start = x_from - 1
            for i in range(start, x_to, step):
                position = self.coords_to_position(i, y_to)
                if self.get_square_occupant(position) != "NONE":
                    print(f"{position} is occupied already")
                    return False
        return True

    def play(self):
        # A method dependent on the player that refers to the object itself and generates movement.
        player = self.get_active_player()
        print(f"It is {player}'s turn")
        from2 = input("Enter the piece position you want to move from: ").rstrip()
        to = input("Enter the piece position you want to move to: ").rstrip()
        self.make_move(from2, to)

    def redden(self, mystr):
        """
        Alters the color or red pieces.
        """
        return "\x1b[31;43m" + mystr + "\x1b[0m"

    def blacken(self, mystr):
        """
        Alters the color of black pieces.
        """
        return "\x1b[30;43m" + mystr + "\x1b[0m"

    def bluen(self, mystr):
        """
        Alters the color of the board.
        """
        return "\x1b[34;43m" + mystr + "\x1b[0m"


def main():
    """
    Actually starts the game.
    """
    game = HasamiShogiGame()
    print(game)
    while game.get_game_state() == "UNFINISHED":
        game.play()
        print(game)
    print(game.get_game_state())


if __name__ == "__main__":
    main()
