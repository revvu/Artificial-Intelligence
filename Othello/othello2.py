import sys; args = sys.argv[1:]
# Reevu Adakroy, pd. 7

directions_dct = {}

def process_move(move):
    if not move.isnumeric():
        move = ord(move[0]) - 105 + int(move[1]) * 8
    move = int(move)
    return move

def parse_input():
    othello_board = '.' * 27 + "ox......xo" + '.' * 27
    token = 'x'
    move = None

    #adjust for input
    for word in args:
        word = word.lower()
        if len(word)==64:
            othello_board = word
            token = 'xo'[othello_board.count('.') % 2]
        elif word in 'xo': token = word
        else: move = process_move(word)

    return othello_board, token, move

def print_board(board):
    for i in range(8):
        print(' '.join([*board[8*i:8*i+8]]))
    print(board.replace('*','.'))
    print(str(board.count('x')) + '/' + str(board.count('o')))

def lookup_board_directions():
    #corners
    direction_dct = {
        0: {1, 8, 9},
        7: {-1, 7, 8},
        56: {-8, -7, 1},
        63: {-9, -8, -1}
    }
    #edges
    for i in range(1, 7):
        direction_dct[i] = {-1, 1, 7, 8, 9}
    for i in range(8, 56, 8):
        direction_dct[i] = {-8, -7, 1, 8, 9}
    for i in range(15, 63, 8):
        direction_dct[i] = {-9, -8, -1, 7, 8}
    for i in range(57, 63):
        direction_dct[i] = {-9, -8, -7, -1, 1}

    #inner
    for row in range(1,7):
        for col in range(1,7):
            pos = 8*row+col
            direction_dct[pos]={-9, -8, -7, -1, 1, 7, 8, 9}
    return direction_dct

def oppose(token):
    return 'xo'.replace(token, '')

def possible_moves(othello_board, token):

    positions_lst = {}
    opposing_token = oppose(token)

    for i in range(len(othello_board)):
        if othello_board[i] != '.': continue

        #go through each of the directions for the point
        for direction in directions_dct[i]:
            #go down the path as far as it leads
            point = i+direction
            #if the path never ends, call it a deadEnd
            deadEnd = False
            while othello_board[point]==opposing_token:
                #the edge of the board has been reached
                if direction not in directions_dct[point]:
                    deadEnd = True
                    break
                point = point+direction
            if not deadEnd and point != i+direction and othello_board[point]==token:
                if i not in positions_lst: positions_lst[i] = []
                positions_lst[i].append(direction)
    return positions_lst
    #update all positions

def update_board(othello_board, positions_lst):
    exploded = [*othello_board]
    for position in positions_lst:
        exploded[position] = '*'
    return ''.join(exploded)



def make_move(othello_board, token, move, positions_lst):
    othello_board = othello_board.replace('*', '.')
    exploded = [*othello_board]
    exploded[move] = token

    opposing_token = oppose(token)

    for direction in positions_lst[move]:
        point = move + direction
        while exploded[point] == opposing_token:
            exploded[point] = token
            point = point + direction

    return ''.join(exploded), oppose(token)

def main():
    global directions_dct
    directions_dct = lookup_board_directions()

    othello_board, token, move = parse_input()

    poss_dct = possible_moves(othello_board, token)
    #can't go --> pass
    if not poss_dct:
        token = oppose(token)
        poss_dct = possible_moves(othello_board, token)
        print('we are in the bad')

    #othello_board = update_board(othello_board, poss_dct)
    print_board(othello_board)
    print('Possible moves for ' + str(token) + ': ' + str(poss_dct.keys())[11:-2])

    print()

    if move is None: return

    print(token + ' moves to ' + str(move))
    othello_board, token = make_move(othello_board, token, move, poss_dct)
    poss_dct = possible_moves(othello_board, token)
    #can't go --> pass
    if not poss_dct:
        token = oppose(token)
        poss_dct = possible_moves(othello_board, token)
    othello_board = update_board(othello_board, poss_dct)
    print_board(othello_board)
    print('Possible moves for ' + str(token) + ': ' + str(poss_dct.keys())[11:-2])

if __name__ == '__main__': main()