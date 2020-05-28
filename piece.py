import copy


# Parent Class
class Piece:

    def __init__(self, row, col, p_type, camp):
        self.name = ""
        self.is_moved = False
        self.is_selected = False
        self.is_king = False

        self.row = row
        self.col = col
        self.piece_type = p_type  # with reference to get_name function
        self.is_bl_or_wh = camp

    def __str__(self):
        return ("Black:" if self.is_bl_or_wh else "White:") + Piece.get_name(self.piece_type) + "(" + str(
            self.row) + "," + str(self.col) + ")"

    @staticmethod
    def get_name(index):
        names = ["k", "q", "r", "b", "n", "p"]
        return names[index]

    def move(self, board, x, y):
        r, c = self.row + x, self.col + y
        if (r, c) in board.pieces:
            board.remove(r, c)
        board.remove(self.row, self.col)
        # Move a chessman from (self.row, self.col, self.row + x, self.col + y)
        self.row += x
        self.col += y
        board.pieces[self.row, self.col] = self
        return True

    def is_valid_move(self, board, x, y):
        raise Exception("virtual method is called.")

    def get_moves(self, board):
        v_moves = []
        for r in range(8):
            for c in range(8):
                if (r, c) in board.pieces and board.pieces[r, c].is_bl_or_wh == self.is_bl_or_wh:
                    continue
                if self.is_valid_move(board, r - self.row, c - self.col):
                    p_copy = copy.deepcopy(self)
                    b_copy = copy.deepcopy(board)
                    b_copy.piece_selected = p_copy
                    b_copy.pawn_pass_by(r, c)
                    p_copy.move(b_copy, r - self.row, c - self.col)

                    if not b_copy.is_check(p_copy.is_bl_or_wh):
                        is_castling = (r == 2 and c == 0) or (r == 6 and c == 0) or (r == 2 and c == 7) or (
                                r == 6 and c == 7)
                        if self.is_king and self.is_moved == False and is_castling and board.is_castling(r, c) == False:
                            continue
                        else:
                            v_moves.append((r, c))
        return v_moves

    def get_between_pieces(self, board, x, y, n1, n2):
        count = 0

        temp_x = n1 / abs(n1) if n1 != 0 else 0
        temp_y = n2 / abs(n2) if n2 != 0 else 0

        nx, ny = x + n1, y + n2
        x, y = x + temp_x, y + temp_y

        while x != nx or y != ny:
            if (x, y) in board.pieces:
                count += 1
            x += temp_x
            y += temp_y
        return count

    def get_value(self):
        raise Exception("virtual method is called.")

    def position_eval(self, x, y, round, mid=100):
        raise Exception("virtual method is called.")


# Children Classes
class Pawn(Piece):
    value = 100

    # value of Pawn on each square of the board
    position_eval_0 = [
        [0, 0, 0, 0, 0, 0, 0, 0],
        [5, 10, 10, -20, -20, 10, 10, 5],
        [5, -5, -10, 0, 0, -10, -5, 5],
        [0, 0, 0, 20, 20, 0, 0, 0],
        [5, 5, 10, 25, 25, 10, 5, 5],
        [10, 10, 20, 30, 30, 20, 10, 10],
        [50, 50, 50, 50, 50, 50, 50, 50],
        [900, 900, 900, 900, 900, 900, 900, 900]
    ]

    position_eval_1 = [
        [0, 0, 0, 0, 0, 0, 0, 0],
        [5, 10, 10, -20, -20, 10, 10, 5],
        [5, -5, -10, 0, 0, -10, -5, 5],
        [0, 0, 0, 20, 20, 0, 0, 0],
        [5, 5, 10, 25, 25, 10, 5, 5],
        [10, 10, 20, 30, 30, 20, 10, 10],
        [50, 50, 50, 50, 50, 50, 50, 50],
        [900, 900, 900, 900, 900, 900, 900, 900]
    ]

    def __init__(self, row, col, camp):
        super().__init__(row, col, 5, camp)
        self.name = "p"

    def get_image(self):
        if self.is_selected:
            if self.is_bl_or_wh:
                return "images/black_pawn.gif"
            else:
                return "images/white_pawn.gif"
        else:
            if self.is_bl_or_wh:
                return "images/black_pawn.gif"
            else:
                return "images/white_pawn.gif"

    def get_value(self):
        return Pawn.value

    def position_eval(self, x, y, round, mid=100):
        if round <= mid:
            return Pawn.position_eval_0[x][y]
        else:
            return Pawn.position_eval_1[x][y]

    def is_valid_move(self, board, x, y):
        if not self.is_bl_or_wh:
            if y == 1 and x == 0:
                if not (self.row + x, self.col + y) in board.pieces.keys():
                    return True
            if y == 1 and abs(x) == 1:
                if (self.row + x, self.col + y) in board.pieces.keys():
                    return True
                elif self.col == 4:
                    if board.pieces[board.last_move[1]].piece_type == 5:
                        if board.last_move[1][1] == 4 and board.last_move[0][1] == 6:
                            if board.last_move[1][0] == self.row + x:
                                return True
            if self.is_moved == False and y == 2 and x == 0:
                if not (self.row + x, self.col + y) in board.pieces.keys():
                    count = self.get_between_pieces(board, self.row, self.col, x, y)
                    if count == 0:
                        return True
        else:
            if y == -1 and x == 0:
                if not (self.row + x, self.col + y) in board.pieces.keys():
                    return True
            if y == -1 and abs(x) == 1:
                if (self.row + x, self.col + y) in board.pieces.keys():
                    return True
                elif self.col == 3:
                    if board.pieces[board.last_move[1]].piece_type == 5:
                        if board.last_move[1][1] == 3 and board.last_move[0][1] == 1:
                            if board.last_move[1][0] == self.row + x:
                                return True
            if self.is_moved == False and y == -2 and x == 0:
                if not (self.row + x, self.col + y) in board.pieces.keys():
                    count = self.get_between_pieces(board, self.row, self.col, x, y)
                    if count == 0:
                        return True
        return False


class Knight(Piece):
    value = 300

    # value of Knight on each square of the board
    position_eval_0 = [
        [-50, -40, -30, -30, -30, -30, -40, -50],
        [-40, -20, 0, 5, 5, 0, -20, -40],
        [-30, 5, 10, 15, 15, 10, 5, -30],
        [-30, 0, 15, 20, 20, 15, 0, -30],
        [-30, 5, 15, 20, 20, 15, 5, -30],
        [-30, 0, 10, 15, 15, 10, 0, -30],
        [-40, -20, 0, 0, 0, 0, -20, -40],
        [-50, -40, -30, -30, -30, -30, -40, -50]
    ]

    position_eval_1 = [
        [-50, -40, -30, -30, -30, -30, -40, -50],
        [-40, -20, 0, 5, 5, 0, -20, -40],
        [-30, 5, 10, 15, 15, 10, 5, -30],
        [-30, 0, 15, 20, 20, 15, 0, -30],
        [-30, 5, 15, 20, 20, 15, 5, -30],
        [-30, 0, 10, 15, 15, 10, 0, -30],
        [-40, -20, 0, 0, 0, 0, -20, -40],
        [-50, -40, -30, -30, -30, -30, -40, -50]
    ]

    def __init__(self, row, col, camp):
        super().__init__(row, col, 4, camp)
        self.name = "n"

    def get_image(self):
        if self.is_selected:
            if self.is_bl_or_wh:
                return "images/black_knight.gif"
            else:
                return "images/white_knight.gif"
        else:
            if self.is_bl_or_wh:
                return "images/black_knight.gif"
            else:
                return "images/white_knight.gif"

    def get_value(self):
        return Knight.value

    def position_eval(self, x, y, round, mid=100):
        if round <= mid:
            return Knight.position_eval_0[x][y]
        else:
            return Knight.position_eval_1[x][y]

    def is_valid_move(self, board, x, y):
        if abs(x) == 1 and abs(y) == 2:
            return True
        elif abs(x) == 2 and abs(y) == 1:
            return True
        return False


class Bishop(Piece):
    value = 325

    position_eval_0 = [
        [-20, -10, -10, -10, -10, -10, -10, -20],
        [-10, 5, 0, 0, 0, 0, 5, -10],
        [-10, 10, 10, 10, 10, 10, 10, -10],
        [-10, 0, 10, 10, 10, 10, 0, -10],
        [-10, 5, 5, 10, 10, 5, 5, -10],
        [-10, 0, 5, 10, 10, 5, 0, -10],
        [-10, 0, 0, 0, 0, 0, 0, -10],
        [-20, -10, -10, -10, -10, -10, -10, -20]
    ]

    position_eval_1 = [
        [-20, -10, -10, -10, -10, -10, -10, -20],
        [-10, 5, 0, 0, 0, 0, 5, -10],
        [-10, 10, 10, 10, 10, 10, 10, -10],
        [-10, 0, 10, 10, 10, 10, 0, -10],
        [-10, 5, 5, 10, 10, 5, 5, -10],
        [-10, 0, 5, 10, 10, 5, 0, -10],
        [-10, 0, 0, 0, 0, 0, 0, -10],
        [-20, -10, -10, -10, -10, -10, -10, -20]
    ]

    def __init__(self, row, col, camp):
        super().__init__(row, col, 3, camp)
        self.name = "b"

    def get_image(self):
        if self.is_selected:
            if self.is_bl_or_wh:
                return "images/black_bishop.gif"
            else:
                return "images/white_bishop.gif"
        else:
            if self.is_bl_or_wh:
                return "images/black_bishop.gif"
            else:
                return "images/white_bishop.gif"

    def get_value(self):
        return Bishop.value

    def position_eval(self, x, y, round, mid=100):
        if round <= mid:
            return Bishop.position_eval_0[x][y]
        else:
            return Bishop.position_eval_1[x][y]

    def is_valid_move(self, board, x, y):
        if x != y and x != -y:
            return False
        count = self.get_between_pieces(board, self.row, self.col, x, y)
        if count != 0:
            return False
        return True


class Rook(Piece):
    value = 500
    position_eval_0 = [
        [0, 0, 0, 5, 5, 0, 0, 0],
        [-5, 0, 0, 0, 0, 0, 0, -5],
        [-5, 0, 0, 0, 0, 0, 0, -5],
        [-5, 0, 0, 0, 0, 0, 0, -5],
        [-5, 0, 0, 0, 0, 0, 0, -5],
        [-5, 0, 0, 0, 0, 0, 0, -5],
        [5, 10, 10, 10, 10, 10, 10, 5],
        [0, 0, 0, 0, 0, 0, 0, 0]
    ]

    position_eval_1 = [
        [0, 0, 0, 5, 5, 0, 0, 0],
        [-5, 0, 0, 0, 0, 0, 0, -5],
        [-5, 0, 0, 0, 0, 0, 0, -5],
        [-5, 0, 0, 0, 0, 0, 0, -5],
        [-5, 0, 0, 0, 0, 0, 0, -5],
        [-5, 0, 0, 0, 0, 0, 0, -5],
        [5, 10, 10, 10, 10, 10, 10, 5],
        [0, 0, 0, 0, 0, 0, 0, 0]
    ]

    def __init__(self, row, col, camp):
        super().__init__(row, col, 2, camp)
        self.name = "r"

    def get_image(self):
        if self.is_selected:
            if self.is_bl_or_wh:
                return "images/black_rook.gif"
            else:
                return "images/white_rook.gif"
        else:
            if self.is_bl_or_wh:
                return "images/black_rook.gif"
            else:
                return "images/white_rook.gif"

    def get_value(self):
        return Rook.value

    def position_eval(self, x, y, round, mid=100):
        if round <= mid:
            return Rook.position_eval_0[x][y]
        else:
            return Rook.position_eval_1[x][y]

    def is_valid_move(self, board, x, y):
        if x != 0 and y != 0:
            return False
        count = self.get_between_pieces(board, self.row, self.col, x, y)
        if count != 0:
            return False
        return True


class Queen(Piece):
    value = 925

    position_eval_0 = [
        [-20, -10, -10, -5, -5, -10, -10, -20],
        [-10, 0, 5, 0, 0, 0, 0, -10],
        [-10, 5, 5, 5, 5, 5, 0, -10],
        [0, 0, 5, 5, 5, 5, 0, -5],
        [-5, 0, 5, 5, 5, 5, 0, -5],
        [-10, 0, 5, 5, 5, 5, 0, -10],
        [-10, 0, 0, 0, 0, 0, 0, -10],
        [-20, -10, -10, -5, -5, -10, -10, -20]
    ]

    position_eval_1 = [
        [-20, -10, -10, -5, -5, -10, -10, -20],
        [-10, 0, 5, 0, 0, 0, 0, -10],
        [-10, 5, 5, 5, 5, 5, 0, -10],
        [0, 0, 5, 5, 5, 5, 0, -5],
        [-5, 0, 5, 5, 5, 5, 0, -5],
        [-10, 0, 5, 5, 5, 5, 0, -10],
        [-10, 0, 0, 0, 0, 0, 0, -10],
        [-20, -10, -10, -5, -5, -10, -10, -20]
    ]

    def __init__(self, row, col, camp):
        super().__init__(row, col, 1, camp)
        self.name = "q"

    def get_image(self):
        if self.is_selected:
            if self.is_bl_or_wh:
                return "images/black_queen.gif"
            else:
                return "images/white_queen.gif"
        else:
            if self.is_bl_or_wh:
                return "images/black_queen.gif"
            else:
                return "images/white_queen.gif"

    def get_value(self):
        return Queen.value

    def position_eval(self, x, y, round, mid=100):
        if round <= mid:
            return Queen.position_eval_0[x][y]
        else:
            return Queen.position_eval_1[x][y]

    def is_valid_move(self, board, x, y):
        if x != y and x != -y and x != 0 and y != 0:
            return False
        count = self.get_between_pieces(board, self.row, self.col, x, y)
        if count != 0:
            return False
        return True


class King(Piece):
    value = 20000

    position_eval_0 = [
        [20, 50, 10, 0, 0, 10, 50, 20],
        [20, 20, 0, 0, 0, 0, 20, 20],
        [-10, -20, -20, -20, -20, -20, -20, -10],
        [-20, -30, -30, -40, -40, -30, -30, -20],
        [-30, -40, -40, -50, -50, -40, -40, -30],
        [-30, -40, -40, -50, -50, -40, -40, -30],
        [-30, -40, -40, -50, -50, -40, -40, -30],
        [-30, -40, -40, -50, -50, -40, -40, -30]
    ]

    position_eval_1 = [
        [-50, -40, -30, -20, -20, -30, -40, -50],
        [-30, -30, 0, 0, 0, 0, -30, -30],
        [-30, -10, 20, 30, 30, 20, -10, -30],
        [-30, -10, 30, 40, 40, 30, -10, -30],
        [-30, -10, 30, 40, 40, 30, -10, -30],
        [-30, -10, 20, 30, 30, 20, -10, -30],
        [-30, -20, -10, 0, 0, -10, -20, -30],
        [-30, -40, -40, -50, -50, -40, -40, -30]
    ]

    def __init__(self, row, col, camp):
        super().__init__(row, col, 0, camp)
        self.is_king=True
        self.name = "k"

    def get_image(self):
        if self.is_selected:
            if self.is_bl_or_wh:
                return "images/black_king.gif"
            else:
                return "images/white_king.gif"
        else:
            if self.is_bl_or_wh:
                return "images/black_king.gif"
            else:
                return "images/white_king.gif"

    def get_value(self):
        return King.value

    def position_eval(self, x, y, round, mid=100):
        if round <= mid:
            return King.position_eval_0[x][y]
        else:
            return King.position_eval_1[x][y]

    def is_valid_move(self, board, x, y):
        if not self.is_moved:
            if self.is_bl_or_wh == False and self.row == 4 and self.col == 0:
                if x == 2 and y == 0:
                    if self.get_between_pieces(board, 4, 0, 3, 0) == 0:
                        return True
                elif x == -2 and y == 0:
                    if self.get_between_pieces(board, 4, 0, -4, 0) == 0:
                        return True
            elif self.is_bl_or_wh == True and self.row == 4 and self.col == 7:
                if x == 2 and y == 0:
                    if self.get_between_pieces(board, 4, 7, 3, 0) == 0:
                        return True
                elif x == -2 and y == 0:
                    if self.get_between_pieces(board, 4, 7, -4, 0) == 0:
                        return True
        if x > 1 or y > 1 or x < -1 or y < -1:
            return False
        return True
