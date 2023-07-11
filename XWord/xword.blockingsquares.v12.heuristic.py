import sys; args = sys.argv[1:]
# Reevu Adakroy pd. 7
# started 2/21/2021

import time
import re

gHEIGHT = gWIDTH = gBLOCKCOUNT = gHALF_LENGTH = 0
gSEEDS, g180LST, gHORIZONTAL_CONSTRAINTS, gVERTICAL_CONSTRAINTS = [],[],[],[]
gEDGESET = set()

def parse_input():
    global gBLOCKCOUNT, gSEEDS, g180LST, gHALF_LENGTH, gEDGESET
    for arg in args:
        if re.fullmatch(r'\d+x\d+',arg): parse_dimensions(arg)
        elif re.fullmatch(r'\d+',arg): gBLOCKCOUNT = int(arg)
        elif re.fullmatch(r'.*\.txt',arg): continue
        elif re.fullmatch(r'(H|V|h|v)\d+x\d+.*',arg): gSEEDS+=[arg]
    pzl = ['*']*((1+gWIDTH*gHEIGHT)//2)
    gHALF_LENGTH = gWIDTH*gHEIGHT//2
    g180LST = [*range(gWIDTH*gHEIGHT-1,-1,-1)]

    for idx in range(0, gWIDTH): gEDGESET.add(idx)
    for idx in range(0, gWIDTH*gHEIGHT, gWIDTH):
        if idx < len(pzl): gEDGESET.add(idx)
        else: gEDGESET.add(g180LST[idx])

    return pzl

def lookup_constraints():
    global gVERTICAL_CONSTRAINTS, gHORIZONTAL_CONSTRAINTS
    #indexed board
    indexed_board = [i for i in range(gHEIGHT*gWIDTH)]
    #horizontal constraints
    for idx in range(0, gHEIGHT//2):
        gHORIZONTAL_CONSTRAINTS+=[indexed_board[idx*gWIDTH:idx*gWIDTH+gWIDTH]]
    # #bad row
    if gHEIGHT%2:
        horizontal_constraint_lst = []
        for index in range((gHEIGHT//2)*gWIDTH,gWIDTH*(gHEIGHT//2)+gWIDTH):
            if index < gHALF_LENGTH: horizontal_constraint_lst+=[indexed_board[index]]
            else: horizontal_constraint_lst+=[indexed_board[g180LST[index]]]
        gHORIZONTAL_CONSTRAINTS+=[horizontal_constraint_lst]
    #vertical constraints
    for idx in range(0, (gWIDTH+1)//2):
        vertical_constraint_lst = []
        for index in range(idx, len(indexed_board), gWIDTH):
            if index < gHALF_LENGTH: vertical_constraint_lst+=[indexed_board[index]]
            else: vertical_constraint_lst+=[indexed_board[g180LST[index]]]
        gVERTICAL_CONSTRAINTS+=[vertical_constraint_lst]


def parse_dimensions(arg):
    global gHEIGHT,gWIDTH
    x_loc = arg.find('x')
    gHEIGHT = int(arg[0:x_loc])
    gWIDTH = int(arg[x_loc+1:])

def print_puzzle(pzl):
    for i in range(0,len(pzl),gWIDTH): print(' '.join(pzl[i:i+gWIDTH]).replace('*','-'))

def place_blocks_180(pzl):
    filled_block_count = 0
    # if  blockcount odd, fill in middle
    if gBLOCKCOUNT%2:
        pzl[-1]='#'
        filled_block_count+=1
    idx = 0
    while filled_block_count < gBLOCKCOUNT:
        if pzl[idx]=='*':
            pzl[idx]='#'
            filled_block_count+=2
        idx+=1
    return pzl

def temp_words(pzl):
    for seed in gSEEDS:
        row,col = [int(x) for x in re.findall(r'\d+', seed)]
        word = str(re.search(r'(?!\w*\d).*', seed).group())
        for idx in range(len(word)):
            placing_index = row*gWIDTH+col+idx*gWIDTH**(seed[0]=='V' or seed[0]=='v')
            if placing_index < len(pzl): pzl[placing_index]=['-','#'][word[idx]=='#']
            else: pzl[g180LST[placing_index]]=['-','#'][word[idx]=='#']
    return pzl

def place_words(pzl):
    for seed in gSEEDS:
        row,col = [int(x) for x in re.findall(r'\d+', seed)]
        word = str(re.search(r'(?!\w*\d).*', seed).group())
        for idx in range(len(word)): pzl[row*gWIDTH+col+idx*gWIDTH**(seed[0]=='V' or seed[0]=='v')]=word[idx]
    return pzl

def lookup_index_lst(pzl):
    # bucket by edge/near-block and not
    # still not sufficient because derived squares can make the puzzle not good placement
    primary = []
    secondary = []
    dpos = [1,-1,gWIDTH,-gWIDTH]
    for i in range(len(pzl)):
        if pzl[i] == '*':
            added = False
            for pos in dpos:
                for multiple in range(3):
                    index = i+pos*(multiple+1)
                    if index<0: continue
                    if len(pzl)+gWIDTH//2 > index >= len(pzl): index = g180LST[index]
                    if index >= len(pzl): continue
                    if pzl[index]=='#':
                        secondary+=[i]
                        added=True
                        break
            if not added: primary+=[i]
    return secondary+primary

# def lookup_index_lst(pzl):
#     # bucket by edge/near-block and not
#     # still not sufficient because derived squares can make the puzzle not good placement
#     primary = []
#     secondary = []
#     dpos = [1,-1,gWIDTH,-gWIDTH]
#     for i in range(len(pzl)):
#         if pzl[i] == '*':
#             if i in gEDGESET: secondary+=[i]
#             else:
#                 added = False
#                 for pos in dpos:
#                     for multiple in range(4):
#                         index = i+pos*(multiple+1)
#                         if 0> index or index >= len(pzl): continue
#                         if pzl[index]=='#':
#                             secondary+=[i]
#                             added=True
#                             break
#                 if not added: primary+=[i]
#     return secondary+primary


def constrain_word_length(pzl):
    new_pzl = [i for i in pzl]
    for constraint_lst in gHORIZONTAL_CONSTRAINTS+gVERTICAL_CONSTRAINTS:
        constrain_string = '#'+''.join([new_pzl[i] for i in constraint_lst])+'#'
        # find #*# and replace with ###
        if '#-#' in constrain_string: return ''
        new_constrain_string = constrain_string.replace('#*#','###')
        while constrain_string != new_constrain_string:
            constrain_string = new_constrain_string
            new_constrain_string=constrain_string.replace('#*#','###')
        constrain_string = new_constrain_string
        # find #**# and replace with ####
        if '#--#' in constrain_string or '#-*#' in constrain_string or '#*-#' in constrain_string: return ''
        new_constrain_string = constrain_string.replace('#**#','####')
        while constrain_string != new_constrain_string:
            constrain_string = new_constrain_string
            new_constrain_string=constrain_string.replace('#**#','####')
        constrain_string = new_constrain_string

        #update new_pzl
        for index in range(len(constraint_lst)):
            new_pzl[constraint_lst[index]] = constrain_string[index+1]

    if pzl == new_pzl: return pzl
    return constrain_word_length(new_pzl)

def mid_connect_check(pzl):
    if pzl.count('-')+pzl.count('*')==0: return True
    index = (gHEIGHT-1) // 2
    for constraint_lst in gVERTICAL_CONSTRAINTS:
        if pzl[constraint_lst[index]]!='#' and pzl[constraint_lst[index+1]]!='#':
            return True
    return False

def floodfill(pzl):
    dpos = [1,-1,gWIDTH,-gWIDTH]
    # -2 for block -1 unvisited 0 for first component 1 for second component
    vis = [-1]*len(pzl)
    for idx in range(len(pzl)):
        if pzl[idx]=='#': vis[idx]=-2
    #label each component
    k=0
    for idx in range(len(vis)):
        if vis[idx]!=-1: continue
        floodfill_recur(idx,vis,k,dpos)
        k+=1
    #either 1 or two components, if two block each
    #if k==1: return [pzl]
    comp_pzl = [['#' if vis[i]==0 else pzl[i] for i in range(len(pzl))]]
    comp_pzl += [['#' if vis[i]==1 else pzl[i] for i in range(len(pzl))]]
    return comp_pzl

def clean_floodfill(pzl):
    dpos = [1,-1,gWIDTH+2,-gWIDTH-2]
    #surround pzl in #
    blocked_pzl = ['#']*(gWIDTH+2)
    for i in range(0,len(pzl)+1, gWIDTH): blocked_pzl+=['#']+pzl[i:i+gWIDTH]+['#']
    blocked_pzl += ['#']*(gWIDTH + 2)
    # -2 for block -1 unvisited 0 for first component 1 for second component
    vis = [-1]*len(blocked_pzl)
    for idx in range(len(blocked_pzl)):
        if blocked_pzl[idx]=='#': vis[idx]=-2
    #label each component
    k=0
    for idx in range(len(blocked_pzl)):
        if vis[idx]!=-1: continue
        floodfill_recur(idx,vis,k,dpos)
        k+=1
    #either 1 or two components, if two block each
    if k:
        comp_pzl = []
        for comp in range(2):
            new_pzl = [i for i in blocked_pzl]
            for index in range(len(blocked_pzl)):
                if vis[index]==comp:
                    new_pzl[index]='#'
            #unblock
            starter = gWIDTH+3
            unblocked_new_pzl = []
            while len(unblocked_new_pzl)<len(pzl):
                unblocked_new_pzl+=[new_pzl[starter]]
                starter+=1
                if (starter+1)%(gWIDTH+2)==0:
                    starter+=2
            comp_pzl += [unblocked_new_pzl]
        return comp_pzl
    else:
        return [pzl]

def floodfill_recur(index,vis,k,dpos):
    if index < 0 or index >= len(vis): return
    if vis[index]!=-1: return
    vis[index]=k
    for pos in dpos:
        if index%gWIDTH==0 and pos==-1: continue
        if (index+1)%gWIDTH == 0 and pos==1: continue
        floodfill_recur(index+pos,vis,k,dpos)

def brute_force_blocks(pzl, index_lst):
    #verify validity in above step
    if pzl.count('#')==(1+gBLOCKCOUNT)//2: return pzl
    if pzl.count('#')>(1+gBLOCKCOUNT)//2 or not index_lst: return []

    while index_lst:
        #fill in first block
        temp = index_lst.pop()
        pzl[temp]='#'
        #check constraint lists for length (if #**# --> ####)
        new_pzl = constrain_word_length(pzl)
        #check connected in O(n) floodfill (change to iterative later)
        if new_pzl and mid_connect_check(new_pzl):
            for comp_pzl in clean_floodfill(new_pzl):
                if not mid_connect_check(comp_pzl): continue
                new_index_lst = lookup_index_lst(comp_pzl)
                bF = brute_force_blocks(comp_pzl, new_index_lst)
                if bF: return bF
        pzl[temp]='-'

def solve_blocks(pzl):
    if gBLOCKCOUNT==gWIDTH*gHEIGHT: return ['#']*gWIDTH*gHEIGHT
    #set up seeded pzl
    pzl = temp_words(pzl)
    if gWIDTH%2 and gHEIGHT%2: pzl[-1]=['-','#'][gBLOCKCOUNT%2]
    #only look at asterisked
    index_lst = lookup_index_lst(pzl)
    #solve blocks
    pzl = brute_force_blocks(pzl,index_lst)
    #assemble puzzle
    complete_pzl = pzl[:-1]+[pzl[-1]]*(not gHEIGHT%2 or not gWIDTH%2)+pzl[::-1]
    complete_pzl = place_words(complete_pzl)
    return complete_pzl

def main():
    if not args:
        print('Input please')
        exit()
    start_time = time.process_time()
    pzl = parse_input()
    lookup_constraints()
    print_puzzle(solve_blocks(pzl))
    print('Elapsed Time: ' + str(time.process_time() - start_time) + 's')
if __name__ == '__main__': main()