import sys; args = sys.argv[1:]
import random
import math
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

def find_opposing_mobility(othello_board, token, move, lst_of_moves):
    return len(find_possible_moves(make_move(othello_board, token, move, lst_of_moves), oppose(token)))

#returns a list of lists that are each region
def find_regions(othello_board):
    #complete bfs to find all regions
    points_lst = list(range(64))
    regions = []

    while points_lst:
        chosen_point = points_lst.pop()
        if othello_board[chosen_point] != '.': continue
        subregion = set()
        #conduct bfs on point
        parseMe = [chosen_point]
        while parseMe:
            point = parseMe.pop()
            for direction in directions_dct[point]:
                nbr = point+direction

                if nbr in points_lst:
                    points_lst.remove(nbr)
                    parseMe.append(nbr)
                    subregion.add(nbr)
        regions.append(subregion)
    return regions

def find_best_move(othello_board, token, lst_of_moves, weights):
    best_value = -99999999999999999999999
    best_move = -1
    regions = find_regions(othello_board)

    #how many stable discs right now?
    initial_stable_disc = 0
    for index in range(len(othello_board)):
        if othello_board[index]==token and is_move_stable(othello_board, token, index):
            initial_stable_disc+=-1

    #determine the best spot positionally, with no regard to the current board
    for move in lst_of_moves:

        move_value = 0

        stable_disc_count = initial_stable_disc
        new_board, useless_token = make_move(othello_board, token, move, lst_of_moves)
        for index in range(len(new_board)):
            if new_board[index]==token and is_move_stable(othello_board, token, index):
                stable_disc_count+=1

        #only consider parity if less than 9 spots left on the board
        region_value = 0
        for region in regions:
            if move in region:
                region_value+= (len(region)%2)
                break
        total_flip = 0
        for direction, point in lst_of_moves[move]:
            total_flip+= (point-move)//direction

        total_frontier = 0
        #having made the move, how large is the frontier?
        for index in range(len(new_board)):
            if new_board[index]==token:
                for direction in directions_dct[index]:
                    if index+direction=='.':
                        total_frontier+=1
                        continue

        move_value_lst = [(positional_value_dict[move]+24) /123, stable_disc_count/64,
                          -1*find_opposing_mobility(othello_board, token, move, lst_of_moves)/60, -1*(total_flip-1)/19,
                          -1*total_frontier/64, region_value]

        move_value += sum(z[0]*z[1] for z in zip(move_value_lst, weights))

        if move_value > best_value:
            best_value = move_value
            best_move = move
    return best_move

def find_random_move(lst_of_moves):
    return random.choice(list(lst_of_moves.keys()))

def play_random(weights):
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
            move = find_best_move(othello_board, token, possible_moves, weights)
        othello_board, token = make_move(othello_board, token, move, possible_moves)

def sigmoid(x):
  return 1 / (1 + math.exp(-x))

def main():
    lookup_board_directions()
    good_tokens = 0
    total_tokens = 0
    for x in range(100):
        for i in range(10):
            z = play_random([0,x,0,0,100-x,0])
            good_tokens+=z[0]
            total_tokens+=z[1]
        print(str(x)+ ': ' + str(good_tokens*100 / total_tokens))

if __name__ == '__main__': main()