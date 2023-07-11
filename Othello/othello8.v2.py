import sys; args = sys.argv[1:]
# Reevu Adakroy, pd. 7
LIMIT_AB = 14
LIMIT_MIDGAME_AB = 5
GAMESINTOURNAMENT = 100
import random
import time

stats_ctr = {
    'makeMove': 0,'corner': 0,'pass': 0,'wedged_edge': 0,'safe_edge': 0,'no stable': 0,'x-conversion': 0,
    'minimax_pass': 0,'possible_moves cache hit': 0,'unfilled game': 0,'negamax cache hit': 0
}

dir_dct, negamax_dct, mv_lst_dct, stable_dict, corner_dict = {}, {}, {}, {}, {}
combo_boards = []
corner_set, edge_set = set(), set()

di = [-1, -1, -1, 0, 0, 1, 1, 1]
dj = [-1, 0, 1, -1, 1, -1, 0, 1]

def lookup_board_directions():
    global dir_dct
    vis=[[False]*8 for i in range(8)]
    for i in range(64): dir_dct[i] = set()
    flood(0, 0, vis)
    go_through_all_combos()

def flood(rw, cl, vis):
    global dir_dct, corner_set, edge_set

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
    return [ord(mv[0])-105+int(mv[1])*8 if mv[0].isalpha() else int(mv) for mv in moves if mv[0]!='-']

def flip_horizontal(board):
    #create a list of rows
    lst = []
    while board:
        lst+= [board[:8]]
        board = board[8:]
    #reverse the list
    lst = lst[::-1]
    big_lst = []
    for small_lst in lst:
        big_lst+=small_lst
    return big_lst

def rotate_90(board):
    new_board = []
    for i in range(8):
        j=56+i
        while j>=0:
            new_board+=[board[j]]
            j+=-8
    return new_board

def go_through_all_combos():
    #returns a set of all unique strings
    global combo_boards
    board = [i for i in range(64)]

    #rotate 0, 90, 180, 270
    for i in range(3):
        board=rotate_90(board)
        combo_boards += [board]
    board = rotate_90(board)
    #flip horizontal
    combo_boards+=[flip_horizontal(board)]
    #transpose = flip horizontal, rotate 90
    combo_boards+=[rotate_90(flip_horizontal(board))]
    #oppose transpose= rotate 90, flip horizontal
    board = flip_horizontal(rotate_90(board))
    combo_boards+=[board]
    #flip vertical = rotate 90, flip horizontal, rotate 270
    for i in range(3):
        board = rotate_90(board)
    combo_boards+=[board]

def parse_input():
    brd, tkn, mvs = '.'*27+"ox......xo"+'.'*27, 'x', []
    for wrd in args:
        wrd = wrd.lower()
        if len(wrd)==64:
            brd = wrd
            tkn = 'xo'[brd.count('.')%2]
        elif wrd in 'xo': tkn = wrd
        else: mvs.append(wrd)
    return brd, tkn, process_move(mvs)

def print_board(brd):
    for i in range(8): print(' '.join([*brd[8 * i:8 * i + 8]]))

def oppose(token):
    return 'xo'['x'==token]

# path ending token
def pet(brd, eTkn, pnt, dct):
    while brd[pnt] == eTkn and dct in dir_dct[pnt]:
        pnt = pnt + dct
    return pnt, brd[pnt]

def poss_mvs(brd, tkn):
    if (brd, tkn) in mv_lst_dct:
        stats_ctr['possible_moves cache hit']+=1
        return mv_lst_dct[(brd, tkn)]

    pst_lst = {}
    eTkn = oppose(tkn)

    for i in range(len(brd)):
        if brd[i] != '.': continue
        for dct in dir_dct[i]:
            pnt, endTkn = pet(brd, eTkn, i+dct, dct)
            if pnt==i+dct or endTkn!=tkn: continue
            if i not in pst_lst: pst_lst[i] = []
            pst_lst[i]+=[(dct, pnt)]

    mv_lst_dct[(brd, tkn)] = pst_lst

    #add all combos
    # for combo in combo_boards:
    #     new_board = ''.join([brd[combo[i]] for i in range(64)])
    #     new_pst_lst = {}
    #     for poss_mv in pst_lst:
    #         new_poss_mv = combo[poss_mv]
    #         new_pst_lst[new_poss_mv]=[]
    #         for dct, pnt in pst_lst[poss_mv]:
    #             new_pnt = combo[pnt]
    #             new_dct = combo[dct+poss_mv]-combo[poss_mv]
    #             new_pst_lst[new_poss_mv]+=[(new_dct,new_pnt)]
    #     mv_lst_dct[(new_board, tkn)]=new_pst_lst
    return pst_lst

def make_move(brd, tkn, mv, pst_lst):
    brd = brd.replace('*', '.')
    exp = [*brd]
    exp[mv] = tkn

    for dct, end in pst_lst[mv]:
        for pnt in range(mv, end, dct):
            exp[pnt] = tkn
    return ''.join(exp)

def play_corner(poss_mvs):
    for mv in poss_mvs:
        if mv in corner_set:
            stats_ctr['corner']+=1
            return mv

def count_corner(brd,tkn):
    if (brd,tkn) in corner_dict:
        return corner_dict[(brd,tkn)]
    corner_dict[(brd,tkn)]=sum(brd[i]==tkn for i in corner_set)
    return corner_dict[(brd,tkn)]

def count_edges(brd,tkn):
    return sum(brd[i]==tkn for i in edge_set)

def is_move_stable(brd, tkn, mv):
    dct_lst= [1,7,8,9]
    eTkn = oppose(tkn)
    for dct in dct_lst:
        if dct not in dir_dct[mv] or -dct not in dir_dct[mv]: continue
        if pet(brd, eTkn, mv+dct, dct)[1]=='.' and pet(brd, eTkn, mv-dct, -dct)[1]=='.': return False
    return True

def max_stability(brd, tkn, poss_mvs, move_lst):
    maxval = 0
    best_move = poss_mvs[0]
    initial_stable = 0
    for index in range(len(brd)):
        if brd[index] == tkn and is_move_stable(brd, tkn, index):
            initial_stable += 1

    for move in poss_mvs:
        stable_disc_count = 0
        new_board = make_move(brd, tkn, move, move_lst)
        for index in range(len(new_board)):
            if new_board[index] == tkn and is_move_stable(brd, tkn, index):
                stable_disc_count += 1
        if stable_disc_count-initial_stable > maxval:
            maxval = stable_disc_count-initial_stable
            best_move = move

    #if stability isn't increasing, look at sometihng else
    if maxval: return best_move
    else: stats_ctr['no stable']+=1

def remove_x_squares(brd, tkn, poss_mvs, mv_lst):

    prblm = {0:9, 7:14, 56:49, 63:54}
    eTkn = oppose(tkn)

    # don't remove if crnr taken
    for crnr in corner_set:
        if brd[crnr]==tkn: continue

        if prblm[crnr] in poss_mvs:
            if len(poss_mvs) <= 1: return
            poss_mvs.remove(prblm[crnr])

        #remove conversions
        if brd[prblm[crnr]]==eTkn:
            for move in poss_mvs:
                new_board = make_move(brd, tkn, move, mv_lst)
                if new_board[prblm[crnr]]==tkn and new_board[crnr]!=tkn:
                    if len(poss_mvs) <= 1: return
                    stats_ctr['x-conversion']+=1
                    del move

def remove_c_squares(brd, tkn, poss_mvs):
    prblm = {0:[1,8], 7:[6,15], 56:[48,57], 63:[55,62]}
    for crnr in corner_set:
        if brd[crnr]==tkn: continue
        for pos in prblm[crnr]:
            if pos in poss_mvs:
                if len(poss_mvs) <= 1: return
                poss_mvs.remove(pos)

def play_wedged_edge(brd, tkn, mv_lst):
    dct_lst = [1,7,8,9]
    eTkn = oppose(tkn)
    for mv in mv_lst:
        if mv not in edge_set: continue
        for dct in dct_lst:
            if dct in dir_dct[mv] and -dct in dir_dct[mv] and brd[mv+dct]==brd[mv-dct]==eTkn:
                stats_ctr['wedged_edge'] += 1
                return mv

def play_safe_edge(brd, tkn, mv_lst):
    for mv in mv_lst:
        if mv not in edge_set: continue
        if is_move_stable(brd, tkn, mv):
            stats_ctr['safe_edge']+=1
            return mv

def find_best_move(brd, tkn, mv_lst):
    poss_mvs = [*mv_lst]
    if mv:=play_corner(poss_mvs): return mv
    remove_x_squares(brd, tkn, poss_mvs, mv_lst)
    remove_c_squares(brd, tkn, poss_mvs)
    if mv:=play_wedged_edge(brd, tkn, poss_mvs): return mv
    if mv:=play_safe_edge(brd, tkn, poss_mvs): return mv
    if mv:=max_stability(brd, tkn, poss_mvs, mv_lst): return mv
    return poss_mvs[0]

def find_random_move(mv_lst):
    return random.choice([*mv_lst])

def preferred_move(brd, tkn):
    if brd.count('.')<LIMIT_AB: return alphabeta(brd, tkn, -65, 65,LIMIT_AB)[-1]
    return alphabeta(brd, tkn, -65, 65,LIMIT_MIDGAME_AB)[-1]
    # return find_best_move(brd, tkn, mv_lst)

def update_board(brd, mv_lst):
    brd.replace('*','.')
    exp = [*brd]
    for pos in mv_lst: exp[pos] = '*'
    return ''.join(exp)

#returns game transcript, tokenct, enemyct
def playGame(tkn):
    brd, trnscrpt, cur = '.'*27 + "ox......xo" + '.'*27, [], 'x'

    while brd.count('.'):
        mv_lst = poss_mvs(brd, cur)
        if not mv_lst:
            trnscrpt+=[-1]
            stats_ctr['pass'] += 1
            cur = oppose(cur)
            mv_lst = poss_mvs(brd, cur)
        # game over early
        if not mv_lst:
            stats_ctr['unfilled game']+=1
            break

        if cur==tkn: mv = preferred_move(brd,cur)
        else: mv = find_random_move(mv_lst)

        brd = make_move(brd, cur, mv, mv_lst)
        cur = oppose(cur)
        trnscrpt+=[mv]
        stats_ctr['makeMove'] += 1

    return [trnscrpt, brd.count(tkn), brd.count(oppose(tkn))]

def runTournament(gameCnt):

    log = []
    my_tkns = 0
    total = 0

    for i in range(gameCnt):
        tkn='xo'[i%2]
        res = playGame(tkn)
        log+=[(res[1]-res[2],res[0],i,tkn)]
        my_tkns+=res[1]
        total+=res[1]+res[2]

        # add an extra space if single digit
        print(' ' * ((0<=res[1]-res[2]+1<=10)+1)+str(res[1]-res[2]), end='', flush=True)
        if not (i+1)%10: print()
    print()
    print('My token ct: '+str(my_tkns))
    print('Total token ct: ' + str(total))
    print('Score so far: ' + '{0:.3g}'.format(my_tkns*100/total) + '%' +'\n')

    # print bad games
    log.sort()
    print('Game '+str(log[0][2])+' as '+log[0][3]+' => '+str(log[0][0])+': '+' '.join(str(i) for i in log[0][1]))
    print('Game '+str(log[1][2])+' as '+log[1][3]+' => '+str(log[1][0])+': '+' '.join(str(i) for i in log[0][1]))

    # print stats
    print()
    for stat in stats_ctr: print(stat + ': ' + str(stats_ctr[stat]))

def snapshot(brd, tkn, mv):
    if mv!=-1: print(str(tkn)+' moves to '+str(mv))
    poss_mvs, tkn = poss_mvs_turn(brd, tkn)
    print_board(update_board(brd, poss_mvs))
    print('\n'+brd.replace('*','.')+' '+ str(brd.count('x')) + '/' + str(brd.count('o')))
    if poss_mvs: print('Possible moves for ' + str(tkn) + ': '+', '.join([str(i) for i in [*poss_mvs]]))

def poss_mvs_turn(brd, tkn):
    mv_lst = poss_mvs(brd, tkn)
    if not mv_lst:
        tkn = oppose(tkn)
        mv_lst = poss_mvs(brd, tkn)
    return mv_lst, tkn

def print_AB(brd, tkn):
    start_time = time.process_time()
    nm = alphabeta(brd, tkn, -65, 65, LIMIT_AB)
    print("Min score: " + str(nm[0]) + "; move sequence: " + str(nm[1:]))
    print("Elapsed time: " + str(time.process_time()-start_time) +'\n')

def individualMoveProcessing():
    brd, tkn, mvs = parse_input()
    snapshot(brd, tkn, -1)

    mv_lst, tkn = poss_mvs_turn(brd, tkn)

    if not mvs and brd.count('.'):
        move = find_best_move(brd, tkn, mv_lst)
        print("My move is " + str(move))
        best = move
        if brd.count('.') < LIMIT_AB:
            print_AB(brd, tkn)
        else:
            for depth in range(3, 16):
                move = alphabeta(brd, tkn, -65, 65, depth)[-1]
                if move != best:
                    print("My move is " + str(move))
                    best = move

    for mv in mvs:
        mv_lst, tkn = poss_mvs_turn(brd, tkn)
        brd = make_move(brd, tkn, mv, mv_lst)
        snapshot(brd, tkn, mv)
        if brd.count('.'):
            print("My move is: " + str(preferred_move(brd, tkn)))
        tkn = oppose(tkn)

def corner_heuristic(brd,tkn):
    tkn_cnt = count_corner(brd, tkn)
    eTkn_cnt = count_corner(brd, oppose(tkn))
    return 25.0*(tkn_cnt-eTkn_cnt)

def edge_heuristic(brd,tkn):
    tkn_cnt = 0
    eTkn_cnt = 0
    eTkn = oppose(tkn)
    for i in range(64):
        if i not in edge_set: continue
        if brd[i]==tkn: tkn_cnt+=1
        elif brd[i]==eTkn: eTkn_cnt+=1
    if tkn_cnt > eTkn_cnt:
        return (100.0 * tkn_cnt) / (tkn_cnt + eTkn_cnt)
    if tkn_cnt < eTkn_cnt:
        return -(100.0 * eTkn_cnt) / (tkn_cnt + eTkn_cnt)
    return 0

def xc_squares_heuristic(brd, tkn):
    prblm = {0:[1,8,9], 7:[6,14,15], 56:[48,49,57], 63:[54,55,62]}
    eTkn = oppose(tkn)
    tkn_cnt = 0
    eTkn_cnt = 0
    # don't remove if crnr taken
    for crnr in corner_set:
        if brd[crnr]!='.': continue
        for pos in prblm[crnr]:
            if brd[pos]==tkn:
                tkn_cnt+=1
            if brd[pos]==eTkn:
                eTkn_cnt+=1
    if tkn_cnt > eTkn_cnt:
        return -(100.0 * tkn_cnt) / (tkn_cnt + eTkn_cnt)
    if tkn_cnt < eTkn_cnt:
        return (100.0 * eTkn_cnt) / (tkn_cnt + eTkn_cnt)
    return 0

def mobility_heuristic(brd,tkn):
    my_mob=len(poss_mvs(brd,tkn))
    eMob=len(poss_mvs(brd,oppose(tkn)))
    if my_mob > eMob:
        return (100.0 * my_mob) / (my_mob + eMob)
    if my_mob < eMob:
        return -(100.0 * eMob) / (my_mob + eMob)
    return 0


def find_frontier(brd,tkn):
    frontier=0
    for i in range(64):
        if brd[i]!=tkn: continue
        for dct in dir_dct[i]:
            if brd[i+dct]=='.':
                frontier+=1
    return frontier

def frontier_heuristic(brd,tkn):
    my_frontier=find_frontier(brd,tkn)
    eFrontier=find_frontier(brd,oppose(tkn))
    if my_frontier > eFrontier:
        return -(100.0 * my_frontier) / (my_frontier + eFrontier)
    if my_frontier < eFrontier:
        return (100.0 * eFrontier) / (my_frontier + eFrontier)
    return 0

def evaluate_pos(brd,tkn):
    #heuristic, must be scaled between +- 64
    if brd.count(tkn)==0: return -64
    if brd.count(oppose(tkn))==0: return 64
    value = 10*corner_heuristic(brd,tkn)
    value += 2*mobility_heuristic(brd,tkn)
    value += 0.5*xc_squares_heuristic(brd,tkn)
    value += 0.25*frontier_heuristic(brd, tkn)
    #value += 0.25*edge_heuristic(brd, tkn)
    return int(value*64/1275)

# returns best score + reversed move sequence
def alphabeta(brd, tkn, lowerBnd, upperBnd, count):
    eTkn = oppose(tkn)

    if count == -1:
        return [evaluate_pos(brd, tkn)]

    count+=-1
    possible_moves = poss_mvs(brd, tkn)

    if not possible_moves:
        possible_moves = poss_mvs(brd, eTkn)
        #game over
        if not possible_moves: return [brd.count(tkn)-brd.count(eTkn)]

        #eTkn can move but tkn can't
        ab = alphabeta(brd, eTkn, -upperBnd, -lowerBnd, count + 1)
        if len(ab)>1:
            return [-ab[0]] + ab[1:] + [-1]

        return [-ab[0]] # vile score

    if brd.count('.')==1:
        move = [*possible_moves][0]
        tokens_flipped = 0
        for direction, endpoint in possible_moves[move]:
            tokens_flipped += (endpoint - move) // direction -1
        return [brd.count(tkn) - brd.count(eTkn)+2*tokens_flipped+1] + [move]

    best = [lowerBnd-1]
    for mv in possible_moves:
        if mv in corner_set:
            newBrd = make_move(brd, tkn, mv, possible_moves)
            ab = alphabeta(newBrd, eTkn, -upperBnd, -lowerBnd, count)
            score = -ab[0]
            if score < lowerBnd: continue
            if score > upperBnd: return [score]
            best = [score] + ab[1:] + [mv]
            lowerBnd = score + 1
        del mv

    for mv in possible_moves:
        newBrd = make_move(brd,tkn,mv, possible_moves)
        ab = alphabeta(newBrd, eTkn, -upperBnd, -lowerBnd, count)
        score = -ab[0]
        if score < lowerBnd: continue
        if score > upperBnd: return [score]
        best = [score]+ab[1:]+[mv]
        lowerBnd = score+1
    return best


class Strategy:
    # implement all the required methods on your own
    logging = True # turns on logging
    def best_strategy(self, board, player, best_move, running):
        time.sleep(1)
        if running.value:
            lookup_board_directions()
            best_move.value = find_best_move(board, player, poss_mvs(board, player))
            if board.count('.')<=15:
                for depth in range(14,18):
                    best_move.value = alphabeta(board, player, -65, 65, depth)[-1]
            else:
                for depth in range(3,18):
                    best_move.value = alphabeta(board, player, -65, 65, depth)[-1]

def main():
    lookup_board_directions()
    if not args:
        start_time = time.process_time()
        runTournament(GAMESINTOURNAMENT)
        print("Elapsed time: " + str(time.process_time()-start_time))
    else: individualMoveProcessing()

if __name__ == '__main__': main()