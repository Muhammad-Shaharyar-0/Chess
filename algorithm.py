import copy
import queue
import random
import threading


class Node:
    def __init__(self, v=0, parent=None):
        self.depth = 0
        self.children = []
        self.parent = parent
        self.value = v

    # is this the bottom?
    def is_leaf(self):
        if self is not None and len(self.children) == 0:
            return True
        else:
            return False

    def get_depth(self):
        if self is not None:
            return self.depth
        else:
            return -1

    def set_depth(self):
        self.depth = self.parent.get_depth() + 1
        if not self.is_leaf():
            for item in self.children:
                item.set_depth()

    def set_parent(self, node):
        if self is not None:
            self.parent = node
            self.set_depth()
            return True
        else:
            raise Exception("Error!")

    def get_nodes(self):
        if self is not None:
            if self.is_leaf():
                return 0
            else:
                count = len(self.children)
                for item in self.children:
                    count += item.get_nodes()
                return count
        else:
            return -1

    def add_child(self, node):
        if self is not None:
            if node is not None:
                node.set_depth()
                self.children.append(node)
                return True
            else:
                return False
        else:
            raise Exception("Error!")

    def remove_children(self):
        if self is not None:
            if not self.is_leaf():
                for item in self.children:
                    item.remove_children()
                self.children = []
                return True
            else:
                return False
        else:
            raise Exception("Error!")


class MinMaxNode(Node):

    def __init__(self, v=0, type=True, info=None, parent=None):
        Node.__init__(self, v, parent)
        self.type = type
        self.info = info

    def get_value(self, a, b):
        if self.is_leaf():
            return self.value
        elif self.type:
            return self.get_max(a, b)
        else:
            return self.get_min(a, b)

    def get_max(self, alpha, beta):
        v = -999999
        for item in self.children:
            v = max(v, item.get_value(alpha, beta))
            if v >= beta:
                self.value = v
                return v
            alpha = max(alpha, v)
        self.value = v
        return v

    def get_min(self, alpha, beta):
        v = 999999
        for item in self.children:
            v = min(v, item.get_value(alpha, beta))
            if v <= alpha:
                self.value = v
                return v
            beta = min(beta, v)
        self.value = v
        return v


# if you want more than ONE AI algorithm to play chess then it will act as a parent class
class AI:
    def __str__(self):
        raise Exception("Virtual method is called.")

    def clear(self):
        raise Exception("Virtual method is called.")

    def play(self, board, camp):
        raise Exception("Virtual method is called.")


class AlphaBeta(AI):
    Infinity = 999999

    def __init__(self, limit, use_value=True, use_position=True):
        self.root = MinMaxNode()
        self.depth_limit = limit
        self.camp = True
        self.use_value = use_value
        self.use_position = use_position
        self.thread_result = queue.Queue()

    def __str__(self):
        msg = "AlphaBeta"
        msg += " - " + "Max Search Depth: " + str(self.depth_limit)
        return msg

    def clear(self):
        self.root.remove_children()

    def play_thread(self, board, camp):
        eva = self.expand(self.root, board, camp, 0, -self.Infinity, self.Infinity)
        self.thread_result.put(eva)

    def play(self, board, camp):
        self.camp = camp
        self.root.type = True
        self.root.remove_children()
        choice = ((-1, -1), (-1, -1))
        choices = []

        thr = threading.Thread(target=self.play_thread, name='thread_ai', args=(board, camp))
        thr.setDaemon(True)
        thr.start()
        thr.join()

        eva = self.thread_result.get()
        count = self.root.get_nodes()
        msg = "Nodes: " + str(count)

        for child in self.root.children:
            if child.value == eva:
                choices.append(child.info)
        random.shuffle(choices)
        if len(choices) != 0:
            choice = choices[0]

        return choice, msg

    def expand(self, node, board, camp, depth, alpha, beta):
        if depth >= self.depth_limit:
            return node.value
        # Max
        elif node.type:
            return self.expand_max(node, board, camp, depth, alpha, beta)
        # Min
        else:
            return self.expand_min(node, board, camp, depth, alpha, beta)

    def expand_max(self, node, board, camp, depth, alpha, beta):
        v = -self.Infinity
        position_move = []
        for position in board.pieces.keys():
            if board.pieces[position].is_bl_or_wh == camp:
                moves = board.pieces[position].get_moves(board)
                for move in moves:
                    position_move.append((position, move))
        random.shuffle(position_move)
        for move in position_move:
            new_board = copy.deepcopy(board)
            new_board.select_ai(move[0], move[1])
            eva = 0
            if depth + 1 >= self.depth_limit:
                if self.use_value:
                    eva += new_board.eval_value(self.camp)
                if self.use_position:
                    eva += new_board.eval_pos(self.camp)
            new_node = MinMaxNode(eva, not node.type, move, node)
            v = max(v, self.expand(new_node, new_board, not camp, depth + 1, alpha, beta))

            # pruning
            if v > beta:
                node.value = v
                node.add_child(new_node)
                return v
            alpha = max(alpha, v)
            node.add_child(new_node)
        if node.is_leaf():
            if not board.is_check(camp):
                v = 0
        node.value = v
        return v

    def expand_min(self, node, board, camp, depth, alpha, beta):
        v = self.Infinity
        position_move = []
        for position in board.pieces.keys():
            if board.pieces[position].is_bl_or_wh == camp:
                moves = board.pieces[position].get_moves(board)
                for move in moves:
                    position_move.append((position, move))
        random.shuffle(position_move)
        for move in position_move:
            new_board = copy.deepcopy(board)
            new_board.select_ai(move[0], move[1])
            eva = 0
            if depth + 1 >= self.depth_limit:
                if self.use_value:
                    eva += new_board.eval_value(self.camp)
                if self.use_position:
                    eva += new_board.eval_pos(self.camp)
            new_node = MinMaxNode(eva, not node.type, move, node)
            v = min(v, self.expand(new_node, new_board, not camp, depth + 1, alpha, beta))

            # Pruning
            if v < alpha:
                node.value = v
                node.add_child(new_node)
                return v
            beta = min(beta, v)
            node.add_child(new_node)
        if node.is_leaf():
            if not board.is_check(camp):
                v = 0
        node.value = v
        return v
