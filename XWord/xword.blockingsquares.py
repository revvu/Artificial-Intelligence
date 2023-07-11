# Reevu Adakroy pd. 7
# started 2/21/2021

import sys; args = sys.argv[1:]
import re

gHEIGHT = gWIDTH = gBLOCKCOUNT = 0
gHORIZONTAL, gVERTICAL = [],[]
g180LST = []

def parse_input():
    global gBLOCKCOUNT, gHORIZONTAL, gVERTICAL, g180LST
    for arg in args:
        if re.fullmatch(r'\d+x\d+',arg): parse_dimensions(arg)
        elif re.fullmatch(r'\d+',arg): gBLOCKCOUNT = int(arg)
        elif re.fullmatch(r'.*\.txt',arg): continue
        elif re.fullmatch(r'H\d+x\d+\w*',arg): gHORIZONTAL+=[arg]
        elif re.fullmatch(r'V\d+x\d+\w*',arg): gVERTICAL+=[arg]
    pzl = '-'*gWIDTH*gHEIGHT
    g180LST = [*range(len(pzl)-1,-1,-1)]
    return pzl

def parse_dimensions(arg):
    global gHEIGHT,gWIDTH
    x_loc = arg.find('x')
    gHEIGHT = int(arg[0:x_loc])
    gWIDTH = int(arg[x_loc+1:])

def print_puzzle(pzl):
    for i in range(0,len(pzl),gWIDTH): print(' '.join([*pzl[i:i+gWIDTH]]))

def place_blocks_180(pzl):
    exploded_pzl = [*pzl]
    filled_block_count = 0
    # if  blockcount odd, fill in middle
    if gBLOCKCOUNT%2:
        exploded_pzl[(len(pzl))//2]='#'
        filled_block_count+=1
    idx = 0
    while filled_block_count < gBLOCKCOUNT:
        if exploded_pzl[idx]=='-' and exploded_pzl[g180LST[idx]]=='-':
            exploded_pzl[idx]='#'
            exploded_pzl[g180LST[idx]]='#'
            filled_block_count+=2
        idx+=1

    return ''.join(exploded_pzl)

def place_words(pzl):
    exploded_pzl = [*pzl]
    for seed in gHORIZONTAL:
        row,col = re.findall(r'\d+', seed)
        row = int(row)
        col = int(col)
        word = str(re.search(r'(?!\w*\d)\w*', seed).group())
        for idx in range(len(word)):
            exploded_pzl[row*gWIDTH+col+idx]=word[idx]

    for seed in gVERTICAL:
        row,col = re.findall(r'\d+', seed)
        row = int(row)
        col = int(col)
        word = str(re.search(r'(?!\w*\d)\w*', seed).group())
        for idx in range(len(word)):
            exploded_pzl[(row+idx)*gWIDTH+col]=word[idx]

    return ''.join(exploded_pzl)

def main():
    pzl = parse_input()
    pzl = place_words(pzl)
    pzl = place_blocks_180(pzl)
    print_puzzle(pzl)

if __name__ == '__main__': main()