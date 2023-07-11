import sys; args = sys.argv[1:]
# Reevu Adakroy, pd. 7
LIMIT_AB = 10
LIMIT_MIDGAME_AB = 3
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
    if brd.count('.')<LIMIT_AB: return alphabeta(brd, tkn, -65, 65,LIMIT_AB, True)[-1]
    return alphabeta(brd, tkn, -65, 65,LIMIT_MIDGAME_AB, False)[-1]
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
    nm = alphabeta(brd, tkn, -65, 65, LIMIT_AB, True)
    print("Min score: " + str(nm[0]) + "; move sequence: " + str(nm[1:]))
    print("Elapsed time: " + str(time.process_time()-start_time) +'\n')

def individualMoveProcessing():
    brd, tkn, mvs = parse_input()
    snapshot(brd, tkn, -1)

    mv_lst, tkn = poss_mvs_turn(brd, tkn)

    if not mvs and brd.count('.'):
        if brd in opening_book: print(random.choice([*opening_book[brd]]))
        else:
            # move = find_best_move(brd, tkn, mv_lst)
            # print("My move is " + str(move))
            print("My move is " + str(preferred_move(brd, tkn)))

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
def alphabeta(brd, tkn, lowerBnd, upperBnd, count, terminal):
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
        ab = alphabeta(brd, eTkn, -upperBnd, -lowerBnd, count + 1, terminal)
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
            ab = alphabeta(newBrd, eTkn, -upperBnd, -lowerBnd, count, terminal)
            score = -ab[0]
            if score < lowerBnd: continue
            if score > upperBnd: return [score]
            if terminal and score>0: return [score]+ab[1:]+[mv]
            best = [score] + ab[1:] + [mv]
            lowerBnd = score + 1
        del mv

    for mv in possible_moves:
        newBrd = make_move(brd,tkn,mv, possible_moves)
        ab = alphabeta(newBrd, eTkn, -upperBnd, -lowerBnd, count, terminal)
        score = -ab[0]
        if score < lowerBnd: continue
        if score > upperBnd: return [score]
        if terminal and score > 0: return [score] + ab[1:] + [mv]
        best = [score]+ab[1:]+[mv]
        lowerBnd = score+1
    return best

opening_book = {'...........................ox......xo...........................': {26, 19, 44, 37}, '..........................xxx......xo...........................': {18, 34, 20}, '..................o.......xox......xo...........................': {19, 44, 37}, '..................ox......xxx......xo...........................': {34, 20}, '..................ox......oxx.....ooo...........................': {33, 9, 41, 43, 45, 17, 25}, '.................xxx......oxx.....ooo...........................': {29}, '.................xxx......oooo....ooo...........................': {33}, '.................xxx......xooo...xooo...........................': {25}, '.................xxx.....ooooo...xooo...........................': {42}, '.................xxx.....oxooo...xxoo.....x.....................': {43}, '.................xxx.....oxooo...xooo.....xo....................': {37}, '..................ox.....xxxx.....ooo...........................': {11, 20}, '...........o......oo.....xxox.....ooo...........................': {10, 43, 12}, '..........xo......xx.....xxox.....ooo...........................': {29}, '..........xo......xx.....xxooo....ooo...........................': {43}, '..........xo......xx.....xxxoo....xxo......x....................': {42}, '..........xo......xx.....xxxoo....xoo.....ox....................': {37}, '..........xo......xx.....xxxxo....xxxx....ox....................': {44}, '..........xo......xx.....xxxxo....xxxx....ooo...................': {53}, '..................ox......oxx.....xoo....x......................': {42, 20}, '..................ox......oxx.....ooo....xo.....................': {33}, '..................ox......oxx.....oxo......x....................': {20, 29}, '..................ox......oooo....oxo......x....................': {25, 37}, '..................ox.....xoooo....xxo......x....................': {41, 42, 20}, '..................ox.....xoooo....oxo....o.x....................': {33}, '..................ox.....xxooo...xxxo....o.x....................': {42}, '..................ox.....xoooo...xooo....oox....................': {17, 37}, '..................ox.....xoooo....ooo.....ox....................': {33}, '..................ox.....xxooo...xooo.....ox....................': {17}, '.................oox.....xoooo...xooo.....ox....................': {41}, '.................oox.....xoooo...xooo....xxx....................': {20}, '.................oooo....xoooo...xooo....xxx....................': {10}, '..........x......oxoo....xxooo...xxoo....xxx....................': {24}, '..........x......oxoo...oooooo...xxoo....xxx....................': {32}, '..........x......oxoo...oxoooo..xxxoo....xxx....................': {40}, '..........x......oxoo...oxoooo..ooxoo...oxxx....................': {11}, '..................ooo....xoooo....xxo......x....................': {17}, '..................ox......ooxo....oxxx.....x....................': {11, 44}, '...........o......oo......ooxo....oxxx.....x....................': {33, 30}, '...........o......oo......ooxxx...oxxx.....x....................': {51}, '..................ox......ooxo....ooxx.....xo...................': {42, 45}, '..................ox......ooxo....oxxx....xxo...................': {51}, '..................ox......oxx.....oox........x..................': {37, 12, 20}, '............o.....oo......oxx.....oox........x..................': {42}, '..................ooo.....oox.....oox........x..................': {42}, '..................ooo.....oox.....oxx.....x..x..................': {37}, '..................ooo.....ooo.....oooo....x..x..................': {29}, '..................ooo.....ooox....ooox....x..x..................': {38}, '..................ooo.....xxo......xo...........................': {9, 10, 11, 12, 13, 45, 29}, '..........x.......xoo.....xxo......xo...........................': {43}, '..........x.......xoo.....xoo......oo......o....................': {12}, '..........x.x.....xxo.....xoo......oo......o....................': {11}, '..........xox.....xoo.....xoo......oo......o....................': {21}, '..........xox.....xxxx....xoo......oo......o....................': {29}, '..........xox.....xxox....xooo.....oo......o....................': {44}, '...........x......oxo.....xxo......xo...........................': {25, 34}, '...........x......oxo....oooo......xo...........................': {17, 29, 33}, '...........x.....xxxo....oxoo......xo...........................': {43}, '...........x.....xxxo....oxoo......oo......o....................': {29}, '...........x.....xxxx....oxxxx.....oo......o....................': {21}, '...........x.....xxxxo...oxxox.....oo......o....................': {44}, '...........x.....xxxxo...oxxxx.....xx......ox...................': {37}, '...........x.....xxxxo...oxxxo.....xxo.....ox...................': {46}, '.............x....oox.....xxo......xo...........................': {34, 21}, '.............x....oooo....xxo......xo...........................': {12}, '..................ooo.....xxxx.....xo...........................': {34, 43}, '..................ooo.....xoxx.....oo......o....................': {11, 44}, '...........x......oox.....xoxx.....oo......o....................': {34, 21, 13}, '...........x......oox.....ooxx....ooo......o....................': {10}, '...........x.o....ooo.....xoxx.....oo......o....................': {12}, '...........xxo....oxx.....xoxx.....oo......o....................': {21}, '...........xxo....oooo....xoox.....oo......o....................': {10, 44}, '...........x......oooo....xoox.....oo......o....................': {12}, '...........xx.....oxoo....xoox.....oo......o....................': {10}, '..........oxx.....oooo....xoox.....oo......o....................': {13}, '..........oxxx....ooox....xoox.....oo......o....................': {34}, '..........oxxx....ooox....ooox....ooo......o....................': {17}, '..........oxxx...xxxxx....ooox....ooo......o....................': {3}, '...o......ooxx...xxoxx....ooox....ooo......o....................': {4}, '...ox.....oxxx...xxoxx....ooox....ooo......o....................': {5}, '...ooo....oxox...xxoxx....ooox....ooo......o....................': {25}, '..................ooo.....xoxx.....xx......ox...................': {25, 37}, '..................ooo....oooxx.....xx......ox...................': {51, 12}, '..................ooo....oooxx.....xx......xx......x............': {30}, '..................ooo.....xoox.....xxo.....ox...................': {45, 21}, '..................ooox....xoxx.....xxo.....ox...................': {30}, '..................ooo.....xxo......xx........x..................': {33, 34, 44}, '..................ooo.....oxo....o.xx........x..................': {21}, '..................ooo.....ooo.....oxx........x..................': {21}, '..................ooox....oox.....oxx........x..................': {44}, '..................ooox....ooo.....ooo.......ox..................': {43}, '..................ooox....ooo.....ooo......xxx..................': {52}, '..................o.......xox......xx.......x...................': {34}, '..................o.......xox......xxx..........................': {34}, '....................o.....xxo......xo...........................': {45, 37, 29}, '....................o.....xxxx.....xo...........................': {34}, '....................o.....xoxx....ooo...........................': {43, 44}, '....................o.....xoxx....oox......x....................': {44, 21}, '....................oo....xoox....oox......x....................': {42, 19, 12, 44}, '...................xoo....xxox....oxx......x....................': {18}, '....................oo....xoox....oxx......xx...................': {18, 42}, '..................o.oo....ooox....oxx......xx...................': {19}, '..................oxoo....oxox....oxx......xx...................': {12}, '............o.....oooo....oxox....oxx......xx...................': {33, 11, 41}, '............o.....oooo....oxox...xxxx......xx...................': {37}, '............o.....oooo....oxoo...xxxxo.....xx...................': {17, 25}, '............o.....oooo...xxxoo...xxxxo.....xx...................': {45}, '............o.....oooo...xxooo...xxxoo.....xxo..................': {10}, '..........x.o.....xooo...xxooo...xxxoo.....xxo..................': {52}, '..........x.o.....xooo...xxooo...xxxoo.....xoo......o...........': {11}, '..........xxo.....xxoo...xxxoo...xxxoo.....xoo......o...........': {50}, '............o.....oooo....oxox....xxx....x.xx...................': {37}, '............o.....oooo....oxoo....xxxo...x.xx...................': {25, 38}, '............o.....oooo...xxxoo....xxxo...x.xx...................': {45}, '............o.....oooo...xxooo....xxoo...x.xxo..................': {38}, '............o.....oooo...xxooo....xxxxx..x.xxo..................': {51}, '............o.....oooo....oxoo....xxxxx..x.xx...................': {45}, '....................o.....xxo......xxx..........................': {25, 44}, '....................o....oooo......xxx..........................': {21}, '....................ox...ooox......xxx..........................': {29}, '....................ox...ooooo.....xxx..........................': {12}, '............x.......xx...oooxo.....xxx..........................': {44}, '............x.......xx...oooxo.....oxx......o...................': {38}, '............x.......xx...oooxx.....oxxx.....o...................': {45}, '............x.......xx...oooxx.....ooxx.....oo..................': {43}, '............x.......xx...oooxx.....oxxx....xoo..................': {42}, '....................o.....xxo......xox......o...................': {19, 29}, '....................o.....xxxx.....xox......o...................': {34}, '....................o.....xoxx....ooox......o...................': {43}, '....................o.....xoxx....ooxx.....xo...................': {42}, '....................o.....xoxx....ooxx....ooo...................': {53}, '....................o.....xoxx....oxxx....oox........x..........': {21, 38}, '....................o.....xoxo....ooooo...oox........x..........': {46}, '....................o.....xxo......xx........x..................': {25, 44}, '....................o.....xxo......xo.......ox..................': {37}, '....................o.....xxo......xxx......ox..................': {34, 46}, '....................o.....xoo.....oxxx......ox..................': {43, 18, 19, 29}, '..................x.o.....xxo.....oxxx......ox..................': {25, 42, 38}, '..................x.o....oooo.....oxxx......ox..................': {43}, '..................x.o....oooo.....oxxx.....xxx..................': {42}, '..................x.o....oooo.....ooxx....oxxx..................': {33}, '..................x.o....oooo....xxxxx....oxxx..................': {40}, '..................x.o....oooo....oxxxx..o.oxxx..................': {41}, '..................x.o....oooo....oxxxx..oxxxxx..................': {50}, '....................o.....xxxx....oxxx......ox..................': {46, 38}, '....................o.....xxxo....ooooo.....ox..................': {30}, '....................o.....xxxxx...ooooo.....ox..................': {21}, '....................oo....xxoox...ooooo.....ox..................': {42}, '....................oo....xxoox...xoooo...x.ox..................': {19}, '...................ooo....xooox...xoooo...x.ox..................': {43}, '...................ooo....xooox...xoooo...xxxx..................': {17}, '.................o.ooo....oooox...xoooo...xxxx..................': {18}, '.................oxooo....xxoox...xoxoo...xxxx..................': {25}, '.................oxooo...ooooox...xoxoo...xxxx..................': {12}, '............x....oxoxx...oooxox...xoxoo...xxxx..................': {41}, '....................o.....xxxx....oxxx......ooo.................': {53}, '....................o.....xxxx....oxxx......xxo......x..........': {19}, '...................x.......xx......xo...........................': {18, 34, 20}, '..................ox.......ox......xo...........................': {26, 44, 37}, '..................ox.......ox......xx.......x...................': {20}, '..................ox.......ox......xxx..........................': {20}, '...................x.......xx.....ooo...........................': {43, 44, 45}, '...................x.......xx.....oxo......x....................': {20}, '...................xo......oo.....oxo......x....................': {37, 29}, '...................xo......oox....oxx......x....................': {42, 37}, '...................xo......oox....oox.....ox....................': {33, 26, 37, 21}, '...................xo.....xxxx....oox.....ox....................': {18}, '...................xo......oxx....ooxx....ox....................': {18, 21}, '..................ooo......oxx....ooxx....ox....................': {26}, '..................ooo.....xxxx....ooxx....ox....................': {33}, '..................ooo.....oxxx...oooxx....ox....................': {25, 12, 13}, '............x.....oox.....oxxx...oooxx....ox....................': {44}, '............x.....oox.....oxxx...oooxx....ooo...................': {10, 11}, '...........xx.....oxx.....oxxx...oooxx....ooo...................': {45}, '...........xx.....oxx.....ooxx...oooox....oooo..................': {17}, '...........xx....xxxx.....ooxx...oooox....oooo..................': {38}, '...........xx....xxxx.....ooxx...oooooo...oooo..................': {25}, '...........xx....xxxx....xxxxx...oooooo...oooo..................': {22}, '.............x....oox.....oxxx...oooxx....ox....................': {44}, '.............x....oox.....oxxx...oooxx....ooo...................': {11, 52}, '...........x.x....oxx.....oxxx...oooxx....ooo...................': {45}, '...........x.x....oxx.....ooxx...oooox....oooo..................': {52}, '...........x.x....oxx.....ooxx...oooxx....ooxo......x...........': {30}, '.............x....oox.....oxxx...oooxx....oox.......x...........': {45}, '...................x.......xx.....oox.......x...................': {11, 37}, '...........o.......o.......ox.....oox.......x...................': {42}, '...........o.......o.......ox.....oxx.....x.x...................': {43}, '...........o.......o.......ox.....oox.....xox...................': {33}, '...........o.......o.......ox....xxxx.....xox...................': {37}, '...........o.......o.......oo....xxxxo....xox...................': {52}, '...........o.......o.......oo....xxxxo....xxx.......x...........': {45}, '...........o.......o.......oo....xxxoo....xxxo......x...........': {29}, '...........o.......o.......oox...xxxxo....xxxo......x...........': {21}, '...................x.......xx.....oooo......x...................': {26, 43}, '...................x.......xx.....oxoo.....xx...................': {20}, '...................xo......oo.....oxoo.....xx...................': {29}, '...................xo......oox....oxxo.....xx...................': {21}, '...................xoo.....ooo....oxxo.....xx...................': {46}, '...................xoo.....oxo....oxxx.....xx.x.................': {42, 52}, '...................xoo.....ooo....oxox.....oo.x.....o...........': {53}, '...................x.......xx.....oox........x..................': {11, 37}, '...................x.......xx.....oooo.......x..................': {44}, '...................x.......xx.....ooxo......xx..................': {20, 53}, '...................xo......ox.....ooxo......xx..................': {43, 18, 26, 29}, '..................xxo......xx.....ooxo......xx..................': {11, 52, 21}, '...........o......xoo......ox.....ooxo......xx..................': {29}, '...........o......xoo......oxx....ooxx......xx..................': {21}, '...........o......xooo.....oox....ooxx......xx..................': {12}, '...........ox.....xoxo.....oxx....ooxx......xx..................': {5}, '.....o.....oo.....xoxo.....oxx....ooxx......xx..................': {13}, '.....o.....oox....xoxx.....oxx....ooxx......xx..................': {22}, '...................xo......xx.....oxxo.....xxx..................': {52, 53}, '...................xo......xo.....oxoo.....oox......o...........': {51}, '...................xo......xo.....oxoo.....xox.....xo...........': {42}, '...................xo......xo.....oooo....ooox.....xo...........': {21}, '...................xxx.....xo.....oooo....ooox.....xo...........': {26}, '...................xxx....ooo.....oooo....ooox.....xo...........': {29}, '...................xxx....ooox....ooox....ooox.....xo...........': {10}, '..........o........oxx....ooox....ooox....ooox.....xo...........': {18}, '..........o.......xxxx....oxox....ooxx....ooox.....xo...........': {11}, '..........oo......xoxx....ooox....ooxx....ooox.....xo...........': {33}, '..........oo......xoxx....ooox...xxxxx....xoox.....xo...........': {13}, '...................xo......xx.....oxxo.....xxo.......o..........': {46}, '...................xo......xx.....oxxx.....xxxx......o..........': {26}, '...........................ox......xx.......x...................': {45, 43, 29}, '...........................ooo.....xx.......x...................': {18, 19, 20}, '..................x........xoo.....xx.......x...................': {26, 52}, '..................x.......oooo.....xx.......x...................': {19}, '..................xx......oxoo.....xx.......x...................': {10, 43}, '..................xx......oxoo.....xo......ox...................': {34, 45, 20, 37}, '..................xxx.....oxxo.....xx......ox...................': {10, 11}, '..........o.......oxx.....oxxo.....xx......ox...................': {17}, '..........o......xxxx.....xxxo.....xx......ox...................': {37}, '...........o......xoo.....ooxo.....ox......ox...................': {12}, '...........ox.....xox.....ooxo.....ox......ox...................': {21}, '...........ox.....xooo....oooo.....ox......ox...................': {42}, '...........ox.....xooo....oooo.....ox.....xxx...................': {37}, '...........ox.....xooo....oooo.....ooo....xxx...................': {34}, '...........ox.....xooo....xooo....xooo....xxx...................': {53}, '...........ox.....xooo....xooo....xooo....xxo........o..........': {45}, '...........ox.....xooo....xxoo....xoxo....xxxx.......o..........': {52}, '...........ox.....xooo....xxoo....xooo....xxox......oo..........': {30}, '...........ox.....xoox....xxxxx...xooo....xxox......oo..........': {50}, '..................xx......oxoo.....xx......oxx..................': {42, 11, 52}, '..................xx......oxoo.....xo......oox......o...........': {34}, '..................xx......xxoo....xxo......oox......o...........': {42}, '..................xx......xxoo....xoo.....ooox......o...........': {51}, '..................xx......xxoo....xxo.....oxox.....xo...........': {58}, '..................xx......xxoo....xxo.....oxox.....oo.....o.....': {50}, '..................xx......xxoo....xxo.....xxox....xoo.....o.....': {41}, '...................x.......xoo.....xx.......x...................': {26, 52}, '...................x......oooo.....xx.......x...................': {20, 37}, '...................xx.....ooxo.....xx.......x...................': {43}, '...................xx.....ooxo.....oo......ox...................': {34}, '...................xx.....oxxo....xoo......ox...................': {42}, '...................xx.....oxxo....ooo.....oox...................': {17}, '.................x.xx.....xxxo....oxo.....oox...................': {11, 21}, '...........o.....x.oo.....xoxo....ooo.....oox...................': {10}, '...................x.......xoo.....xo.......o.......o...........': {21}, '...................x.x.....xxo.....xo.......o.......o...........': {20}, '...................xox.....xoo.....xo.......o.......o...........': {30}, '...................xox.....xxxx....xo.......o.......o...........': {26}, '...................xox....oxxxx....oo.......o.......o...........': {11}, '...........x.......xxx....oxxxx....oo.......o.......o...........': {18}, '...........x......oxxx....ooxxx....oo.......o.......o...........': {34}, '...........x......oxxx....oxxxx...xoo.......o.......o...........': {42}, '....................x......oxo.....xx.......x...................': {43}, '....................x......oxo.....oo......ox...................': {26, 34}, '....................x......xxo....xoo......ox...................': {26, 21}, '....................xo.....xoo....xoo......ox...................': {26, 42, 37, 30}, '....................xo....xxoo....xxo......ox...................': {42, 45}, '....................xo....xxoo....xxo......ooo..................': {37}, '....................xo....xxoo....xxxx.....ooo..................': {30}, '....................xo....xxooo...xxxo.....ooo..................': {50, 51, 38}, '....................xo....xxooo...xxxo.....xoo....x.............': {19}, '...................ooo....xxooo...xxxo.....xoo....x.............': {11, 52}, '...........x.......xoo....xxooo...xxxo.....xoo....x.............': {18}, '...................ooo....xxooo...xxxo.....xxo....x.x...........': {18}, '..................oooo....xoooo...xxoo.....xxo....x.x...........': {11}, '...........x......oxoo....xxooo...xxoo.....xxo....x.x...........': {33}, '....................xo....xxooo...xxxo.....xoo.....x............': {19}, '...................ooo....xxooo...xxxo.....xoo.....x............': {52, 53}, '...................ooo....xxooo...xxxo.....xxo.....xx...........': {18}, '..................oooo....xoooo...xxoo.....xxo.....xx...........': {46}, '..................oooo....xoooo...xxoo.....xxxx....xx...........': {25}, '..................oooo...oooooo...xxoo.....xxxx....xx...........': {38}, '..................oooo...oooooo...xxxxx....xxxx....xx...........': {41}, '....................xo.....xoo....xxxx.....ox...................': {45}, '...........................ox......xo.......xo..................': {26, 19, 37}, '..........................xxx......xo.......xo..................': {43}, '...................x.......xx......xo.......xo..................': {43}, '...........................ox......xxx......xo..................': {43, 29}, '...........................ox......oxx.....ooo..................': {34, 18, 51, 50, 52, 53, 54}, '..................x........xx......oxx.....ooo..................': {19, 29, 30}, '..................x........xxo.....ooo.....ooo..................': {42}, '..................x........xxo.....xoo....xooo..................': {19}, '..................xo.......ooo.....ooo....xooo..................': {20}, '..................xxx......ooo.....ooo....xooo..................': {11}, '..................x........xx.o....oxo.....ooo..................': {42}, '...........................ox.....xxxx.....ooo..................': {20, 29}, '....................o......oo.....xxox.....ooo..................': {19, 52}, '...................xo......xx.....xxox.....ooo..................': {26, 38}, '...................xo.....oxx.....xoox.....ooo..................': {18, 42}, '...................xo.....oxx.....xxox....xooo..................': {33}, '...................xo......xx.....xxooo....ooo..................': {51, 12}, '............x......xx......xx.....xxooo....ooo..................': {33}, '....................o......oo.....xxox.....xoo......x...........': {42, 50, 29}, '....................o......oo.....xoox....oooo......x...........': {51}, '....................o......oo.....xoox....ooxo.....xx...........': {53}, '....................o......oo.....xoox....oooo.....xxo..........': {50}, '....................o......oo.....xoox....xooo....xxxo..........': {29}, '....................o......ooo....xooo....xooo....xxxo..........': {46}, '....................o......ooo....xooo....xxxxx...xxxo..........': {60}, '....................o......ooo....xooo....xxoxx...xxoo......o...': {59}, '....................o......ooo....xooo....xxoxx...xxxo.....xo...': {58}, '....................o......ooo....xooo....xxoxx...xoxo....ooo...': {38}, '....................o......oo.....xxox.....ooo....o.x...........': {51}, '....................o......oo.....xxox.....xxo....oxx...........': {42}, '....................o......oo.....xoox....oooo....oxx...........': {19, 53}, '....................o......ooo....xxoo.....xoo......x...........': {53}, '...........................ox......oxx.....xoo....x.............': {42, 29}, '...........................ox......oxx....oooo....x.............': {51}, '...........................ox......oxx.....oxo......x...........': {29, 38}, '...........................ox......oooo....oxo......x...........': {46, 34, 30}, '...........................ox......ooxo....oxxx.....x...........': {20}, '....................o......oo......ooxo....oxxx.....x...........': {34}, '....................o......oo.....xxxxo....xxxx.....x...........': {42}, '....................o......oo.....xoxxo...oxxxx.....x...........': {19}, '...................xo......xx.....xxxxo...oxxxx.....x...........': {26}, '...................xo.....oxx.....oxxxo...oxxxx.....x...........': {17}, '...........................ox......oxx.....oox.......x..........': {20}, '....................o......oo......oox.....oox.......x..........': {51}, '....................o......oo......oox.....oxx.....x.x..........': {52}, '....................o......oo......oox.....oox.....xox..........': {42}, '....................o......oo......oox....xxxx.....xox..........': {34}, '....................o......oo.....ooox....xoxx.....xox..........': {19}, '...........................ooo.....xxo......xo..................': {38, 46, 18, 20, 22, 54, 30}, '..................x........xoo.....xxo......xo..................': {51, 26, 43}, '..................x........xoo.....xoo.....ooo..................': {21}, '..................x..x.....xxo.....xoo.....ooo..................': {26}, '..................x..x....oooo.....ooo.....ooo..................': {34}, '..................x..x....xooo....xooo.....ooo..................': {25}, '..................x........xoo.....xxo......oo.....o............': {21}, '....................x......oxo.....xxo......xo..................': {34, 43}, '....................x......oxo....oooo......xo..................': {26, 38}, '....................x.....xxxo....oxoo......xo..................': {19, 52}, '...................ox.....xxoo....oxoo......xo..................': {18, 21}, '...................oxx....xxxo....oxoo......xo..................': {12}, '....................x.....xxxo....oxoo......oo......o...........': {33, 30}, '....................x.....xxxo...xxxoo......oo......o...........': {12}, '....................x......oxx....oooox.....xo..................': {43, 21, 22}, '....................x......oxx....oooox....ooo..................': {46}, '....................xo.....ooo....oooox.....xo..................': {30}, '....................xo.....ooox...oooxx.....xo..................': {46}, '....................xo.....ooox...oooox.....xoo.................': {22}, '....................xxx....ooox...oooox.....xoo.................': {43}, '....................xxx....ooox...oooox....oooo.................': {53}, '....................xxx....ooxx...oooxx....ooxo......x..........': {39}, '....................xxx....ooxx...oooooo...ooxo......x..........': {31}, '....................xxx....ooxxx..ooooxo...ooxo......x..........': {23}, '....................xxxo...ooxoo..ooooxo...ooxo......x..........': {52}, '....................x.o....oxo....oooox.....xo..................': {30}, '....................x.o....oxxx...oooxx.....xo..................': {21}, '....................xoo....ooox...oooox.....xo..................': {26, 46}, '......................x....oox.....xxo......xo..................': {43, 21}, '.....................ox....ooo.....xxo......xo..................': {30}, '...........................ooo.....xxxx.....xo..................': {43, 52}, '...........................ooo.....xoxx.....oo......o...........': {51, 20, 53}, '...........................ooo.....xoxx.....xx......ox..........': {34}, '...........................ooo....oooxx.....xx......ox..........': {20}, '....................x......oxx....ooxxx.....xx......ox..........': {21}, '....................xo.....oox....ooxxx.....xx......ox..........': {26}, '....................xo....xxxx....oxxxx.....xx......ox..........': {19}, '...................ooo....xxxx....oxxxx.....xx......ox..........': {10}, '...........................ooo.....xxo......xxx.................': {34}, '...........................ooo....oooo......xxx.................': {30}, '...........................ooox...ooox......xxx.................': {38}, '...........................ooox...ooooo.....xxx.................': {21}, '.....................x.....ooxx...oooxo.....xxx.................': {20}, '....................ox.....ooox...oooxo.....xxx.................': {26}, '...........................ox......xxx..........................': {45, 43, 29}, '...........................ox......oxx.....o....................': {18, 26, 34}, '..................x........xx......oxx.....o....................': {19, 38}, '..................xo.......ox......oxx.....o....................': {26}, '..................xo......xxx......oxx.....o....................': {17, 29}, '..................xo......xxxo.....oox.....o....................': {34, 20, 45, 44}, '..................xo......xxxo....xxxx.....o....................': {17, 25}, '.................ooo......xxxo....xxxx.....o....................': {10}, '..........x......oxx......xxxo....xxxx.....o....................': {44}, '..................xo.....ooooo....oxxx.....o....................': {33}, '..................xo.....ooooo...xxxxx.....o....................': {42}, '..................xo.....ooooo...xooxx....oo....................': {21}, '..................xo.x...oooox...xooxx....oo....................': {44}, '..................xo.x...oooox...xooox....ooo...................': {20}, '..................xxxx...oooox...xooox....ooo...................': {46}, '..................xxxx...oooox...xoooo....ooo.o.................': {45}, '..................xxxx...ooxox...xooxx....oooxo.................': {38}, '..................xxxx...ooxox...xooooo...oooxo.................': {51}, '..................xxxx...ooxox...xoxooo...xxoxo....x............': {22}, '..................xo......xxxo.....oxx.....o.x..................': {25, 21, 38}, '..................xo......xxxo.....oooo....o.x..................': {20}, '..................xxx.....xxxo.....oooo....o.x..................': {21}, '..................xxxo....xxoo.....oooo....o.x..................': {30}, '..................xxxo....xxxxx....oooo....o.x..................': {23}, '..................xxxo.o..xxxxo....oooo....o.x..................': {22}, '..................xxxxxo..xxxxo....oooo....o.x..................': {13}, '..........................xxx......oxx.....o....................': {19, 38}, '...................o......xox......oxx.....o....................': {34, 44}, '...................o......xox.....xxxx.....o....................': {29}, '...................o......xooo....xxox.....o....................': {20}, '...................ox.....xxoo....xxox.....o....................': {21}, '...................ooo....xxoo....xxox.....o....................': {10}, '..........x........xoo....xxxo....xxox.....o....................': {25, 42}, '..........x........xoo...ooooo....oxox.....o....................': {17}, '..........................xxx......oooo....o....................': {42}, '..........................xxx......xooo...xo....................': {34}, '..........................xxx.....ooooo...xo....................': {51}, '..........................xxx.....oxooo...xx.......x............': {19}, '...................o......xxo.....oxooo...xx.......x............': {25}, '...................o.....xxxo.....xxooo...xx.......x............': {18}, '..................oo.....xxoo.....xxooo...xx.......x............': {20}, '..................oox....xxxo.....xxooo...xx.......x............': {21}, '...........................ox.....xxxx.....o....................': {29}, '...........................ooo....xxox.....o....................': {19, 20}, '....................x......xoo....xxox.....o....................': {42, 19}, '....................x......xoo....xoox....oo....................': {51, 19, 44, 21}, '...................xx......xxo....xoox....oo....................': {45, 21}, '...................xx......xxo....xooo....oo.o..................': {44}, '...................xx......xxo....xoxo....ooxo..................': {51}, '...................xx......xxo....xoxo....oooo.....o............': {52, 22, 30}, '...................xx.x....xxx....xoxo....oooo.....o............': {26}, '...................xx.x...oxxx....ooxo....oooo.....o............': {25, 38}, '...................xx.x..xxxxx....ooxo....oooo.....o............': {18}, '...................xx.x...oxxx....ooxxx...oooo.....o............': {18}, '..................oxx.x...ooxx....oooxx...oooo.....o............': {25}, '..................oxx.x..xxxxx....oooxx...oooo.....o............': {12}, '...................xx......xxxx...xoxo....oooo.....o............': {26}, '...................xx.....oxxxx...ooxo....oooo.....o............': {46, 38}, '...................xx.....oxxxx...ooxxx...oooo.....o............': {18}, '..................oxx.....ooxxx...oooxx...oooo.....o............': {53}, '..................oxx.....ooxxx...oooxx...ooox.....o.x..........': {11}, '...........o......oox.....ooxxx...oooxx...ooox.....o.x..........': {52}, '...........o......oox.....ooxxx...ooxxx...ooxx.....oxx..........': {13}, '....................x......xxo....xoxx....oox...................': {45}, '...........................ox......xox.......o..................': {26, 19, 44}, '..........................xxx......xox.......o..................': {29}, '...................x.......xx......xox.......o..................': {29}}

class Strategy:
    # implement all the required methods on your own
    logging = True # turns on logging
    def best_strategy(self, board, player, best_move, running):
        time.sleep(1)
        if running.value:
            lookup_board_directions()

            if board in opening_book: best_move.value = random.choice([*opening_book[board]])
            else:
                best_move.value = find_best_move(board, player, poss_mvs(board, player))
                if board.count('.')<=15:
                    for depth in range(14,18):
                        best_move.value = alphabeta(board, player, -65, 65, depth, True)[-1]
                else:
                    for depth in range(3,18):
                        best_move.value = alphabeta(board, player, -65, 65, depth, False)[-1]

def main():
    lookup_board_directions()
    if not args:
        start_time = time.process_time()
        runTournament(GAMESINTOURNAMENT)
        print("Elapsed time: " + str(time.process_time()-start_time))
    else: individualMoveProcessing()

if __name__ == '__main__': main()