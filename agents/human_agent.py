import random
import gamePlay
from getAllPossibleMoves import getAllPossibleMoves


def nextMove(board, color, sim_time, max_turns, max_sim, percent_wrong,
    movesRemaining, verbose):
        valid_moves = getAllPossibleMoves(board, color)
        print_moves(valid_moves)
        return valid_moves[getValidChoice(1, len(valid_moves)) - 1]

def getValidChoice(lower_bound, upper_bound):
    choice = 0
    while True:
        try:
            choice = int(input("Choice: "))
        except ValueError:
            print("Not an integer!\n")
            continue
        else:
            if choice >= lower_bound and choice <= upper_bound:
                return choice
            else:
                print("Not a valid choice!\n")
            continue

def print_moves(valid_moves):
    print("Valid Moves:")
    for i, move in enumerate(valid_moves):
        print("{}: {} to {}".format(i + 1, move[0], move[1]))

