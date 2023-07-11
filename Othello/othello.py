import sys; args = sys.argv[1:]
# Reevu Adakroy, pd. 7

#either takes in two, one, or none
if not args:
    othello_board = '.'*27 + "ox......xo" + '.'*27
    token = 'x'
elif len(args)==2:
    othello_board, token = args
#should have exactly one given
else:
    if len(args) > 1:
        print('bad input')
    if len(args[0])==1:
        token = args[0]
        othello_board = '.'*27 + "ox......xo" + '.'*27
    else:
        othello_board = args[0]
        #token determined by parity of dot count
        token = ['x','o'][othello_board.count('.')%2]

#case insensitive
othello_board = othello_board.lower()
token = token.lower()

def print_board(board):
    for i in range(8):
        print(' '.join([*board[8*i:8*i+8]]))

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

def find_possible_positions(othello_board, direction_dct, token):
    positions_lst = []
    opposing_token = 'xo'.replace(token,'')

    for i in range(len(othello_board)):
        if othello_board[i] != '.': continue

        #go through each of the directions for the point
        for direction in direction_dct[i]:
            #go down the path as far as it leads
            point = i+direction
            #if the path never ends, call it a deadEnd
            deadEnd = False
            while othello_board[point]==opposing_token:
                #the edge of the board has been reached
                if direction not in direction_dct[point]:
                    deadEnd = True
                    break
                point = point+direction
            if not deadEnd and point != i+direction and othello_board[point]==token:
                positions_lst.append(i)
                break
    return positions_lst
    #update all positions

def print_direction_dct(othello_board, direction_dct, i, direction):
    exploded = [*othello_board]
    if direction in direction_dct[i]:
        point = i+direction
        while True:
            exploded[point] = '*'
            new_point = point+direction
            if direction in direction_dct[new_point]:
                point = new_point
            else:
                exploded[new_point] = '*'
                break
    board = ''.join(exploded)
    print_board(board)

#print_direction_dct(othello_board, lookup_board_directions(), 35, 9)
positions_lst = find_possible_positions(othello_board, lookup_board_directions(), token)

exploded = [*othello_board]
for position in positions_lst:
    exploded[position] = '*'

print_board(''.join(exploded))

print(str(positions_lst)[1:-1])

if not positions_lst:
    print('No moves possible')
#print_board(othello_board)