# Name      : Vikas Palakurthi
# User ID   : vpalakur
import gamePlay
import random
import time
from copy import deepcopy
from getAllPossibleMoves import getAllPossibleMoves

sim_count = 0

def nextMove(board, color, sim_time, max_turns, max_sim, percent_wrong,
    moves_remaining, verbose):
    moves = getAllPossibleMoves(board, color)
    if len(moves) == 1:
        return moves[0]
    else:
        global sim_count
        sim_count = 0
        move = run_alpha_beta(board, color, sim_time, moves_remaining, moves,
            max_turns, verbose)
        if verbose:
            print(
                "{} simulations performed, {} to {} chosen as best move".format(
                    sim_count, move[0], move[1]))
        return move

def run_alpha_beta(board, color, sim_time, moves_remaining, moves, max_turns,
    verbose):
    op_color = gamePlay.getOpponentColor(color)
    best_val = -1 * float("inf")
    alpha = -1 * float("inf")
    beta = float("inf")
    depth = min(moves_remaining, max_turns)
    random.shuffle(moves)
    start_time = time.time()
    best_moves = [random.choice(moves)]

    for i, move in enumerate(moves):
        if (time.time() - start_time) < sim_time:
            if verbose:
                print("Exploring move {} of {}".format(i + 1, len(moves)))
            new_board = deepcopy(board)
            gamePlay.doMove(new_board, move)
            move_val = evaluation(new_board, color, depth, 'min', op_color,
                alpha, beta, start_time, sim_time)
        if move_val > best_val:
            best_val = move_val
            best_moves = [move]
        elif move_val == best_val:
            best_moves.append(move)
        if best_val > alpha:
            alpha = best_val
    return random.choice(best_moves)


def evaluation(board, color, depth, turn, op_color, alpha, beta, start_time,
    sim_time):
    if depth > 1:
        if turn == 'max':
            moves = getAllPossibleMoves(board, color)
            random.shuffle(moves)
            opti = -1 * float("inf")
            for move in moves:
                if (time.time() - start_time) < sim_time:
                    next_board = deepcopy(board)
                    gamePlay.doMove(next_board, move)
                    opti = max(opti, evaluation(next_board, color, depth - 1,
                        'min', op_color, alpha, beta, start_time, sim_time))
                    alpha = max(alpha, opti)
                    if beta <= alpha:
                        break
            return opti

        elif turn == 'min':
            moves = getAllPossibleMoves(board, op_color)
            random.shuffle(moves)
            opti = float("inf")
            for move in moves:
                if (time.time() - start_time) < sim_time:
                    next_board = deepcopy(board)
                    gamePlay.doMove(next_board,move)
                    opti = min(opti, evaluation(next_board, color, depth - 1,
                        'max', op_color, alpha, beta, start_time, sim_time))
                    beta = min(beta, opti)
                    if beta <= alpha:
                        break
            return opti

    else:
        return get_value(board, color, op_color)

def get_value(board, color, op_color):
    my_pieces = 0
    opponent_pieces = 0
    for row in board:
        for piece in row:
            if piece.upper() == color.upper():
                my_pieces += 1
            elif piece.upper() == op_color.upper():
                opponent_pieces += 1
    global sim_count
    sim_count += 1
    if my_pieces == 0:
        return -1
    elif opponent_pieces == 0:
        return 1
    else:
        return my_pieces - opponent_pieces