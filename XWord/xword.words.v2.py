import sys; args = sys.argv[1:]
# Reevu Adakroy pd. 7
# started 2/21/2021

import time
import re
import random

gHEIGHT = gWIDTH = gBLOCKCOUNT = gHALF_LENGTH = 0
gSEEDS, g180LST, gHORIZONTAL_CONSTRAINTS, gVERTICAL_CONSTRAINTS = [],[],[],[]
gEDGESET = set()
gWORD_LST = []
gROWS, gCOLS = [],[]
gHORIZONTAL_SKELETON = []
gVERTICAL_SKELETON = []
gWORD_DICTIONARY = {}
gBINARY_DICT = {}

def parse_input():
    global gBLOCKCOUNT, gSEEDS, g180LST, gHALF_LENGTH, gEDGESET, gWORD_LST
    for arg in args:
        if re.fullmatch(r'\d+x\d+',arg): parse_dimensions(arg)
        elif re.fullmatch(r'\d+',arg): gBLOCKCOUNT = int(arg)
        elif re.fullmatch(r'.*\.txt',arg): gWORD_LST = [word.strip() for word in open(arg, 'r').readlines()]
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
    global gVERTICAL_CONSTRAINTS, gHORIZONTAL_CONSTRAINTS, gROWS, gCOLS
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

    #word horizontal
    for idx in range(0, gHEIGHT):
        gROWS+=[indexed_board[idx * gWIDTH:idx * gWIDTH + gWIDTH]]

    #word vertical
    for idx in range(0, gWIDTH):
        vertical_constraint_lst = []
        for index in range(idx, len(indexed_board), gWIDTH): vertical_constraint_lst+=[indexed_board[index]]
        gCOLS+=[vertical_constraint_lst]

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

def place_seeds(pzl):
    for seed in gSEEDS:
        row,col = [int(x) for x in re.findall(r'\d+', seed)]
        word = str(re.search(r'(?!\w*\d).*', seed).group())
        for idx in range(len(word)): pzl[row*gWIDTH+col+idx*gWIDTH**(seed[0]=='V' or seed[0]=='v')]=word[idx].lower()
    return pzl

def lookup_index_lst(pzl):
    # bucket by edge/near-block and not
    # still not sufficient because derived squares can make the puzzle not good placement
    primary = []
    secondary = []
    dpos = [1,-1,gWIDTH,-gWIDTH]
    for i in range(len(pzl)):
        if pzl[i]!='*': continue
        if i==0 or i==gWIDTH-1:
            secondary+=[i]
            continue

        added = False
        for pos in dpos:
            if gBLOCKCOUNT<gWIDTH*gHEIGHT//2:
                for multiple in range(3):
                    index = i+pos*(multiple+1)
                    if len(pzl)+gWIDTH > index >= len(pzl): index = g180LST[index]
                    if 0> index or index >= len(pzl): continue
                    if pzl[index]=='#' or index-pos in gEDGESET:
                        secondary+=[i]
                        added=True
                        break
        if not added: primary += [i]

    #sort by distance to center
    return secondary+primary

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
            for comp_pzl in floodfill(new_pzl):
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
    complete_pzl = place_seeds(complete_pzl)

    return [complete_pzl[i] if complete_pzl[i]!='*' else '-' for i in range(len(complete_pzl))]

def build_binary_dict(max_length):
    global gBINARY_DICT
    for num in range(2**(max_length-1)):
        gBINARY_DICT[num]=('{0:0' + str(max_length)+'b}').format(num)

def binary_string(num, length):
    return gBINARY_DICT[num][-length:]

def parse_word_dict(word_lengths_combined):
    word_lengths,max_word_length = word_lengths_combined
    global gWORD_DICTIONARY
    build_binary_dict(max_word_length)

    for base_word in gWORD_LST:
        word_length = len(base_word)
        if word_length not in word_lengths: continue
        if not re.fullmatch(r'\w+', base_word): continue
        for num in range(2**(word_length-1)):
            basis = binary_string(num,word_length)
            modified_word = ''
            modified_word2 = ''
            for i in range(word_length):
                if basis[i]=='1':
                    modified_word += base_word[i]
                    modified_word2 += '-'
                else:
                    modified_word += '-'
                    modified_word2 += base_word[i]

            if modified_word in gWORD_DICTIONARY: gWORD_DICTIONARY[modified_word]+=[base_word]
            else: gWORD_DICTIONARY[modified_word]=[base_word]

            if modified_word2 in gWORD_DICTIONARY: gWORD_DICTIONARY[modified_word2]+=[base_word]
            else: gWORD_DICTIONARY[modified_word2]=[base_word]

def place_words(pzl, index, word, vertical):
    row = index // gWIDTH
    col = index % gWIDTH
    for idx in range(len(word)): pzl[row*gWIDTH+col+idx*gWIDTH**vertical] = word[idx].lower()

def find_word_lengths(pzl):
    word_lengths = set()
    max_word_length = 0
    for row in range(gHEIGHT):
        count = 0
        for col in range(gWIDTH):
            if pzl[row*gWIDTH+col]=='#':
                word_lengths.add(count)
                max_word_length = max(count, max_word_length)
                count = 0
            else: count+=1
        word_lengths.add(count)
        max_word_length = max(count, max_word_length)
    for col in range(gWIDTH):
        count = 0
        for row in range(gHEIGHT):
            if pzl[row*gWIDTH+col]=='#':
                word_lengths.add(count)
                max_word_length = max(count, max_word_length)
                count = 0
            else: count+=1
        word_lengths.add(count)
        max_word_length = max(count, max_word_length)
    return word_lengths, max_word_length

def parse_skeleton(pzl):
    global gHORIZONTAL_SKELETON, gVERTICAL_SKELETON
    for row in range(gHEIGHT):
        col, length,word_start_index = 0,0,0
        inWord = False
        while col<gWIDTH:
            if pzl[row*gWIDTH+col]=='#':
                if inWord:
                    gHORIZONTAL_SKELETON+=[(word_start_index,length)]
                inWord = False
            else:
                if not inWord:
                    word_start_index = row*gWIDTH+col
                    inWord = True
                    length=1
                else:
                    length+=1
            col+=1
        if (word_start_index, length) not in gHORIZONTAL_SKELETON: gHORIZONTAL_SKELETON += [(word_start_index, length)]

    for col in range(gWIDTH):
        row, length,word_start_index = 0,0,0
        inWord = False
        while row<gHEIGHT:
            if pzl[row*gWIDTH+col]=='#':
                if inWord:
                    gVERTICAL_SKELETON+=[(word_start_index,length)]
                inWord = False
            else:
                if not inWord:
                    word_start_index = row*gWIDTH+col
                    inWord = True
                    length=1
                else:
                    length+=1
            row+=1
        if (word_start_index, length) not in gVERTICAL_SKELETON: gVERTICAL_SKELETON += [(word_start_index, length)]

def solve_words(pzl):
    parse_word_dict(find_word_lengths(pzl))
    parse_skeleton(pzl)
    for h_index,h_length in gHORIZONTAL_SKELETON:
        constraint = ''.join(pzl[i] for i in range(h_index,h_index+h_length))
        word = random.choice(gWORD_DICTIONARY[constraint])
        place_words(pzl,h_index,word,False)
    return pzl

def main():
    if not args:
        print('Input please')
        exit()

    start_time = time.process_time()
    pzl = parse_input()
    lookup_constraints()
    blocks = solve_blocks(pzl)
    print_puzzle(blocks)
    print()
    print_puzzle(solve_words(blocks))
    # print()

    # parse_skeleton(blocks)
    # print(gHORIZONTAL_SKELETON)
    # print(gVERTICAL_SKELETON)

    #parse_word_dict(find_word_lengths(blocks))
    #print(gWORD_DICTIONARY)
    print('Elapsed Time: ' + str(time.process_time() - start_time) + 's')

if __name__ == '__main__': main()