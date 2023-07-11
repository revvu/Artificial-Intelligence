# Reevu Adakroy pd. 7
# started 2/21/2021

import sys; args = sys.argv[1:]
import re

gHEIGHT, gWIDTH, gBLOCKCOUNT = 0, 0, 0
gHORIZONTAL, gVERTICAL = [],[]

def parse_input():
    global gBLOCKCOUNT, gHORIZONTAL, gVERTICAL
    for arg in args:
        if re.fullmatch(r'\d+x\d+',arg): parse_dimensions(arg)
        elif re.fullmatch(r'\d+',arg): gBLOCKCOUNT = int(arg)
        elif re.fullmatch(r'.*\.txt',arg): continue
        elif re.fullmatch(r'H\d+x\d+\w*',arg): gHORIZONTAL+=[arg]
        elif re.fullmatch(r'V\d+x\d+\w*',arg): gVERTICAL+=[arg]

    pzl = '-'*gWIDTH*gHEIGHT
    return pzl

def parse_dimensions(arg):
    global gHEIGHT,gWIDTH
    x_loc = arg.find('x')
    gHEIGHT = int(arg[0:x_loc])
    gWIDTH = int(arg[x_loc+1:])

def print_puzzle(pzl):
    for i in range(0,len(pzl),gWIDTH): print(' '.join([*pzl[i:i+gWIDTH]]))

def main():
    pzl = parse_input()
    print_puzzle(pzl)
    print('blocked squared count: '+ str(gBLOCKCOUNT))

if __name__ == '__main__': main()