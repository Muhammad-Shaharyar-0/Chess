import tkinter
from tkinter import messagebox
import main
def board_cord(x):
    return 100 * x + 50


class GUI:
    root = tkinter.Tk()
    root.title("Chess")
    root.resizable(0, 0)
    can = tkinter.Canvas(root, width=800, height=800)
    can.pack(expand=tkinter.YES, fill=tkinter.BOTH)
    img = tkinter.PhotoImage(file="images/chess_board.gif")
    can.create_image(0, 0, image=img, anchor=tkinter.NW)
    piece_images = dict()
    move_images = []

    def start(self):
        tkinter.mainloop()


    def draw_board(self, board):
        self.piece_images.clear()
        self.move_images = []
        pieces = board.pieces
        for (x, y) in pieces.keys():
            self.piece_images[x, y] = tkinter.PhotoImage(file=pieces[x, y].get_image())
            self.can.create_image(board_cord(x), board_cord(7 - y), image=self.piece_images[x, y])
        if board.piece_selected:
            self.move_images.append(tkinter.PhotoImage(file="images/select.gif"))
            self.can.create_image(board_cord(board.piece_selected.row), board_cord(7 - board.piece_selected.col), image=self.move_images[-1])
            for (x, y) in board.piece_selected.get_moves(board):
                self.move_images.append(tkinter.PhotoImage(file="images/select.gif"))
                self.can.create_image(board_cord(x), board_cord(7 - y), image=self.move_images[-1])


    def show_msg(self, msg):
        self.root.title(msg)

    def MoveBack(self):
        self.control.TurnBack()

    def __init__(self, control):
        self.control = control
        self.can.bind('<Button-1>', self.control.call_back)
        B = tkinter.Button(self.root, text="Turn Back", command=self.MoveBack, bg="grey")
        B.pack()
