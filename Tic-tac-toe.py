'''
Tic-Tac-Toe game
'''

EMPTY = 1
PLAYERX = 2
PLAYERO = 3 
DRAW = 4
STRMAP = {EMPTY: " ",
          PLAYERX: "X",
          PLAYERO: "O"}

class TTTBoard:
    def __init__(self, dim, reverse = False, board = None):
        self._dim = dim
        self._reverse = reverse
        if board == None:
            self._board = [[EMPTY for dummycol in range(dim)] 
                           for dummyrow in range(dim)]
        else:
            self._board = [[board[row][col] for col in range(dim)] 
                           for row in range(dim)]
            
    def __str__(self):
        rep = ""
        for row in range(self._dim):
            for col in range(self._dim):
                rep += STRMAP[self._board[row][col]]
                if col == self._dim - 1:
                    rep += "\n"
                else:
                    rep += " | "
            if row != self._dim - 1:
                rep += "-" * (4 * self._dim - 3)
                rep += "\n"
        return rep

    def get_dim(self):
        return self._dim
    
    def square(self, row, col):
        return self._board[row][col]

    def get_empty_squares(self):
        empty = []
        for row in range(self._dim):
            for col in range(self._dim):
                if self._board[row][col] == EMPTY:
                    empty.append((row, col))
        return empty

    def move(self, row, col, player):
        if self._board[row][col] == EMPTY:
            self._board[row][col] = player

    def check_win(self):
        lines = []
        lines.extend(self._board)
        cols = [[self._board[rowidx][colidx] for rowidx in range(self._dim)]
                for colidx in range(self._dim)]
        lines.extend(cols)
        diag1 = [self._board[idx][idx] for idx in range(self._dim)]
        diag2 = [self._board[idx][self._dim - idx -1] 
                 for idx in range(self._dim)]
        lines.append(diag1)
        lines.append(diag2)
        for line in lines:
            if len(set(line)) == 1 and line[0] != EMPTY:
                if self._reverse:
                    return switch_player(line[0])
                else:
                    return line[0]
        if len(self.get_empty_squares()) == 0:
            return DRAW
        return None
            
    def clone(self):
        return TTTBoard(self._dim, self._reverse, self._board)


def switch_player(player):
    if player == PLAYERX:
        return PLAYERO
    else:
        return PLAYERX

def play_game(mc_move_function, ntrials, reverse = False):
    board = TTTBoard(3, reverse)
    curplayer = PLAYERX
    winner = None
    while winner == None:
        row, col = mc_move_function(board, curplayer, ntrials)
        board.move(row, col, curplayer)
        winner = board.check_win()
        curplayer = switch_player(curplayer)
        print(board)
        print
        
    if winner == PLAYERX:
        print("X wins!")
    elif winner == PLAYERO:
        print("O wins!")
    elif winner == DRAW:
        print("Tie!")
    else:
        print("Error: unknown winner")



'''
Player
'''

import random

NTRIALS = 1
MCMATCH = 1.0
MCOTHER = 1.0
    
def mc_trial(board, player):
    currently_empty_squares = board.get_empty_squares()
    while currently_empty_squares:
        square = random.choice(currently_empty_squares)
        board.move(square[0], square[1], player)
        currently_empty_squares.remove(square)
        if board.check_win(): 
            break
        player = switch_player(player)

def mc_update_scores(scores, board, player):
    winner = board.check_win()
    for row in range(board.get_dim()):
        for col in range(board.get_dim()):
            player = board.square(row, col)
            if player == PLAYERX:
                if winner == PLAYERX:
                    scores[row][col] += MCMATCH
                elif winner == PLAYERO:
                    scores[row][col] += -MCOTHER
            elif player == PLAYERO:
                if winner == PLAYERX:
                    scores[row][col] += -MCOTHER
                elif winner == PLAYERO:
                    scores[row][col] += MCMATCH
            else:
                pass

def get_best_move(board, scores):
    maximum_score = []
    maximum = float('-inf')
    empty_squares = board.get_empty_squares()
    
    for row in range(board.get_dim()):
        for col in range(board.get_dim()):
            if scores[row][col] > maximum and (row, col) in empty_squares:
                maximum = scores[row][col]
                maximum_score = [(row, col)]
            elif scores[row][col] == maximum and (row, col) in empty_squares:
                maximum_score.append((row, col))

    return random.choice(maximum_score)
        
def mc_move(board, player, trials):
    initial_scores = [[0 for dummy_col in range(board.get_dim())] for dummy_row in range(board.get_dim())]
    for dummy_trial in range(trials):
        cloned = board.clone()
        mc_trial(cloned, player)
        mc_update_scores(initial_scores, cloned, player)
        
    return get_best_move(board, initial_scores)

play_game(mc_move, NTRIALS, False)        
