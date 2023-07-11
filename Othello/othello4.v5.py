import sys; args = sys.argv[1:]
import random

# Reevu Adakroy, pd. 7

directions_dct = {}
corner_set = set()
edge_set = set()
almost_corner_set = set()
positional_value_dict = [99,-8,8,6,6,8,-8,99,-8,-24,-4,-3,-3,-4,-24,-8,8,-4,7,4,4,7,-4,8,6,-3,4,0,0,4,-3,6,6,-3,4,0,0,4,
                         -3,6,8,-4,7,4,4,7,-4,8,-8,-24,-4,-3,-3,-4,-24,-8,99,-8,8,6,6,8,-8,99]

#given a board and a token, return preferred move
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

def oppose(token):
    return 'xo'.replace(token, '')

def find_possible_moves(othello_board, token):
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

def make_move(othello_board, token, move, positions_lst):
    othello_board = othello_board.replace('*', '.')
    exploded = [*othello_board]
    exploded[move] = token

    for direction,endpoint in positions_lst[move]:
        for point in range(move, endpoint, direction):
            exploded[point] = token
    return ''.join(exploded), oppose(token)

def is_move_stable(othello_board, token, move):
    #check all directions
    move_dict = {
        '.':set(),
        'x':set(),
        'o':set()
    }

    for direction in directions_dct[move]:
        #determine the first character at the end of the string of tokens in that direction
        end_point = move+direction
        while othello_board[end_point]==token:
            if direction in directions_dct[end_point]:
                end_point = end_point+direction
            #reached the end and the end is this token
            else: break
        move_dict[othello_board[end_point]].add(direction)

    #can it be taken back eventually?
    for direction in move_dict[oppose(token)]:
        if -1*direction in move_dict['.']:
            return False
    for direction in move_dict['.']:
        if -1*direction in move_dict['.']:
            return False
    return True

def find_stable_token_count(othello_board, token, move, lst_of_moves):
    stable_disc_count = 0
    new_board, useless_token = make_move(othello_board, token, move, lst_of_moves)
    for index in range(len(new_board)):
        if new_board[index] == token and is_move_stable(othello_board, token, index):
            stable_disc_count += 1
    return stable_disc_count

def find_regions(othello_board):
    #complete bfs to find all regions
    points_lst = list(range(64))
    regions = []

    while points_lst:
        chosen_point = points_lst.pop()
        if othello_board[chosen_point] != '.': continue
        subregion = set()
        subregion.add(chosen_point)
        #conduct bfs on point
        parseMe = [chosen_point]
        while parseMe:
            point = parseMe.pop()
            for direction in directions_dct[point]:
                nbr = point+direction

                if nbr in points_lst:
                    points_lst.remove(nbr)
                    if othello_board[nbr]=='.':
                        parseMe.append(nbr)
                        subregion.add(nbr)
        regions.append(subregion)
    return regions

def parity(move, token, regions):
    #white prefers even while black prefers odd
    #regions is a list of sets of points

    #go through regions and find the one that move is in
    target_region = set()
    for region in regions:
        if move in region:
            target_region = region
            break
    if not target_region: print('proble')

    parity = len(target_region)%2
    return token=='o' and parity==0 or (token=='x' and parity==1)

def remove_x_squares(othello_board, token, possible_moves):
    for corner in corner_set:
        #if you already have the corner, it's perfectly fine to play next to it
        if othello_board[corner]==token: continue

        total_direction = 0
        for direction in directions_dct[corner]:
            total_direction+=direction

        #check unbalanced edge case
        #corner must be empty, next to corner must be empty, far corner must be empty
        # if othello_board[corner]=='.':
        #     unbalanced = False
        #     for direction in directions_dct[corner]:
        #         edge = ''
        #         for i in range(1, 8):
        #             edge = edge+othello_board[corner+direction*i]
        #         if token=='x' and edge=='..ooooo.' or (token=='o' and edge=='..xxxxx.'):
        #             #make the new board and make you would be able to move appropriately
        #             new_board = make_move(othello_board, token, corner+total_direction, possible_moves)
        #             new_board = make_move(new_board, oppose(token), corner, possible_moves)
        #             unbalanced = True
        #             break
        #     if unbalanced: continue


        if len(possible_moves)>1 and (corner+total_direction) in possible_moves:
            possible_moves.remove(corner+total_direction)

def remove_c_squares(othello_board, token, possible_moves):
    for corner in corner_set:
        #if you already have the corner, it's perfectly fine to play next to it
        if othello_board[corner]==token: continue

        for direction in directions_dct[corner]:
            #if the list would not be emptied, get rid of the bad move
            if len(possible_moves)>1 and corner+direction in possible_moves:
                possible_moves.remove(corner+direction)

def play_wedged_edge(othello_board, token, possible_moves):
    for move in possible_moves:
        #find the edges
        if move not in edge_set: continue
        #determine if its wedged

        #find appropriate directions to check
        wedged = True
        for direction in directions_dct[move]:
            if -1*direction in directions_dct[move] and othello_board[move + direction]!=oppose(token):
                wedged = False
                break
        if wedged: return move

def play_safe_edge(othello_board, token, possible_moves):
    for move in possible_moves:
        #find the edges
        if move not in edge_set: continue
        if is_move_stable(othello_board, token, move): return move

def fom(othello_board, token, move, lst_of_moves):
    new_board = make_move(othello_board, token, move, lst_of_moves)
    return len(find_possible_moves(new_board, oppose(token)))

def find_frontier(othello_board, token, move, lst_of_moves):
    new_board, useless_token = make_move(othello_board, token, move, lst_of_moves)
    total_frontier = 0
    for index in range(len(new_board)):
        # only consider own token frontier
        if new_board[index] != token: continue
        for direction in directions_dct[index]:
            if index + direction == '.':
                total_frontier += 1
                break

    return total_frontier

def best_of_the_rest(board, token, possible_moves, move_lst):
    #negative number of large magnitude
    best_value = -10**10
    best_move = possible_moves[0]

    for move in possible_moves:
        # find the number of tokens flipped
        tokens_flipped = 0
        for direction, endpoint in move_lst[move]:
            tokens_flipped += (endpoint - move) // direction

        # find the frontier on the new board after this move is played
        frontier = find_frontier(board, token, move, move_lst)

        # stable and evaporate
        move_value = 100*is_move_stable(board, token, move)-0*fom(board, token, move, move_lst) \
                     -0*tokens_flipped-0*frontier+0*parity(move,token,f:=find_regions(board))*(len(f)>4 or board.count('.')<10)
        if move_value > best_value:
            best_move = move
            best_value = move_value

    #returns the move_value assigned based on stability and evaporation
    return best_move

def find_best_move(othello_board, token, lst_of_moves):

    possible_moves = list(lst_of_moves.keys())

    #first go through the dictionary and play to any corners
    for move in possible_moves:
        if move in corner_set: return move

    #remove all x-squares
    remove_x_squares(othello_board, token, possible_moves)

    #remove all c-squares
    remove_c_squares(othello_board, token, possible_moves)

    #prefer wedged edges
    if move:=play_wedged_edge(othello_board, token, possible_moves): return move

    #safe edge covering x.. x.x
    #if move:=play_safe_edge(othello_board, token, possible_moves): return move

    return best_of_the_rest(othello_board, token, possible_moves, lst_of_moves)


    # for move in possible_moves:
    #     if preferred_parity(move, token, find_regions(othello_board)): return move

    #move with preference to parity
    # for move in possible_moves:
    #     if preferred_parity(move, token, find_regions(othello_board)): return move

    #return possible_moves[0]

def find_random_move(lst_of_moves):
    return random.choice(list(lst_of_moves.keys()))

def play_random():
    othello_board = '.'*27 + "ox......xo" + '.'*27
    initial_token = random.choice(['x','o'])
    token = 'x'
    while True:
        possible_moves = find_possible_moves(othello_board, token)
        if not possible_moves:
            token = oppose(token)
            possible_moves = find_possible_moves(othello_board, token)
            if not possible_moves:
                #game over
                return othello_board.count(initial_token), 64 - othello_board.count('.')
        move = find_random_move(possible_moves)
        if token==initial_token:
            move = find_best_move(othello_board, token, possible_moves)
        othello_board, token = make_move(othello_board, token, move, possible_moves)

def main():
    lookup_board_directions()
    good_tokens = 0
    total_tokens = 0
    for x in range(300):
        z = play_random()
        good_tokens+=z[0]
        total_tokens+=z[1]
        if not (x+1)%30: print("*", end='', flush=True)
    print()
    print('300'+ ': ' + str(good_tokens*100 / total_tokens))

    # othello_board = '.'*27 + "ox......xo" + '.'*27
    # regions = find_regions(othello_board)
    # print(regions)

    # othello_board, token = parse_input()
    #
    # poss_dct = find_possible_moves(othello_board, token)
    # #can't go --> pass
    # if not poss_dct:
    #     token = oppose(token)
    #     poss_dct = find_possible_moves(othello_board, token)
    # print(str(poss_dct.keys())[11:-2])
    # print(find_best_move(othello_board, token, poss_dct))

if __name__ == '__main__': main()
else: print('sup')