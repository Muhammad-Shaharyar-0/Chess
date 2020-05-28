from gui import GUI
from board import *
from algorithm import *
import time
import math
from tkinter import messagebox
import pickle
import copy
import threading


def real_cord(x):
    if x <= 100:
        return 0
    else:
        return (x - 100) / 100 + 1


def board_cord(x):
    return 100 * x + 50


class Game:
    game_opening = ["Default Game", "Custom Game"]
    modes = ["Human vs Human", "Human vs AI"]

    def __init__(self, game_mode=1, opening=0, show_move=True, show_search=False, show_gui=True, save_data=False,load_data=False):
        self.board = Board()
        self.player_turn = False
        self.game_mode = game_mode
        self.opening = opening
        self.show_move = show_move
        self.show_search = show_search
        self.show_gui = show_gui
        self.save_data = save_data
        self.load_data = load_data
        self.view = GUI(self)
        self.ai = AI()

    def set_game_mode(self, mode=1, opening=0):
        self.game_mode = mode
        self.opening = opening

    def set_data(self, show_move=True, show_search=False, show_gui=True, save_data=False):
        self.show_move = show_move
        self.show_search = show_search
        self.show_gui = show_gui
        self.save_data = save_data

    def set_ai(self, ai):
        self.ai = ai



    def set_stage(self, game_mode=1, opening=0, show_move=True, show_search=False, show_gui=True, save_data=False,
                  save_path=r".\Records", ai_name="AlphaBeta", use_pos=False, depth=2,load_data=False):
        self.game_mode = game_mode
        self.opening = opening
        self.show_move = show_move
        self.show_search = show_search
        self.show_gui = show_gui
        self.save_data = save_data
        self.save_path = save_path
        self.load_data=load_data
        self.save_file_name = ""
        if ai_name == "AlphaBeta":
            art_int = AlphaBeta(depth, True, use_pos)
        self.set_ai(art_int)

    def start(self):

        time_info = time.strftime('%Y-%m-%d %H:%M:%S')
        time_label = time.strftime('%Y-%m-%d-%H-%M-%S')

        self.save_file_name = time_label + ".txt"

        msg = time_info + " " + Game.modes[self.game_mode] + " " + Game.game_opening[self.opening]
        msg_ai = ""
        if self.game_mode == 1:
            msg_ai += str(self.ai) + "\n"

        print(msg_ai)
        if self.load_data:
            file = open("Game.pickle", "rb")
            self.board, self.player_turn, self.game_mode, self.save_data = pickle.load(file)
            file.close()
        else:
            self.board.initialize_board(self.opening)
        if self.save_data:
            self.import_data(msg_ai)

        self.view.show_msg("Chess")
        self.view.draw_board(self.board)
        self.view.start()

    def call_back(self, event):
        rx, ry = real_cord(event.x), real_cord(800 - event.y)
        rx=math.floor(rx)
        ry = math.floor(ry)
        self.choose(rx, ry, self.game_mode)

    def move_info(self, move_info):
        game_info = {0: "", 1: " #", 2: " #", 3: " Stalemate", 4: " Draw"}
        return "(" + str(self.board.round) + "):" + move_info + game_info[self.board.status] + ("; " if self.player_turn else ";\n")

    def import_data(self, info):
       # file_name = self.save_path + r'chess-' + self.save_file_name
       # with open(file_name, 'a') as data:
        #    data.write(info)
        file = open("Game.pickle", "wb")
        pickle.dump((self.board, self.player_turn, self.game_mode, self.save_data), file)
        file.close()

    def TurnBack(self):
        file = open("previous.pickle", "rb")
        self.board, self.player_turn= pickle.load(file)
        file.close()
        self.view.draw_board(self.board)

    def choose(self, x, y, mode=0):
        if mode == 0:
            self.pvsp_mode(x, y)
        elif mode == 1:
            self.pvsai_mode(x, y)
        else:
            raise Exception("Invalid game mode: " + str(mode))

    def pvsp_mode(self, rx, ry):
        move_info = self.board.select(rx, ry, self.player_turn)
        if move_info != "":
            self.view.show_msg("White turn" if self.player_turn else "Black turn")
            self.player_turn = not self.player_turn
            self.board.round += 1
            self.board.game_status()
            if self.show_move:
                print(self.move_info(move_info))
            if self.save_data:
                self.import_data(self.move_info(move_info))
        self.view.draw_board(self.board)
        if self.board.status != 0:
            if self.board.status == 1:
                self.Rematch("White player has won the game")
            if self.board.status == 2:
                self.Rematch("Black player has won the game")
            if self.board.status == 3:
                self.Rematch("The game has entered a statlemate")
            if self.board.status == 4:
                self.Rematch("The game has ended in a draw")

    def pvsai_mode(self, rx, ry):
        file = open("previous.pickle", "wb")
        pickle.dump((self.board, self.player_turn), file)
        file.close()
        move_info = self.board.select(rx, ry, self.player_turn)
        self.view.draw_board(self.board)
        if move_info != "":
            self.view.show_msg("White turn" if self.player_turn else "Black turn")
            self.player_turn = not self.player_turn
            self.board.round += 1
            if self.show_move:
                print(self.move_info(move_info))
            if self.save_data:
                self.import_data(self.move_info(move_info))

            self.view.draw_board(self.board)


            move, msg = self.ai.play(self.board, self.player_turn)
            self.board.select(move[0][0], move[0][1], self.player_turn)
            move_info = self.board.select(move[1][0], move[1][1], self.player_turn)
            self.view.show_msg("White turn" if self.player_turn else "Black turn")
            self.player_turn = not self.player_turn
            self.board.round += 1
            if self.show_search:
                print(msg)
                if self.save_data:
                    self.import_data(msg + " ")
            if self.show_move:
                print(self.move_info(move_info))
            if self.save_data:
                self.import_data(self.move_info(move_info))
            self.view.draw_board(self.board)

            self.board.game_status()
            if self.board.status != 0:
                if self.board.status == 1:
                    self.Rematch("White player has won the game")
                if self.board.status == 2:
                    self.Rematch("Black player has won the game")
                if self.board.status == 3:
                    self.Rematch("The game has entered a statlemate")
                if self.board.status == 4:
                    self.Rematch("The game has ended in a draw")

                return
    def Rematch(self,text):
        if not messagebox.askyesno("Result", text+"\nDo You Want A Rematch?"):
            exit()
        else:
            self.board.status = 0
            self.start()