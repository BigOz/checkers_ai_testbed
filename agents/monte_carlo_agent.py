import random
import time
import math
from copy import deepcopy
import gamePlay
from getAllPossibleMoves import getAllPossibleMoves

ALL_PLAYERS = {}
WIN_PRIZE = 1
LOSS_PRIZE = 0
TURNS_COUNT = 0
C = math.sqrt(2)

def nextMove(board, color, sim_time, max_turns, max_sim, percent_wrong,
    moves_remaining, verbose):
    global ALL_PLAYERS
    reset(moves_remaining)
    if color in ALL_PLAYERS:
        return ALL_PLAYERS[color].next_move(board, moves_remaining)
    else:
        ALL_PLAYERS[color] = MonteCarlo(color, sim_time, max_turns, max_sim,
            percent_wrong, verbose)
        return ALL_PLAYERS[color].next_move(board, moves_remaining)

def reset(moves_remaining):
    global ALL_PLAYERS
    global TURNS_COUNT
    if moves_remaining > TURNS_COUNT:
        ALL_PLAYERS = {}
    TURNS_COUNT = moves_remaining


class MonteCarlo:

    def __init__(self, color, sim_time, max_turns, max_sim, percent_wrong,
        verbose):
        self.color = color
        self.op_color = gamePlay.getOpponentColor(self.color)
        self.sim_time = sim_time
        self.max_turns = max_turns
        self.max_sim = max_sim
        self.percent_wrong = percent_wrong
        self.state_node = {}
        self.verbose = verbose

    def reset(self):
        self.state_node = {}

    def next_move(self, board, moves_remaining):
        moves = getAllPossibleMoves(board, self.color)
        chosen_move = None
        if random.randint(1, 100) <= self.percent_wrong:
            chosen_move = random.choice(moves)
        else:
            chosen_move = self.monte_carlo_search(board, len(moves),
                moves_remaining)
        if self.verbose:
            print("Chosen Move: {} to {}".format(chosen_move[0],
                chosen_move[1]))
        return chosen_move

    def monte_carlo_search(self, board, len_moves, moves_remaining):
        results = {}
        root = self.get_root(board, len_moves, moves_remaining)
        sim_count = 0
        now = time.time()
        while (time.time() - now) < self.sim_time and (root.moves_unfinished
            > 0 and sim_count < self.max_sim):
            picked_node = self.tree_policy(root)
            result = self.simulate(picked_node)
            self.back_prop(picked_node, result)
            sim_count += 1
        if self.verbose:
            self.print_monte_carlo_results(root, results, sim_count)
        return self.best_action(root)

    def get_root(self, board, len_moves, moves_remaining):
        root = None
        board_string = makeBoardString(board)
        if board_string in self.state_node:
            root = self.state_node[board_string]
        else:
            amnt_children = len_moves
            if amnt_children == 0 and self.isAWinner(board) is False:
                amnt_children = 1
            root = Node(board, None, amnt_children, moves_remaining, self.color)
        root.parent = None
        return root

    def print_monte_carlo_results(self, root, results, sim_count):
        for child in root.children:
            wins, plays = child.get_wins_plays()
            position = convertMoveToString(child.move)
            results[position] = (wins, plays)
        for position in sorted(results, key=lambda x: results[x][1]):
            print('Monte Carlo {}: {}: ({}/{})'.format(self.color,
                position,
                results[position][0],
                results[position][1]))
        print('Monte Carlo {}: {} simulations performed.'.format(self.color,
            sim_count))

    def best_action(self, node):
        most_plays = -float('inf')
        best_wins = -float('inf')
        best_actions = []
        for child in node.children:
            wins, plays = child.get_wins_plays()
            wins += 1
            plays += 2
            if wins > best_wins:
                most_plays = plays
                best_actions = [child.move]
                best_wins = wins
            elif wins == best_wins:
                if plays > most_plays:
                    most_plays = plays
                    best_actions = [child.move]
                elif plays == most_plays:
                    best_actions.append(child.move)
        return random.choice(best_actions)

    def back_prop(self, node, delta):
        while node.parent is not None:
            node.plays += 1
            node.wins += delta
            node = node.parent
        node.plays += 1
        node.wins += delta

    def tree_policy(self, root):
        cur_node = root
        while root.moves_unfinished > 0:
            legal_moves = getAllPossibleMoves(cur_node.board, self.color)
            if not legal_moves:
                break
            elif len(cur_node.children) < len(legal_moves):
                unexpanded = [
                    move for move in legal_moves
                    if move not in cur_node.moves_expanded
                ]
                assert len(unexpanded) > 0
                move = random.choice(unexpanded)
                future_state = deepcopy(cur_node.board)
                gamePlay.doMove(future_state, move)
                child = Node(future_state, move, len(legal_moves),
                    cur_node.turn - 1,
                    gamePlay.getOpponentColor(cur_node.color))
                cur_node.add_child(child)
                board_string = makeBoardString(future_state)
                self.state_node[board_string] = child
                return child
            else:
                # Every possible next state has been expanded, so pick one
                cur_node = self.best_child(cur_node)
        return cur_node

    def best_child(self, node):
        enemy_turn = (node.color != self.color)
        values = {}
        for child in node.children:
            wins, plays = child.get_wins_plays()
            if enemy_turn:
                # the enemy will play against us, not for us
                wins = plays - wins
            _, parent_plays = node.get_wins_plays()
            assert parent_plays > 0
            values[child] = (wins / plays) \
                + C * math.sqrt(2 * math.log(parent_plays) / plays)
        best_choice = max(values, key=values.get)
        return best_choice

    def simulate(self, picked_node):
        board_copy = deepcopy(picked_node.board)
        turns = picked_node.turn
        cur_color = picked_node.color
        op_color = gamePlay.getOpponentColor(cur_color)
        while turns > 0:
            moves = getAllPossibleMoves(board_copy, cur_color)
            if not moves:
                winner = self.isAWinner(board_copy)
                if winner == self.color:
                    return WIN_PRIZE
                elif winner == self.op_color:
                    return LOSS_PRIZE
                else:
                    if cur_color == self.color:
                        return LOSS_PRIZE
                    else:
                        return WIN_PRIZE
            else:
                random_move = random.choice(moves)
                gamePlay.doMove(board_copy, random_move)
                cur_color, op_color = op_color, cur_color
                turns -= 1
        return LOSS_PRIZE

    def isAWinner(self, board):
        my_pieces = 0
        opponent_pieces = 0
        for row in board:
            for item in row:
                if item.upper() == self.color.upper():
                    my_pieces += 1
                elif item.upper() == self.op_color.upper():
                    opponent_pieces += 1
                elif item != ' ':
                    pass
        if my_pieces == 0:
            return self.op_color
        elif opponent_pieces == 0:
            return self.color
        else:
            return False

def convertMoveToString(move):
    move_string = ""
    for item in move:
        move_string += "{}".format(item).zfill(2)
    return move_string

def makeBoardString(board):
    board_string = ''
    for row in board:
        for item in row:
            board_string += item
    return board_string

def numberOfRemainingPieces(board, color):
    piece_count = 0
    for row in board:
        for item in row:
            if item.upper() == color.upper():
                piece_count += 1
    return piece_count

class Node:

    def __init__(self, board, move, amount_children, turn, color):
        self.board = board
        self.plays = 0
        self.wins = 0
        self.children = []
        self.parent = None
        self.moves_expanded = list()
        self.moves_unfinished = amount_children
        self.move = move
        self.turn = turn
        self.color = color

    def propagate_completion(self):
        if self.parent is None:
            return
        if self.moves_unfinished > 0:
            self.moves_unfinished -= 1
        self.parent.propagate_completion()

    def add_child(self, node):
        self.children.append(node)
        self.moves_expanded.append(node.move)
        node.parent = self

    def has_children(self):
        return len(self.children) > 0

    def get_wins_plays(self):
        return self.wins, self.plays

    def __hash__(self):
        return hash(makeBoardString(self.board))

    def __eq__(self, other):
        if not isinstance(other, Node):
            return False
        return self.board == other.board