import sys; args = sys.argv[1:]
# Reevu Adakroy, pd. 7
LIMIT_NM = 9
import random
import time


directions_dct = {}
corner_set = set()
edge_set = set()
almost_corner_set = set()

stats_ctr = {
    'makeMove': 0,
    'corner':0,
    'pass': 0,
    'wedged_edge': 0,
    'safe_edge': 0,
    'no stable': 0,
    'x-conversion': 0,
    'minimax_pass': 0,
    'possible_moves cache hit': 0,
    'unfilled game': 0,
    'negamax cache hit': 0,
    'move cache hit': 0,
    'best move cache hit': 0
    #'salvaged_c': 0
}
negamax_dict = {}
dictionary_of_lst_of_moves = {}
has_move_dict = {}
move_dict = {}
best_move_dict = {}

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
    moves = []

    #adjust for input
    for word in args:
        word = word.lower()
        if len(word)==64:
            othello_board = word
            token = 'xo'[othello_board.count('.') % 2]
        elif word in 'xo': token = word
        else: moves.append(word)

    moves = process_move(moves)

    return othello_board, token, moves

def print_board(board):
    for i in range(8):
        print(' '.join([*board[8*i:8*i+8]]))
    print()
    print(board.replace('*','.') + " " + str(board.count('x')) + '/' + str(board.count('o')))

def oppose(token):
    return 'xo'['x'==token]

def find_possible_moves(othello_board, token):
    if (othello_board, token) in dictionary_of_lst_of_moves:
        stats_ctr['possible_moves cache hit']+=1
        return dictionary_of_lst_of_moves[(othello_board, token)]

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
    dictionary_of_lst_of_moves[(othello_board, token)] = positions_lst
    return positions_lst
    #update all positions

def has_move(othello_board, token):

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
                return True
    return False

def make_move(othello_board, token, move, positions_lst):
    othello_board = othello_board.replace('*', '.')

    if (othello_board, token, move) in move_dict:
        stats_ctr['move cache hit']+=1
        return move_dict[(othello_board, token, move)]

    exploded = [*othello_board]
    exploded[move] = token

    for direction,endpoint in positions_lst[move]:
        for point in range(move, endpoint, direction):
            exploded[point] = token

    move_dict[(othello_board, token, move)] = ''.join(exploded)

    return ''.join(exploded)

def is_move_stable(othello_board, token, move):
    #check all directions
    move_direction_dict = {
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
        move_direction_dict[othello_board[end_point]].add(direction)

    #can it be taken back eventually?
    for direction in move_direction_dict[oppose(token)]:
        if -1*direction in move_direction_dict['.']:
            return False
    for direction in move_direction_dict['.']:
        if -1*direction in move_direction_dict['.']:
            return False
    return True

def remove_x_squares(othello_board, token, possible_moves, lst_of_moves):
    for corner in corner_set:
        #if you already have the corner, it's perfectly fine to play next to it
        if othello_board[corner]==token: continue

        total_direction = 0
        for direction in directions_dct[corner]:
            total_direction+=direction

        if len(possible_moves)>1 and (corner+total_direction) in possible_moves:
            possible_moves.remove(corner+total_direction)

        #remove moves that will convert an x-square as a possibility
        if othello_board[corner+total_direction]==oppose(token):
            for move in possible_moves:
                new_board = make_move(othello_board, token, move, lst_of_moves)
                if new_board[corner+total_direction]==token and new_board[corner]!=token and len(possible_moves)>1:
                    stats_ctr['x-conversion']+=1
                    del move

def remove_c_squares(othello_board, token, possible_moves):
    for corner in corner_set:
        #if you already have the corner, it's perfectly fine to play next to it
        if othello_board[corner]==token: continue

        for direction in directions_dct[corner]:
            #if the list would not be emptied, get rid of the bad move
            if len(possible_moves)>1 and corner+direction in possible_moves:
                # if is_move_stable(othello_board, token, corner+direction):
                #     stats_ctr['salvaged_c']+=1
                #     return corner+direction
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
        if wedged:
            stats_ctr['wedged_edge']+=1
            return move

def play_safe_edge(othello_board, token, possible_moves):
    for move in possible_moves:
        #find the edges
        if move not in edge_set: continue
        if is_move_stable(othello_board, token, move):
            stats_ctr['safe_edge']+=1
            return move


def max_stability(board, token, possible_moves, move_lst):
    best_value = 0
    best_move = possible_moves[0]
    initial_stable = 0
    for index in range(len(board)):
        if board[index] == token and is_move_stable(board, token, index):
            initial_stable += 1

    for move in possible_moves:
        stable_disc_count = 0
        new_board = make_move(board, token, move, move_lst)
        for index in range(len(new_board)):
            if new_board[index] == token and is_move_stable(board, token, index):
                stable_disc_count += 1
        if stable_disc_count-initial_stable > best_value:
            best_value = stable_disc_count-initial_stable
            best_move = move

    #if stability isn't increasing, look at sometihng else
    if best_value>0:
        return best_move
    else:
        stats_ctr['no stable']+=1

def find_best_move(othello_board, token, lst_of_moves):

    # if othello_board.count('.') <= negamax_point_count:
    #     return negamax(othello_board, token)[-1]

    if (othello_board, token) in best_move_dict:
        stats_ctr['best move cache hit']+=1
        return best_move_dict[(othello_board, token)]

    possible_moves = list(lst_of_moves.keys())

    #first go through the dictionary and play to any corners
    for move in possible_moves:
        if move in corner_set:
            stats_ctr['corner']+=1
            return move

    #remove all x-squares
    remove_x_squares(othello_board, token, possible_moves, lst_of_moves)

    #remove all c-squares
    if move:=remove_c_squares(othello_board, token, possible_moves):
        best_move_dict[(othello_board, token)] = move
        return move

    #prefer wedged edges
    if move:=play_wedged_edge(othello_board, token, possible_moves):
        best_move_dict[(othello_board, token)] = move
        return move

    #safe edge covering x.. x.x
    if move:=play_safe_edge(othello_board, token, possible_moves):
        best_move_dict[(othello_board, token)] = move
        return move

    if move:=max_stability(othello_board, token, possible_moves, lst_of_moves):
        best_move_dict[(othello_board, token)] = move
        return move

    best_move_dict[(othello_board, token)] = possible_moves[0]
    return possible_moves[0]

def find_random_move(lst_of_moves):
    return random.choice(list(lst_of_moves.keys()))

def update_board(othello_board, positions_lst):
    exploded = [*othello_board]
    for position in positions_lst:
        exploded[position] = '*'
    return ''.join(exploded)

def playGame(token):
    #each game should stand on its own, so set globals in game
    #returns game transcript, tokenct, enemyct

    #start with empty board
    board = '.'*27 + "ox......xo" + '.'*27
    game_transcript = []
    player = 'x'

    #run until the game is over
    while True:
        possible_moves = find_possible_moves(board, player)

        #if the game ended by the board filling up, don't want to add a -1
        if not board.count('.'): return [game_transcript, board.count(token), board.count(oppose(token))]

        if not possible_moves:
            #add a -1 for pass
            game_transcript.append(-1)
            stats_ctr['pass'] += 1
            #swap to other player
            player = oppose(player)
            possible_moves = find_possible_moves(board, player)
            #if neither player can play then the game is over
            if not possible_moves:
                stats_ctr['unfilled game']+=1
                return [game_transcript, board.count(token), board.count(oppose(token))]

        move = find_random_move(possible_moves)
        if player==token:
            if board.count('.') < LIMIT_NM:
                move = negamax(board, player)[-1]
            else:
                move = find_best_move(board, player, possible_moves)
        board = make_move(board, player, move, possible_moves)
        player = oppose(player)
        game_transcript.append(move)
        stats_ctr['makeMove']+=1

def runTournament(gameCnt):
    game_log = []
    my_tokens = 0
    total_tokens = 0

    # play 300 games
    for i in range(gameCnt):
        token = 'xo'[i % 2]
        res = playGame(token)
        summary = res[1] - res[2]
        game_log.append((summary, i, token, res[0]))
        my_tokens += res[1]
        total_tokens += res[1] + res[2]

        # add an extra space if single digit
        print(' ' * ((0 <= summary < 10) + 1) + str(summary), end='', flush=True)
        # new line after 30
        if not (i + 1) % 10: print()
    print('My token ct: ' + str(my_tokens))
    print('Total token ct: ' + str(total_tokens))
    print('Score so far: ' + '{0:.3g}'.format(my_tokens * 100 / total_tokens) + '%')

    print()

    # print bad games
    game_log.sort()
    print('Game ' + str(game_log[0][1]) + ' as ' + game_log[0][2] + ' => ' + str(game_log[0][0]) + ': ' + str(
        game_log[0][3]).replace(',', '')[1:-1])
    print('Game ' + str(game_log[1][1]) + ' as ' + game_log[1][2] + ' => ' + str(game_log[1][0]) + ': ' + str(
        game_log[1][3]).replace(',', '')[1:-1])

    # print stats
    print()
    for stat in stats_ctr:
        print(stat + ': ' + str(stats_ctr[stat]))

def snapshot(board, token, move):
    if move != -1: print(str(token) + " moves to " + str(move))
    poss_dct = find_possible_moves(board, token)
    board = update_board(board, poss_dct)
    print_board(board)
    if poss_dct:
        print('Possible moves for ' + str(token) + ': ' + str(poss_dct.keys())[11:-2])

def individualMoveProcessing():
    board, token, moves = parse_input()
    snapshot(board, token, -1)

    lst_of_moves = find_possible_moves(board, token)

    if not moves:
        if board.count('.')<=0: return
        start_time = time.process_time()

        print("My move is: " + str(find_best_move(board, token, lst_of_moves)))
        if board.count('.') < LIMIT_NM:
            nm = negamax(board, token)
            print("Min score: " + str(nm[0]) + "; move sequence: " + str(nm[1:]))
            print("Elapsed time: " + str(time.process_time()-start_time))
            print()

    for move in moves:
        new_board = make_move(board, token, move, lst_of_moves)
        snapshot(board, token, move)

        if board.count('.')<=0: return
        print("My move is " + str(find_best_move(board, token, lst_of_moves)))
        if board.count('.') < LIMIT_NM:
            nm = negamax(board, token)
            print("Min score: " + str(nm[0]) + "; move sequence: " + str(nm[1:]))
            print()

        board = new_board
        token = oppose(token)
        lst_of_moves = find_possible_moves(board, token)

def negamax(brd, tkn):
    # returns a list of the best possible score that tkn can
    # achieve, along with an optimal (reversed) move sequence
    # that can get tkn there.

    if (brd, tkn) in negamax_dict:
        stats_ctr['negamax cache hit']+=1
        return negamax_dict[(brd, tkn)]

    eTkn = oppose(tkn)
    possible_moves = find_possible_moves(brd, tkn)
    if not possible_moves:
        possible_moves = has_move(brd, eTkn)
        #game over
        if not possible_moves:
            negamax_dict[(brd, tkn)] = [brd.count(tkn)-brd.count(eTkn)]
            return [brd.count(tkn)-brd.count(eTkn)]
        #eTkn can move but tkn can't
        nm = negamax(brd, eTkn)
        stats_ctr['minimax_pass']+=1
        return [-nm[0]]+nm[1:]+[-1]

    bestSoFar = [-65]
    for mv in list(possible_moves.keys()):
        newBrd = make_move(brd,tkn,mv, possible_moves)
        nm = negamax(newBrd, eTkn)

        if -nm[0] > bestSoFar[0]:
            bestSoFar = [-nm[0]] + nm[1:] + [mv]

    negamax_dict[(brd, tkn)] = bestSoFar
    return bestSoFar

def main():
    lookup_board_directions()
    if not args:
        start_time = time.process_time()
        runTournament(100)
        print("Elapsed time: " + str(time.process_time()-start_time))
    else: individualMoveProcessing()

if __name__ == '__main__': main()