from piece import *
import copy


class Board:
    max_round = 300
    mid_round = 50

    def __init__(self):
        self.pieces = dict()
        self.status = 0
        self.piece_selected = None
        self.round = 0
        self.last_move = [(-1, -1), (-1, -1)]

    def __str__(self):
        data = ""
        for piece in self.pieces.values():
            data += str(piece)
            data += " "
        return data

    def clear_board(self):
        self.pieces.clear()

    def initialize_board(self, openning=0):
        self.pieces = dict()
        self.piece_selected = None
        self.status = 0
        self.round = 0

        if openning == 0:
            self.default_game()
        elif openning == 1:
            self.custom_game()
        else:
            raise Exception("Error!")

    def default_game(self):

        self.clear_board()

        self.pieces[(4, 0)] = King(4, 0, False)
        self.pieces[(3, 0)] = Queen(3, 0, False)
        self.pieces[(0, 0)] = Rook(0, 0, False)
        self.pieces[(7, 0)] = Rook(7, 0, False)
        self.pieces[(2, 0)] = Bishop(2, 0, False)
        self.pieces[(5, 0)] = Bishop(5, 0, False)
        self.pieces[(1, 0)] = Knight(1, 0, False)
        self.pieces[(6, 0)] = Knight(6, 0, False)
        for item in range(8):
            self.pieces[(item, 1)] = Pawn(item, 1, False)

        self.pieces[(4, 7)] = King(4, 7, True)
        self.pieces[(3, 7)] = Queen(3, 7, True)
        self.pieces[(0, 7)] = Rook(0, 7, True)
        self.pieces[(7, 7)] = Rook(7, 7, True)
        self.pieces[(2, 7)] = Bishop(2, 7, True)
        self.pieces[(5, 7)] = Bishop(5, 7, True)
        self.pieces[(1, 7)] = Knight(1, 7, True)
        self.pieces[(6, 7)] = Knight(6, 7, True)
        for item in range(8):
            self.pieces[(item, 6)] = Pawn(item, 6, True)

    def custom_game(self):
        self.clear_board()

        self.pieces[(4, 0)] = King(4, 0, False)
        self.pieces[(3, 0)] = Queen(3, 0, False)
        self.pieces[(0, 0)] = Rook(0, 0, False)
        self.pieces[(7, 0)] = Rook(7, 0, False)
        self.pieces[(2, 0)] = Bishop(2, 0, False)
        self.pieces[(5, 0)] = Bishop(5, 0, False)
        self.pieces[(1, 0)] = Knight(1, 0, False)
        self.pieces[(6, 0)] = Knight(6, 0, False)
        for item in range(8):
            self.pieces[(item, 1)] = Pawn(item, 1, False)

        self.pieces[(4, 7)] = King(4, 7, True)
        self.pieces[(3, 7)] = Queen(3, 7, True)
        self.pieces[(0, 7)] = Rook(0, 7, True)
        self.pieces[(7, 7)] = Rook(7, 7, True)
        self.pieces[(2, 7)] = Bishop(2, 7, True)
        self.pieces[(5, 7)] = Bishop(5, 7, True)
        self.pieces[(1, 7)] = Knight(1, 7, True)
        self.pieces[(6, 7)] = Knight(6, 7, True)
        for item in range(8):
            self.pieces[(item, 6)] = Pawn(item, 6, True)

    def eval_value(self, camp):
        eval_v = 0
        for item in self.pieces.values():
            if item.is_bl_or_wh == camp:
                eval_v += item.get_value()
            else:
                eval_v -= item.get_value()
        return eval_v

    def eval_pos(self, camp):
        eval_pos = 0
        for item in self.pieces.values():
            # My side
            if item.is_bl_or_wh == camp:
                if not item.is_bl_or_wh:
                    eval_pos += item.position_eval(item.col, item.row, self.round, self.mid_round)
                else:
                    eval_pos += item.position_eval(7 - item.col, item.row, self.round, self.mid_round)
            # Enemy side
            else:
                if not item.is_bl_or_wh:
                    eval_pos -= item.position_eval(item.col, item.row, self.round, self.mid_round)
                else:
                    eval_pos -= item.position_eval(7 - item.col, item.row, self.round, self.mid_round)
        return eval_pos

    def is_under_attack(self, x, y, camp):
        for item in self.pieces.values():
            if item.is_bl_or_wh != camp:
                if item.is_valid_move(self, x - item.row, y - item.col):
                    return True
        return False

    def is_check(self, camp):
        x, y = -1, -1
        for item in self.pieces.values():
            if item.is_king and item.is_bl_or_wh == camp:
                x, y = item.row, item.col
                break
        return self.is_under_attack(x, y, camp)

    def is_stalemate(self):
        if len(self.pieces) == 2:
            return True
        elif len(self.pieces) == 3:
            for item in self.pieces.values():
                if item.piece_type == 3 or item.piece_type == 4:
                    return True
        elif len(self.pieces) == 4:
            i = 0
            pieces_remain = []
            for item in self.pieces.values():
                if item.piece_type != 0:
                    pieces_remain.append(item)
                    i += 1
            if pieces_remain[0].piece_type == 3 and pieces_remain[1].piece_type == 3:
                if pieces_remain[0].is_bl_or_wh != pieces_remain[1].is_bl_or_wh:
                    x0 = pieces_remain[0].row
                    y0 = pieces_remain[0].col
                    x1 = pieces_remain[1].row
                    y1 = pieces_remain[1].col
                    if (x0 + y0) % 2 == (x1 + y1) % 2:
                        return True
            return False

    @staticmethod
    def move_info(x, y):
        asc_ii = ["a", "b", "c", "d", "e", "f", "g", "h"]
        x = int(x) % 8
        return asc_ii[x] + str(int(y) + 1)

    def is_valid_move(self, x, y, dx, dy):
        return self.pieces[x, y].is_valid_move(self, dx, dy)


    def move(self, x, y, dx, dy):
        self.last_move = [(x, y), (x + dx, y + dy)]
        return self.pieces[x, y].move(self, dx, dy)

    # move Back
    def move_(self, position, cord):
        self.last_move = [position, cord]
        return self.pieces[position].move(self, cord[0] - position[0], cord[1] - position[1])

    def remove(self, x, y):
        del self.pieces[x, y]

    def is_castling(self, x, y):
        if x == 2 and y == 0:
            if (4, 0) in self.pieces.keys()  and (0, 0) in self.pieces.keys():
                if self.pieces[(4, 0)].piece_type == 0 and self.pieces[(4, 0)].is_moved == False:
                    if self.pieces[(0, 0)].piece_type == 2 and self.pieces[(0, 0)].is_moved == False:
                        for i in range(1, 5):
                            if self.is_under_attack(i, 0, False):
                                return False
                        return True
        elif x == 6 and y == 0:
            if (4, 0) in self.pieces.keys() and (7, 0) in self.pieces.keys():
                if self.pieces[(4, 0)].piece_type == 0 and self.pieces[(4, 0)].is_moved == False:
                    if self.pieces[(7, 0)].piece_type == 2 and self.pieces[(7, 0)].is_moved == False:
                        for i in range(4, 8):
                            if self.is_under_attack(i, 0, False):
                                return False
                        return True
        elif x == 2 and y == 7:
            if (4, 7) in self.pieces.keys() and (0, 7) in self.pieces.keys():
                if self.pieces[(4, 7)].piece_type == 0 and self.pieces[(4, 7)].is_moved == False:
                    if self.pieces[(0, 7)].piece_type == 2 and self.pieces[(0, 7)].is_moved == False:
                        for i in range(1, 5):
                            if self.is_under_attack(i, 7, True):
                                return False
                        return True
        elif x == 6 and y == 7:
            if (4, 7) in self.pieces.keys() and (7, 7) in self.pieces.keys():
                if self.pieces[(4, 7)].piece_type == 0 and self.pieces[(4, 7)].is_moved == False:
                    if self.pieces[(7, 7)].piece_type == 2 and self.pieces[(7, 7)].is_moved == False:
                        for i in range(4, 8):
                            if self.is_under_attack(i, 7, True):
                                return False
                        return True
        return False

    def castling(self, x, y):
        if x == 2 and y == 0:
            self.pieces[(4, 0)].move(self, -2, 0)
            self.pieces[(0, 0)].move(self, 3, 0)
            return "0-0-0"
        elif x == 6 and y == 0:
            self.pieces[(4, 0)].move(self, 2, 0)
            self.pieces[(7, 0)].move(self, -2, 0)
            return "0-0"
        elif x == 2 and y == 7:
            self.pieces[(4, 7)].move(self, -2, 0)
            self.pieces[(0, 7)].move(self, 3, 0)
            return "0-0-0"
        elif x == 6 and y == 7:
            self.pieces[(4, 7)].move(self, 2, 0)
            self.pieces[(7, 7)].move(self, -2, 0)
            return ""
        return ""

    def pawn_pass_by(self, x, y):
        if self.piece_selected.is_bl_or_wh == False and self.piece_selected.piece_type == 5:
            if self.piece_selected.col == 4:
                if self.pieces[self.last_move[1]].piece_type == 5:
                    if self.last_move[1][1] == 4 and self.last_move[0][1] == 6:
                        if x == self.last_move[1][0] and y == 5:
                            if abs(self.piece_selected.row - x) == 1:
                                self.move_(self.last_move[1], (x, y))
                                return True
        elif self.piece_selected.is_bl_or_wh == True and self.piece_selected.piece_type == 5:
            if self.piece_selected.col == 3:
                if self.pieces[self.last_move[1]].piece_type == 5:
                    if self.last_move[1][1] == 3 and self.last_move[0][1] == 1:
                        if x == self.last_move[1][0] and y == 2:
                            if abs(self.piece_selected.row - x) == 1:
                                self.move_(self.last_move[1], (x, y))
                                return True
        return False

    def pawn_promotion(self, x, y, p_type=1):
        if self.pieces[(x, y)].piece_type == 5 and y == 0 or y == 7:
            camp = self.pieces[(x, y)].is_bl_or_wh
            switch = {
                1: Queen(x, y, camp),
                2: Rook(x, y, camp),
                3: Bishop(x, y, camp),
                4: Knight(x, y, camp),
            }
            self.pieces[(x, y)] = switch.get(p_type, Queen(x, y, camp))
            return True
        return False

    def select(self, x, y, camp):
        if not self.piece_selected:
            if (x, y) in self.pieces and self.pieces[x, y].is_bl_or_wh == camp:
                self.pieces[x, y].is_selected = True
                self.piece_selected = self.pieces[x, y]
            return ""

        moves = self.piece_selected.get_moves(self)

        if (x, y) in moves:
            self.pawn_pass_by(x, y)         # En-Passant Capture

        if not (x, y) in self.pieces.keys():
            if self.piece_selected:
                orig_x, orig_y = self.piece_selected.row, self.piece_selected.col

                # moves = self.piece_selected.get_moves(self)

                if (x, y) in moves:
                    move_info = ""
                    if self.piece_selected.is_king and self.piece_selected.is_moved == False and self.is_castling(x, y):
                        move_info = self.castling(x, y)
                    else:
                        self.move(orig_x, orig_y, x - orig_x, y - orig_y)
                        if self.piece_selected.piece_type == 5:
                            p_type = 1
                            if self.pawn_promotion(x, y, p_type):
                                self.piece_selected.name = Piece.get_name(p_type)
                        if self.is_check(not self.piece_selected.is_bl_or_wh):
                            move_info = self.piece_selected.name + " " + Board.move_info(orig_x, orig_y) + " + " + Board.move_info(x, y)
                        else:
                            move_info = self.piece_selected.name + " " + Board.move_info(orig_x, orig_y) + " - " + Board.move_info(x, y)
                    self.piece_selected.is_moved = True
                    self.piece_selected.is_selected = False
                    self.piece_selected = None
                    return move_info
                else:
                    self.piece_selected = None
            return ""

        if self.pieces[x, y].is_bl_or_wh != camp:
            orig_x, orig_y = self.piece_selected.row, self.piece_selected.col
            if (x, y) in moves:
                self.move(orig_x, orig_y, x - orig_x, y - orig_y)
                if self.piece_selected.piece_type == 5:
                    p_type = 1
                    if self.pawn_promotion(x, y, p_type):
                        self.piece_selected.name = Piece.get_name(p_type)
                if self.is_check(not self.piece_selected.is_bl_or_wh):
                    move_info = self.piece_selected.name + " " + Board.move_info(orig_x, orig_y) + " X " + Board.move_info(x, y)
                else:
                    move_info = self.piece_selected.name + " " + Board.move_info(orig_x, orig_y) + " X " + Board.move_info(x, y)
                self.piece_selected.is_moved = True
                self.piece_selected.is_selected = False
                self.piece_selected = None
                return move_info
            return ""

        for key in self.pieces.keys():
            self.pieces[key].is_selected = False
        self.pieces[x, y].is_selected = True
        self.piece_selected = self.pieces[x,y]
        return ""

    def select_ai(self, position, cord):
        r, c = cord[0], cord[1]
        self.piece_selected = self.pieces[position]
        if self.pieces[position].is_king and self.piece_selected.is_moved == False and self.is_castling(r, c):
            self.castling(r, c)
        else:
            self.pawn_pass_by(r, c)
            self.move_(position, cord)
            if self.piece_selected.piece_type == 5:
                p_type = 1
                self.pawn_promotion(r, c, p_type)

    def game_status(self):
        # 0->Gaming
        # 1->White Win
        # 2->Black Win
        # 3->Stalemate
        # 4->Draw

        count_wh_win = 0
        count_bl_win = 0

        if self.is_stalemate():
            self.status = 4
            return

        for item in self.pieces.values():
            if not item.is_bl_or_wh:
                count_wh_win += len(item.get_moves(self))
            else:
                count_bl_win += len(item.get_moves(self))

        if count_wh_win != 0 and count_bl_win == 0:
            if self.is_check(True):
                self.status = 1

            else:
                self.status = 3
        elif count_bl_win != 0 and count_wh_win == 0:
            if self.is_check(False):
                self.status = 2

            else:
                self.status = 3

        elif count_bl_win == 0 and count_wh_win == 0:
            self.status = 3