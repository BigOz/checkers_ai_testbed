from sys import argv
import time
import getopt
from copy import deepcopy
import gamePlay


def main():
    print('About to run {} games, Red as {}, White as {}'.format(amount,
        args[0],
        args[1]))
    red_wins = 0
    white_wins = 0

    start = time.time()
    for t in range(1, amount + 1):
        result = playGame()
        if result[3] == "Won":
            if result[1] > result[2]:
                red_wins += 1
            else:
                white_wins += 1
        else:
            print(result[3])
        print("Game {}, Red: {}, White: {}".format(t, result[1], result[2]))

    seconds_spent = time.time() - start
    sec_per_game = (seconds_spent / amount)
    print('time: {0:.2f} minutes'.format(seconds_spent / 60))
    print('Red won {}, White won {}'.format(red_wins, white_wins))
    output_file = open(filename, 'a')
    score_string = "{}\n".format(red_wins)
    output_file.write(score_string)

def isAWinner(board):
    red_pieces = 0
    white_pieces = 0
    for row in board:
        for piece in row:
            if piece.upper() == 'R':
                red_pieces += 1
            elif piece.upper() == 'W':
                white_pieces += 1
    if red_pieces == 0:
        return 'w'
    elif white_pieces == 0:
        return 'r'
    else:
        return False

def playGame():
    # Takes as input two functions p1 and p2 (each of which
    # calculates a next move given a board and player color),
    # and returns a tuple containing
    # the final board,
    # pieces left for red,
    # pieces left for white,
    # and status message "Drawn"/"Won"/"Timeout"/"Bad Move"

    board = gamePlay.newBoard()
    movesRemaining = num_rounds + 1

    while movesRemaining > 0:
        movesRemaining -= 1
        if verbose:
            gamePlay.printBoard(board)
        tempBoard = deepcopy(board)
        if movesRemaining % 2 == 0:
            if gamePlay.isAnyMovePossible(board, 'r'):
                nextMove = p_red(tempBoard,
                    'r',
                    red_sim_time,
                    red_max_turns,
                    red_max_sim,
                    red_percent_wrong,
                    deepcopy(movesRemaining),
                    verbose)
                if gamePlay.isLegalMove(board, nextMove, 'r'):
                    gamePlay.doMove(board, nextMove)
                else:
                    return(board, -1, 1, "Bad Move")
            else:
                return(board, 0, 13, "Won")
        else:
            if gamePlay.isAnyMovePossible(board, 'w'):
                nextMove = p_white(tempBoard,
                    'w',
                    white_sim_time,
                    white_max_turns,
                    white_max_sim,
                    white_percent_wrong,
                    deepcopy(movesRemaining),
                    verbose)
                if gamePlay.isLegalMove(board, nextMove, 'w'):
                    gamePlay.doMove(board, nextMove)
                else:
                    return(board, 1, -1, "Bad Move")
            else:
                return(board, 13, 0, "Won")
        winner = isAWinner(board)
        if winner is not False:
            return(board, gamePlay.countPieces(board, 'r'),
                gamePlay.countPieces(board, 'w'), "Won")
    return (board, gamePlay.countPieces(board, 'r'),
        gamePlay.countPieces(board, 'w'), "Drawn")

if __name__ == "__main__":
    try:
        optlist,args = getopt.getopt(argv[1:],'vt:', ["red_max_turns=",
            "red_sim_time=",
            "red_max_sim=",
            "red_percent_wrong=",
            "white_max_turns=",
            "white_sim_time=",
            "white_max_sim=",
            "white_percent_wrong=",
            "filename=",
            "num_games=",
            "num_rounds="])
    except getopt.error:
        print("Usage: python %s {-v} {-t time} player1 player2" % (sys.argv[0]))
        exit()

    verbose = False
    red_sim_time = 10
    red_max_turns = 150
    red_max_sim = float('inf')
    red_percent_wrong = 0
    white_sim_time = 10
    white_max_turns = 150
    white_max_sim = float('inf')
    white_percent_wrong = 0
    filename = "results_test.csv"
    amount = 1
    num_rounds = 150


    for (op,opVal) in optlist:
        if (op == "-v"):
            verbose = True
        elif (op == "--red_sim_time"):
            red_sim_time = float(opVal)
        elif (op == "--red_max_turns"):
            red_max_turns = int(opVal)
        elif (op == "--red_max_sim"):
            red_max_sim = int(opVal)
        elif (op == "--red_percent_wrong"):
            red_percent_wrong = int(opVal)
        elif (op == "--white_sim_time"):
            white_sim_time = float(opVal)
        elif (op == "--white_max_turns"):
            white_max_turns = int(opVal)
        elif (op == "--white_max_sim"):
            white_max_sim = int(opVal)
        elif (op == "--white_percent_wrong"):
            white_percent_wrong = int(opVal)
        elif (op == "--filename"):
            filename = opVal
        elif (op == "--num_games"):
            amount = int(opVal)
        elif (op == "--num_rounds"):
            num_rounds = int(opVal)

    exec("from agents." + args[0] + " import nextMove")
    p_red = nextMove
    exec("from agents." + args[1] + " import nextMove")
    p_white = nextMove
    main()