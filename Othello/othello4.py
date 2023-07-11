import sys; args = sys.argv[1:]
# Reevu Adakroy, pd. 7

directions_dct = {}
corner_set = set()
edge_set = set()
almost_corner_set = set()

#given a board and a token, return preferred move

def process_move(moves):
    updated_moves = []
    for move in moves:
        if not move.isnumeric():
            if move[0]=='-': continue
            move = ord(move[0]) - 105 + int(move[1]) * 8
        move = int(move)
        updated_moves.append(move)
    return updated_moves

def parse_input():
    othello_board = '.' * 27 + "ox......xo" + '.' * 27
    token = 'x'
    #moves = []

    #adjust for input
    for word in args:
        word = word.lower()
        if len(word)==64:
            othello_board = word
            token = 'xo'[othello_board.count('.') % 2]
        elif word in 'xo': token = word
        #else: moves.append(word)

    #moves = process_move(moves)

    return othello_board, token#, moves

def print_board(board):
    for i in range(8):
        print(' '.join([*board[8*i:8*i+8]]))
    print(board.replace('*','.'))
    print(str(board.count('x')) + '/' + str(board.count('o')))

def lookup_board_directions():
    #corners
    global directions_dct, edge_set, corner_set, almost_corner_set
    directions_dct = {
        0: {1, 8, 9},
        7: {-1, 7, 8},
        56: {-8, -7, 1},
        63: {-9, -8, -1}
    }
    corner_set = {0, 7, 56, 63}
    almost_corner_set = {1, 8, 9, 6, 14, 15, 48, 49, 57, 54, 55, 62}
    #edges
    for i in range(1, 7):
        directions_dct[i] = {-1, 1, 7, 8, 9}
        if i not in almost_corner_set:
            edge_set.add(i)
    for i in range(8, 56, 8):
        directions_dct[i] = {-8, -7, 1, 8, 9}
        if i not in almost_corner_set:
            edge_set.add(i)
    for i in range(15, 63, 8):
        directions_dct[i] = {-9, -8, -1, 7, 8}
        if i not in almost_corner_set:
            edge_set.add(i)
    for i in range(57, 63):
        directions_dct[i] = {-9, -8, -7, -1, 1}
        if i not in almost_corner_set:
            edge_set.add(i)

    #inner
    for row in range(1,7):
        for col in range(1,7):
            pos = 8*row+col
            directions_dct[pos]={-9, -8, -7, -1, 1, 7, 8, 9}

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
                positions_lst[i].append((direction, point))
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

    for direction,endpoint in positions_lst[move]:
        for point in range(move, endpoint, direction):
            exploded[point] = token
    return ''.join(exploded), oppose(token)

def single_minmax(othello_board, token, lst_of_moves):
    #given that there are no edges or corners choose the best move given best opponent play
    best_move = -1
    best_score = -65
    score = 0
    #-65 is guaranteed to be less than the net tile change between my turn and opposing

    for possible_move in lst_of_moves:
        for direction, end in lst_of_moves[possible_move]:
            score += (end-possible_move)//direction
        new_board = make_move(othello_board, token, possible_move, lst_of_moves)
        opposing_moves = possible_moves(new_board, oppose(token))
        best_opposing_score = 0
        opposing_score = 0
        for possible_opposing_move in opposing_moves:
            for direction, end in opposing_moves[possible_opposing_move]:
                opposing_score += (end-possible_move)//direction
            if opposing_score > best_opposing_score:
                best_opposing_score = opposing_score
            opposing_score = 0

        #looks ahead one move
        score = score - best_opposing_score

        if score > best_score:
            best_move = possible_move
            best_score = score
        score = 0

def find_best_move(othello_board, token, lst_of_moves):

    #if there is a corner, go there
    corner_dict = {}
    for possible_move in lst_of_moves:
        if possible_move in corner_set:
            corner_dict[possible_move]=lst_of_moves[possible_move]

    #remove possibly dangerous squares
    almost_corner_dict = {}
    for possible_move in lst_of_moves:
        if possible_move in almost_corner_set:
            almost_corner_dict[possible_move]=lst_of_moves[possible_move]

    if len(almost_corner_dict) < len(lst_of_moves):
        for possible_move in almost_corner_dict:
            del lst_of_moves[possible_move]

    edge_dict = {}
    #second preference towards edges
    for possible_move in lst_of_moves:
        if possible_move in edge_set:
            edge_dict[possible_move]=lst_of_moves[possible_move]

    #choose the best one
    if corner_dict: lst_of_moves = corner_dict
    elif edge_dict: lst_of_moves = edge_dict

    return

def main():
    lookup_board_directions()
    othello_board, token = parse_input()

    poss_dct = possible_moves(othello_board, token)
    #can't go --> pass
    if not poss_dct:
        token = oppose(token)
        poss_dct = possible_moves(othello_board, token)

    print(find_best_move(othello_board, token, poss_dct))

if __name__ == '__main__': main()