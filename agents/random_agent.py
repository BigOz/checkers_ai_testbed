import random
import gamePlay
from getAllPossibleMoves import getAllPossibleMoves

def nextMove(board, color, sim_time, max_turns, max_sim, percent_wrong,
    movesRemaining, verbose):
    '''Just play randomly among the possible moves'''
    moves = getAllPossibleMoves(board, color)
    chosen_move = random.choice(moves)
    if verbose:
        print("Chosen Move: {} to {}".format(chosen_move[0], chosen_move[1]))
    return chosen_move