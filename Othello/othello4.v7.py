import sys; args = sys.argv[1:]
import random

# Reevu Adakroy, pd. 7

directions_dct = {}
corner_set = set()
edge_set = set()
almost_corner_set = set()
danger_zone = set()
positional_value_dict = [99,-8,8,6,6,8,-8,99,-8,-24,-4,-3,-3,-4,-24,-8,8,-4,7,4,4,7,-4,8,6,-3,4,0,0,4,-3,6,6,-3,4,0,0,4,
                         -3,6,8,-4,7,4,4,7,-4,8,-8,-24,-4,-3,-3,-4,-24,-8,99,-8,8,6,6,8,-8,99]
stats_ctr = {
    'makeMove': 0,
    'corner':0,
    'pass': 0,
    'wedged_edge': 0,
    'safe_edge': 0,
    'no stable': 0,
    'x-conversion': 0,
    #'salvaged_c': 0
}

#given a board and a token, return preferred move
di = [-1, -1, -1, 0, 0, 1, 1, 1]
dj = [-1, 0, 1, -1, 1, -1, 0, 1]

def lookup_board_directions():
    global directions_dct
    vis=[[False]*8 for i in range(8)]
    for i in range(64): dir_dct[i] = set()
    flood(0, 0, vis)

def flood(rw, cl, vis):
    global directions_dct, corner_set, edge_set

    if vis[rw][cl]: return
    vis[rw][cl]=True
    cnt=0
    for i in range(8):
        if not 0<=rw+di[i]<8 or not 0<=cl+dj[i]<8: continue
        dir_dct[rw*8+cl].add(di[i]*8+dj[i])
        flood(rw+di[i], cl+dj[i], vis)
        cnt+=1

    if cnt==3: corner_set.add(rw*8+cl)
    elif cnt==5: edge_set.add(rw*8+cl)

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
                new_board, useless_token = make_move(othello_board, token, move, lst_of_moves)
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

def play_not_unsafe_edge(othello_board, token, possible_moves):
    #two dot edge
    for move in possible_moves:
        #find the edges
        if move not in edge_set: continue
        for direction in directions_dct[move]:
            if -1*direction in directions_dct[move]:
                if othello_board[move+direction]=='.' and othello_board[move-direction]=='.':
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
        new_board, useless_token = make_move(board, token, move, move_lst)
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
        new_board, useless_token = make_move(board, token, move, move_lst)
        frontier = find_frontier(new_board, token, move, move_lst)-find_frontier(board, token, move, move_lst)

        # stable and evaporate
        move_value = -0*fom(board, token, move, move_lst) \
                     -0*tokens_flipped-0*frontier+0*parity(move,token,f:=find_regions(board))
        if move_value > best_value:
            best_move = move
            best_value = move_value

    #returns the move_value assigned based on stability and evaporation
    return best_move

def find_best_move(othello_board, token, lst_of_moves):

    possible_moves = list(lst_of_moves.keys())

    #first go through the dictionary and play to any corners
    for move in possible_moves:
        if move in corner_set:
            stats_ctr['corner']+=1
            return move

    #remove all x-squares
    remove_x_squares(othello_board, token, possible_moves, lst_of_moves)

    #remove all c-squares
    if move:=remove_c_squares(othello_board, token, possible_moves): return move

    #prefer wedged edges
    if move:=play_wedged_edge(othello_board, token, possible_moves): return move

    #safe edge covering x.. x.x
    if move:=play_safe_edge(othello_board, token, possible_moves): return move

    if move:=max_stability(othello_board, token, possible_moves, lst_of_moves): return move
    # for move in possible_moves:
    #     if is_move_stable(othello_board, token, move):
    #         stats_ctr['stable']+=1
    #         return move

    # for move in possible_moves:
    #      if move in edge_set: return move

    return best_of_the_rest(othello_board, token, possible_moves, lst_of_moves)

def find_random_move(lst_of_moves):
    return random.choice(list(lst_of_moves.keys()))

def playGame(token):
    #each game should stand on its own, so set globals in game
    lookup_board_directions()
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
            if not possible_moves: return [game_transcript, board.count(token), board.count(oppose(token))]

        move = find_random_move(possible_moves)
        if player==token:
            move = find_best_move(board, player, possible_moves)
        board, player = make_move(board, player, move, possible_moves)
        game_transcript.append(move)
        stats_ctr['makeMove']+=1



def main():
    game_log=[]
    my_tokens = 0
    total_tokens = 0

    #play 300 games
    for i in range(300):
        token = random.choice(['x','o'])
        res = playGame(token)
        summary = res[1]-res[2]
        game_log.append((summary, i, token, res[0]))
        my_tokens+=res[1]
        total_tokens+=res[1]+res[2]

        #add an extra space if single digit
        print(' '*((0<=summary<10)+1)+str(summary), end='', flush=True)
        #new line after 30
        if not (i+1)%30: print()
    print('My token ct: ' + str(my_tokens))
    print('Total token ct: ' + str(total_tokens))
    print('Score so far: ' + '{0:.3g}'.format(my_tokens*100 / total_tokens)+'%')

    print()

    #print bad games
    game_log.sort()
    print('Game ' + str(game_log[0][1])+' as '+game_log[0][2]+' => '+str(game_log[0][0])+': '+str(game_log[0][3]).replace(',','')[1:-1])
    print('Game ' + str(game_log[1][1])+' as '+game_log[1][2]+' => '+str(game_log[1][0])+': '+str(game_log[1][3]).replace(',','')[1:-1])

    #print stats
    print()
    for stat in stats_ctr:
        print(stat+': '+str(stats_ctr[stat]))

if __name__ == '__main__': main()