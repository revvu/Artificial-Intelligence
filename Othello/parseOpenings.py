# Reevu Adakroy 2/9/2021
# prints a dictionary for the opening book

dir_dct = {}

di = [-1, -1, -1, 0, 0, 1, 1, 1]
dj = [-1, 0, 1, -1, 1, -1, 0, 1]

def lookup_board_directions():
    global dir_dct
    vis=[[False]*8 for i in range(8)]
    for i in range(64): dir_dct[i] = set()
    flood(0, 0, vis)

def flood(rw, cl, vis):
    global dir_dct

    if vis[rw][cl]: return
    vis[rw][cl]=True
    cnt=0
    for i in range(8):
        if not 0<=rw+di[i]<8 or not 0<=cl+dj[i]<8: continue
        dir_dct[rw*8+cl].add(di[i]*8+dj[i])
        flood(rw+di[i], cl+dj[i], vis)
        cnt+=1

def make_move(brd, tkn, mv, pst_lst):
    brd = brd.replace('*', '.')
    exp = [*brd]
    exp[mv] = tkn

    for dct, end in pst_lst[mv]:
        for pnt in range(mv, end, dct):
            exp[pnt] = tkn
    return ''.join(exp)

def poss_mvs(brd, tkn):

    pst_lst = {}
    eTkn = oppose(tkn)

    for i in range(len(brd)):
        if brd[i] != '.': continue
        for dct in dir_dct[i]:
            pnt, endTkn = pet(brd, eTkn, i+dct, dct)
            if pnt==i+dct or endTkn!=tkn: continue
            if i not in pst_lst: pst_lst[i] = []
            pst_lst[i]+=[(dct, pnt)]
    return pst_lst

def oppose(token):
    return 'xo'['x'==token]

def pet(brd, eTkn, pnt, dct):
    while brd[pnt] == eTkn and dct in dir_dct[pnt]:
        pnt = pnt + dct
    return pnt, brd[pnt]

def process_move(moves):
    return [ord(mv[0])-105+int(mv[1])*8 if mv[0].isalpha() else int(mv) for mv in moves if mv[0]!='-']

openings = ['C4 c3', 'C4 c3 D3 c5 B2', 'C4 c3 D3 c5 B3', 'C4 c3 D3 c5 B3 f4 B5 b4 C6 d6 F5', 'C4 c3 D3 c5 B4', 'C4 c3 D3 c5 B4 d2 C2 f4 D6 c6 F5 e6 F7', 'C4 c3 D3 c5 B4 d2 D6', 'C4 c3 D3 c5 B4 d2 E2', 'C4 c3 D3 c5 B4 e3', 'C4 c3 D3 c5 B5', 'C4 c3 D3 c5 B6 c6 B5', 'C4 c3 D3 c5 B6 e3', 'C4 c3 D3 c5 D6', 'C4 c3 D3 c5 D6 e3', 'C4 c3 D3 c5 D6 f4 B4', 'C4 c3 D3 c5 D6 f4 B4 b6 B5 c6 B3', 'C4 c3 D3 c5 D6 f4 B4 b6 B5 c6 F5', 'C4 c3 D3 c5 D6 f4 B4 c6 B5 b3 B6 e3 C2 a4 A5 a6 D2', 'C4 c3 D3 c5 D6 f4 B4 e3 B3', 'C4 c3 D3 c5 D6 f4 F5', 'C4 c3 D3 c5 D6 f4 F5 d2', 'C4 c3 D3 c5 D6 f4 F5 d2 B5', 'C4 c3 D3 c5 D6 f4 F5 d2 G4 d7', 'C4 c3 D3 c5 D6 f4 F5 e6 C6 d7', 'C4 c3 D3 c5 D6 f4 F5 e6 F6', 'C4 c3 D3 c5 F6', 'C4 c3 D3 c5 F6 e2 C6', 'C4 c3 D3 c5 F6 e3 C6 f5 F4 g5', 'C4 c3 D3 c5 F6 f5', 'C4 c3 D3 e3 B2', 'C4 c3 D3 e3 C2', 'C4 c3 D3 e3 C2 d6 E2 d2 F3 f4 E6', 'C4 c3 D3 e3 D2', 'C4 c3 D3 e3 D2 b4 B3 d6 F4 f3 E6 f5 G6', 'C4 c3 D3 e3 D2 b4 B5', 'C4 c3 D3 e3 D2 b4 F4', 'C4 c3 D3 e3 D2 c5', 'C4 c3 D3 e3 E2', 'C4 c3 D3 e3 F2 c5', 'C4 c3 D3 e3 F2 f3 E2', 'C4 c3 D3 e3 F4', 'C4 c3 D3 e3 F4 c5', 'C4 c3 D3 e3 F4 d6 D2', 'C4 c3 D3 e3 F4 d6 D2 c5 C2', 'C4 c3 D3 e3 F4 d6 D2 f2 E2 f3 C2', 'C4 c3 D3 e3 F4 d6 D2 f2 E2 f3 E6', 'C4 c3 D3 e3 F4 d6 D2 f3 E2 c2 F2 c5 B3 d1 E1 f1 B4', 'C4 c3 D3 e3 F4 d6 E6', 'C4 c3 D3 e3 F4 d6 E6 b4', 'C4 c3 D3 e3 F4 d6 E6 b4 D7 g4', 'C4 c3 D3 e3 F4 d6 E6 b4 E2', 'C4 c3 D3 e3 F4 d6 E6 f5 F3 g4', 'C4 c3 D3 e3 F4 d6 E6 f5 F6', 'C4 c3 D3 e3 F6', 'C4 c3 D3 e3 F6 b5 F3', 'C4 c3 D3 e3 F6 c5 F3 e6 D6 e7', 'C4 c3 D3 e3 F6 e6', 'C4 c3 E6 c5', 'C4 c3 F5 c5', 'C4 c5', 'C4 e3', 'C4 e3 F4 c5 D6 e6', 'C4 e3 F4 c5 D6 f3 C6', 'C4 e3 F4 c5 D6 f3 D3', 'C4 e3 F4 c5 D6 f3 D3 c3', 'C4 e3 F4 c5 D6 f3 E2', 'C4 e3 F4 c5 D6 f3 E6 c3 D3 e2', 'C4 e3 F4 c5 D6 f3 E6 c3 D3 e2 B5', 'C4 e3 F4 c5 D6 f3 E6 c3 D3 e2 B5 f5', 'C4 e3 F4 c5 D6 f3 E6 c3 D3 e2 B5 f5 B3', 'C4 e3 F4 c5 D6 f3 E6 c3 D3 e2 B5 f5 B4 f6 C2 e7 D2 c7', 'C4 e3 F4 c5 D6 f3 E6 c3 D3 e2 B6 f5', 'C4 e3 F4 c5 D6 f3 E6 c3 D3 e2 B6 f5 B4 f6 G5 d7', 'C4 e3 F4 c5 D6 f3 E6 c3 D3 e2 B6 f5 G5', 'C4 e3 F4 c5 D6 f3 E6 c3 D3 e2 B6 f5 G5 f6', 'C4 e3 F4 c5 D6 f3 E6 c3 D3 e2 D2', 'C4 e3 F4 c5 D6 f3 E6 c6', 'C4 e3 F4 c5 E6', 'C4 e3 F5 b4', 'C4 e3 F5 b4 F3', 'C4 e3 F5 b4 F3 f4 E2 e6 G5 f6 D6 c6', 'C4 e3 F5 e6 D3', 'C4 e3 F5 e6 F4', 'C4 e3 F5 e6 F4 c5 D6 c6 F7 f3', 'C4 e3 F5 e6 F4 c5 D6 c6 F7 g5 G6', 'C4 e3 F6 b4', 'C4 e3 F6 e6 F5', 'C4 e3 F6 e6 F5 c5 C3', 'C4 e3 F6 e6 F5 c5 C3 b4', 'C4 e3 F6 e6 F5 c5 C3 b4 D6 c6 B5 a6 B6 c7', 'C4 e3 F6 e6 F5 c5 C3 c6', 'C4 e3 F6 e6 F5 c5 C3 g5', 'C4 e3 F6 e6 F5 c5 D3', 'C4 e3 F6 e6 F5 c5 D6', 'C4 e3 F6 e6 F5 c5 F4 g5 G4 f3 C6 d3 D6', 'C4 e3 F6 e6 F5 c5 F4 g5 G4 f3 C6 d3 D6 b3 C3 b4 E2 b6', 'C4 e3 F6 e6 F5 c5 F4 g6 F7', 'C4 e3 F6 e6 F5 c5 F4 g6 F7 d3', 'C4 e3 F6 e6 F5 g6', 'D3 c3', 'D3 c3 C4 c5 B2', 'D3 c3 C4 c5 B3', 'D3 c3 C4 c5 B3 f4 B5 b4 C6 d6 F5', 'D3 c3 C4 c5 B4', 'D3 c3 C4 c5 B4 d2 C2 f4 D6 c6 F5 e6 F7', 'D3 c3 C4 c5 B4 d2 D6', 'D3 c3 C4 c5 B4 d2 E2', 'D3 c3 C4 c5 B4 e3', 'D3 c3 C4 c5 B5', 'D3 c3 C4 c5 B6 c6 B5', 'D3 c3 C4 c5 B6 e3', 'D3 c3 C4 c5 D6', 'D3 c3 C4 c5 D6 e3', 'D3 c3 C4 c5 D6 f4 B4', 'D3 c3 C4 c5 D6 f4 B4 b6 B5 c6 B3', 'D3 c3 C4 c5 D6 f4 B4 b6 B5 c6 F5', 'D3 c3 C4 c5 D6 f4 B4 c6 B5 b3 B6 e3 C2 a4 A5 a6 D2', 'D3 c3 C4 c5 D6 f4 B4 e3 B3', 'D3 c3 C4 c5 D6 f4 F5', 'D3 c3 C4 c5 D6 f4 F5 d2', 'D3 c3 C4 c5 D6 f4 F5 d2 B5', 'D3 c3 C4 c5 D6 f4 F5 d2 G4 d7', 'D3 c3 C4 c5 D6 f4 F5 e6 C6 d7', 'D3 c3 C4 c5 D6 f4 F5 e6 F6', 'D3 c3 C4 c5 F6', 'D3 c3 C4 c5 F6 e2 C6', 'D3 c3 C4 c5 F6 e3 C6 f5 F4 g5', 'D3 c3 C4 c5 F6 f5', 'D3 c3 C4 e3 B2', 'D3 c3 C4 e3 C2', 'D3 c3 C4 e3 C2 d6 E2 d2 F3 f4 E6', 'D3 c3 C4 e3 D2', 'D3 c3 C4 e3 D2 b4 B3 d6 F4 f3 E6 f5 G6', 'D3 c3 C4 e3 D2 b4 B5', 'D3 c3 C4 e3 D2 b4 F4', 'D3 c3 C4 e3 D2 c5', 'D3 c3 C4 e3 E2', 'D3 c3 C4 e3 F2 c5', 'D3 c3 C4 e3 F2 f3 E2', 'D3 c3 C4 e3 F4', 'D3 c3 C4 e3 F4 c5', 'D3 c3 C4 e3 F4 d6 D2', 'D3 c3 C4 e3 F4 d6 D2 c5 C2', 'D3 c3 C4 e3 F4 d6 D2 f2 E2 f3 C2', 'D3 c3 C4 e3 F4 d6 D2 f2 E2 f3 E6', 'D3 c3 C4 e3 F4 d6 D2 f3 E2 c2 F2 c5 B3 d1 E1 f1 B4', 'D3 c3 C4 e3 F4 d6 E6', 'D3 c3 C4 e3 F4 d6 E6 b4', 'D3 c3 C4 e3 F4 d6 E6 b4 D7 g4', 'D3 c3 C4 e3 F4 d6 E6 b4 E2', 'D3 c3 C4 e3 F4 d6 E6 f5 F3 g4', 'D3 c3 C4 e3 F4 d6 E6 f5 F6', 'D3 c3 C4 e3 F6', 'D3 c3 C4 e3 F6 b5 F3', 'D3 c3 C4 e3 F6 c5 F3 e6 D6 e7', 'D3 c3 C4 e3 F6 e6', 'D3 c3 E6 e3', 'D3 c3 F5 e3', 'D3 c5', 'D3 c5 D6 e3 F4 c6 B5', 'D3 c5 D6 e3 F4 c6 C4', 'D3 c5 D6 e3 F4 c6 C4 c3', 'D3 c5 D6 e3 F4 c6 F3', 'D3 c5 D6 e3 F4 c6 F5 c3 C4 b5', 'D3 c5 D6 e3 F4 c6 F5 c3 C4 b5 B4', 'D3 c5 D6 e3 F4 c6 F5 c3 C4 b5 E2', 'D3 c5 D6 e3 F4 c6 F5 c3 C4 b5 E2 e6', 'D3 c5 D6 e3 F4 c6 F5 c3 C4 b5 E2 e6 C2', 'D3 c5 D6 e3 F4 c6 F5 c3 C4 b5 E2 e6 D2 f6 B3 g5 B4 g3', 'D3 c5 D6 e3 F4 c6 F5 c3 C4 b5 F2 e6', 'D3 c5 D6 e3 F4 c6 F5 c3 C4 b5 F2 e6 D2 f6 E7 g4', 'D3 c5 D6 e3 F4 c6 F5 c3 C4 b5 F2 e6 E7', 'D3 c5 D6 e3 F4 c6 F5 c3 C4 b5 F2 e6 E7 f6', 'D3 c5 D6 e3 F4 c6 F5 f3', 'D3 c5 D6 e3 F4 f5', 'D3 c5 D6 e3 F5', 'D3 c5 E6 d2', 'D3 c5 E6 d2 C6', 'D3 c5 E6 d2 C6 d6 B5 f5 E7 f6 F4 f3', 'D3 c5 E6 f5 C4', 'D3 c5 E6 f5 D6', 'D3 c5 E6 f5 D6 e3 F4 f3 G6 c6', 'D3 c5 E6 f5 D6 e3 F4 f3 G6 e7 F7', 'D3 c5 F6 d2', 'D3 c5 F6 f5 E6', 'D3 c5 F6 f5 E6 e3 C3', 'D3 c5 F6 f5 E6 e3 C3 d2', 'D3 c5 F6 f5 E6 e3 C3 d2 F4 f3 E2 f1 F2 g3', 'D3 c5 F6 f5 E6 e3 C3 e7', 'D3 c5 F6 f5 E6 e3 C3 f3', 'D3 c5 F6 f5 E6 e3 C4', 'D3 c5 F6 f5 E6 e3 D6 e7 D7 c6 F3 c4 F4', 'D3 c5 F6 f5 E6 e3 D6 e7 D7 c6 F3 c4 F4 c2 C3 d2 B5 f2', 'D3 c5 F6 f5 E6 e3 D6 f7 G6', 'D3 c5 F6 f5 E6 e3 D6 f7 G6 c4', 'D3 c5 F6 f5 E6 e3 F4', 'D3 c5 F6 f5 E6 f7', 'D3 e3', 'E6 d6', 'E6 f4', 'E6 f4 C3 c4 D3', 'E6 f4 C3 c4 D3 c2', 'E6 f4 C3 c4 D3 d6 C5', 'E6 f4 C3 c4 D3 d6 E3 c2 B3', 'E6 f4 C3 c4 D3 d6 E3 c2 B3 f5', 'E6 f4 C3 c4 D3 d6 E3 d2 E2 f3 C6 f5 C5', 'E6 f4 C3 c4 D3 d6 E3 d2 E2 f3 C6 f5 C5 f7 F6 e7 G4 c7', 'E6 f4 C3 c4 D3 d6 F5', 'E6 f4 C3 c4 D3 d6 F6', 'E6 f4 C3 c4 D3 d6 F6 c6', 'E6 f4 C3 c4 D3 d6 F6 d2', 'E6 f4 C3 c4 D3 d6 F6 e7', 'E6 f4 C3 c4 D3 d6 F6 e7 C5 c6 D7 c8 C7 b6', 'E6 f4 C3 e7', 'E6 f4 D3 c4 E3', 'E6 f4 D3 c4 E3 d6 C5 c6 B3 d2 C2', 'E6 f4 D3 c4 E3 d6 C5 c6 B3 f3', 'E6 f4 D3 c4 F5', 'E6 f4 D3 e7', 'E6 f4 D3 e7 F3', 'E6 f4 D3 e7 F3 e3 G4 c4 D2 c3 C5 c6', 'E6 f4 E3 d6 C4', 'E6 f4 E3 d6 C5 c4', 'E6 f4 E3 d6 C5 f3 C4 c6', 'E6 f4 E3 d6 C5 f3 C4 f6 F5 g4', 'E6 f4 E3 d6 C5 f3 C4 f6 F5 g4 C7 d3', 'E6 f4 E3 d6 C5 f3 C4 f6 F5 g4 C7 d3 D2', 'E6 f4 E3 d6 C5 f3 C4 f6 F5 g4 C7 d3 D2 c3', 'E6 f4 E3 d6 C5 f3 C4 f6 F5 g4 C7 d3 E7 c3 D2 b5', 'E6 f4 E3 d6 C5 f3 C4 f6 F5 g4 D7', 'E6 f4 E3 d6 C5 f3 C4 f6 F5 g4 D7 d3', 'E6 f4 E3 d6 C5 f3 C4 f6 F5 g4 D7 d3 E7 c3 G6 b4 G5 b6', 'E6 f4 E3 d6 C5 f3 C4 f6 F5 g4 D7 d3 F7', 'E6 f4 E3 d6 C5 f3 C4 f6 F5 g4 G5', 'E6 f4 E3 d6 C5 f3 C6', 'E6 f4 E3 d6 C5 f3 F5', 'E6 f4 E3 d6 C5 f3 F5 f6', 'E6 f4 E3 d6 C5 f3 G4', 'E6 f6', 'E6 f6 C4 d6', 'E6 f6 D3 d6', 'E6 f6 F5 d6 C3', 'E6 f6 F5 d6 C3 d3', 'E6 f6 F5 d6 C3 f4 C6 d3 E3 d2', 'E6 f6 F5 d6 C3 g4 C6', 'E6 f6 F5 d6 C5', 'E6 f6 F5 d6 C5 e3 D3', 'E6 f6 F5 d6 C5 e3 D3 c4 C3', 'E6 f6 F5 d6 C5 e3 D3 c4 C6 b5', 'E6 f6 F5 d6 C5 e3 D3 g5', 'E6 f6 F5 d6 C5 e3 D3 g5 D7', 'E6 f6 F5 d6 C5 e3 D3 g5 E2 b5', 'E6 f6 F5 d6 C5 e3 E7', 'E6 f6 F5 d6 C5 e3 E7 c6 D7 f7 C7 f4 G6 e8 D8 c8 G5', 'E6 f6 F5 d6 C5 e3 E7 c7 D7 c6 D3', 'E6 f6 F5 d6 C5 e3 E7 c7 D7 c6 F7', 'E6 f6 F5 d6 C5 e3 E7 f4 F7', 'E6 f6 F5 d6 C5 f4', 'E6 f6 F5 d6 C7 c6 D7', 'E6 f6 F5 d6 C7 f4', 'E6 f6 F5 d6 D7', 'E6 f6 F5 d6 E7', 'E6 f6 F5 d6 E7 f4', 'E6 f6 F5 d6 E7 g5 C5', 'E6 f6 F5 d6 E7 g5 G4', 'E6 f6 F5 d6 E7 g5 G6 e3 C5 c6 D3 c4 B3', 'E6 f6 F5 d6 F7', 'E6 f6 F5 d6 F7 e3 D7 e7 C6 c5 D3', 'E6 f6 F5 d6 G7', 'E6 f6 F5 f4 C3', 'E6 f6 F5 f4 C3 c4', 'E6 f6 F5 f4 C3 d6 F3 c4 C5 b4', 'E6 f6 F5 f4 C3 d7 F3', 'E6 f6 F5 f4 E3', 'E6 f6 F5 f4 E3 c5 C4', 'E6 f6 F5 f4 E3 c5 C4 d3 C3', 'E6 f6 F5 f4 E3 c5 C4 d3 F3 e2', 'E6 f6 F5 f4 E3 c5 C4 e7', 'E6 f6 F5 f4 E3 c5 C4 e7 B5 e2', 'E6 f6 F5 f4 E3 c5 C4 e7 G4', 'E6 f6 F5 f4 E3 c5 G5', 'E6 f6 F5 f4 E3 c5 G5 d6 G6', 'E6 f6 F5 f4 E3 c5 G5 f3 G4 g6 G3 d6 F7 h5 H4 h3 E7', 'E6 f6 F5 f4 E3 c5 G5 g3 G4 f3 C4', 'E6 f6 F5 f4 E3 c5 G5 g3 G4 f3 G6', 'E6 f6 F5 f4 E3 d6', 'E6 f6 F5 f4 G3 d6', 'E6 f6 F5 f4 G3 f3 G4', 'E6 f6 F5 f4 G4', 'E6 f6 F5 f4 G5', 'E6 f6 F5 f4 G5 d6', 'E6 f6 F5 f4 G5 e7 D7', 'E6 f6 F5 f4 G5 e7 E3', 'E6 f6 F5 f4 G5 e7 F7 c5 E3 f3 C4 d3 C2', 'E6 f6 F5 f4 G6', 'E6 f6 F5 f4 G6 c5 G4 g5 F3 e3 C4', 'E6 f6 F5 f4 G7', 'F5 d6', 'F5 d6 C3 d3 C4', 'F5 d6 C3 d3 C4 b3', 'F5 d6 C3 d3 C4 f4 C5 b3 C2', 'F5 d6 C3 d3 C4 f4 C5 b3 C2 e6', 'F5 d6 C3 d3 C4 f4 C5 b4 B5 c6 F3 e6 E3', 'F5 d6 C3 d3 C4 f4 C5 b4 B5 c6 F3 e6 E3 g6 F6 g5 D7 g3', 'F5 d6 C3 d3 C4 f4 E3', 'F5 d6 C3 d3 C4 f4 E6', 'F5 d6 C3 d3 C4 f4 F6', 'F5 d6 C3 d3 C4 f4 F6 b4', 'F5 d6 C3 d3 C4 f4 F6 f3', 'F5 d6 C3 d3 C4 f4 F6 g5', 'F5 d6 C3 d3 C4 f4 F6 g5 E3 f3 G4 h3 G3 f2', 'F5 d6 C3 g5', 'F5 d6 C4 d3 C5', 'F5 d6 C4 d3 C5 f4 E3 f3 C2 b4 B3', 'F5 d6 C4 d3 C5 f4 E3 f3 C2 c6', 'F5 d6 C4 d3 E6', 'F5 d6 C4 g5', 'F5 d6 C4 g5 C6', 'F5 d6 C4 g5 C6 c5 D7 d3 B4 c3 E3 f3', 'F5 d6 C5 f4 D3', 'F5 d6 C5 f4 E3 c6 D3 f3', 'F5 d6 C5 f4 E3 c6 D3 f6 E6 d7', 'F5 d6 C5 f4 E3 c6 D3 f6 E6 d7 E7', 'F5 d6 C5 f4 E3 c6 D3 f6 E6 d7 G3 c4', 'F5 d6 C5 f4 E3 c6 D3 f6 E6 d7 G3 c4 B4', 'F5 d6 C5 f4 E3 c6 D3 f6 E6 d7 G3 c4 B4 c3', 'F5 d6 C5 f4 E3 c6 D3 f6 E6 d7 G3 c4 G5 c3 B4 e2', 'F5 d6 C5 f4 E3 c6 D3 f6 E6 d7 G4', 'F5 d6 C5 f4 E3 c6 D3 f6 E6 d7 G4 c4', 'F5 d6 C5 f4 E3 c6 D3 f6 E6 d7 G4 c4 G5 c3 F7 d2 E7 f2', 'F5 d6 C5 f4 E3 c6 D3 f6 E6 d7 G4 c4 G6', 'F5 d6 C5 f4 E3 c6 D7', 'F5 d6 C5 f4 E3 c6 E6', 'F5 d6 C5 f4 E3 c6 E6 f6', 'F5 d6 C5 f4 E3 c6 F3', 'F5 d6 C5 f4 E3 d3', 'F5 f4', 'F5 f6', 'F5 f6 C4 f4', 'F5 f6 D3 f4', 'F5 f6 E6 d6 C3', 'F5 f6 E6 d6 C3 d3', 'F5 f6 E6 d6 C3 f4 C6 d3 E3 d2', 'F5 f6 E6 d6 C3 g4 C6', 'F5 f6 E6 d6 C5', 'F5 f6 E6 d6 C5 e3 D3', 'F5 f6 E6 d6 C5 e3 D3 c4 C3', 'F5 f6 E6 d6 C5 e3 D3 c4 C6 b5', 'F5 f6 E6 d6 C5 e3 D3 g5', 'F5 f6 E6 d6 C5 e3 D3 g5 D7', 'F5 f6 E6 d6 C5 e3 D3 g5 E2 b5', 'F5 f6 E6 d6 C5 e3 E7', 'F5 f6 E6 d6 C5 e3 E7 c6 D7 f7 C7 f4 G6 e8 D8 c8 G5', 'F5 f6 E6 d6 C5 e3 E7 c7 D7 c6 D3', 'F5 f6 E6 d6 C5 e3 E7 c7 D7 c6 F7', 'F5 f6 E6 d6 C5 e3 E7 f4 F7', 'F5 f6 E6 d6 C5 f4', 'F5 f6 E6 d6 C7 c6 D7', 'F5 f6 E6 d6 C7 f4', 'F5 f6 E6 d6 D7', 'F5 f6 E6 d6 E7', 'F5 f6 E6 d6 E7 f4', 'F5 f6 E6 d6 E7 g5 C5', 'F5 f6 E6 d6 E7 g5 G4', 'F5 f6 E6 d6 E7 g5 G6 e3 C5 c6 D3 c4 B3', 'F5 f6 E6 d6 F7', 'F5 f6 E6 d6 F7 e3 D7 e7 C6 c5 D3', 'F5 f6 E6 d6 G7', 'F5 f6 E6 f4 C3', 'F5 f6 E6 f4 C3 c4', 'F5 f6 E6 f4 C3 d6 F3 c4 C5 b4', 'F5 f6 E6 f4 C3 d7 F3', 'F5 f6 E6 f4 E3', 'F5 f6 E6 f4 E3 c5 C4', 'F5 f6 E6 f4 E3 c5 C4 d3 C3', 'F5 f6 E6 f4 E3 c5 C4 d3 F3 e2', 'F5 f6 E6 f4 E3 c5 C4 e7', 'F5 f6 E6 f4 E3 c5 C4 e7 B5 e2', 'F5 f6 E6 f4 E3 c5 C4 e7 G4', 'F5 f6 E6 f4 E3 c5 G5', 'F5 f6 E6 f4 E3 c5 G5 d6 G6', 'F5 f6 E6 f4 E3 c5 G5 f3 G4 g6 G3 d6 F7 h5 H4 h3 E7', 'F5 f6 E6 f4 E3 c5 G5 g3 G4 f3 C4', 'F5 f6 E6 f4 E3 c5 G5 g3 G4 f3 G6', 'F5 f6 E6 f4 E3 d6', 'F5 f6 E6 f4 G3 d6', 'F5 f6 E6 f4 G3 f3 G4', 'F5 f6 E6 f4 G4', 'F5 f6 E6 f4 G5', 'F5 f6 E6 f4 G5 d6', 'F5 f6 E6 f4 G5 e7 D7', 'F5 f6 E6 f4 G5 e7 E3', 'F5 f6 E6 f4 G5 e7 F7 c5 E3 f3 C4 d3 C2', 'F5 f6 E6 f4 G6', 'F5 f6 E6 f4 G6 c5 G4 g5 F3 e3 C4', 'F5 f6 E6 f4 G7']
opening_book = {}

#make a book where each board has a set of moves

def parse_to_book(opening):
    global opening_book
    brd, tkn = '.'*27+"ox......xo"+'.'*27, 'x'
    opening = opening.split(' ')
    new_opening = [mv.lower() for mv in opening]
    mvs = process_move(new_opening)

    for mv in mvs:
        #check the current board
        if brd not in opening_book:
            opening_book[brd]=[]
        opening_book[brd].append(mv)

        #make the move
        mv_lst = poss_mvs(brd, tkn)
        brd = make_move(brd, tkn, mv, mv_lst)
        tkn = oppose(tkn)

lookup_board_directions()
for opening in openings:
    parse_to_book(opening)

print(opening_book)
print(len(opening_book))
print(opening_book['.'*27+"ox......xo"+'.'*27])