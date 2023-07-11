import sys; args = sys.argv[1:]
# Reevu Adakroy, pd. 7
import time
import random

def manhattan(pzl, goal, width):
    lst = []
    for i in range(len(pzl)):
        row = i // width
        col = i % width
        s = goal.index(pzl[i])
        md = abs(s // width - row) + abs(s % width - col)
        lst = fixListLength(lst, md+1)
        lst[md] += 1

    return sum(i*lst[i] for i in range(len(lst)) )

def find_height(str):
    n = int(len(str)**0.5)
    while len(str) % n != 0:
        n+= -1
    return n

def inversion_count(str):
    str = str.replace('_', '')
    return sum(str[x]>y for x in range(len(str)) for y in str[x+1:])

def swap(str, index1, index2):
    return str[:index1] + str[index2] + str[index1+1:index2]+str[index1]+str[index2+1:]

def neighbors(str, width):
    s = str.index('_')
    row = s // width
    col = s % width

    lst = []
    if col > 0:
        lst.append(swap(str, s-1, s))
    if col < width-1:
        lst.append(swap(str, s, s+1))
    if row > 0:
        lst.append(swap(str, s-width, s))
    if row < len(str)//width-1:
        lst.append(swap(str, s, s+width))
    return lst

def parsePath(dct, goal):
    str = goal
    lst=[]
    while str != '':
        lst.insert(0, str)
        str= dct[str]
    return lst

def solve(root, goal, width):
    #if odd, the parity of inversion count of start and goal equal
    if width%2 == 1 and (inversion_count(root)%2!=inversion_count(goal)%2):
        return []
    #if even, the parity of inversion count + row of _ of start and goal equal
    elif width%2 == 0 and ((inversion_count(root)+root.index('_')//width)%2 != (inversion_count(goal)+goal.index('_')//width)%2):
        return []

    if root == goal: return [root]
    parseMe = [(manhattan(root,goal,width), root)]
    dctSeen = { root: ''}
    while parseMe:
        md, item = parseMe.pop(0)
        for nbr in neighbors(item, width):
            if nbr in dctSeen: continue

            dctSeen[nbr]=item
            mdn = manhattan(nbr, goal, width)
            parseMe.append((mdn, nbr))

            if nbr == goal: return parsePath(dctSeen,goal)
        parseMe.sort()
    return []

def fixListLength(lst, length):
    return lst+[0]*(length-len(lst))       #length is always >= len(lst)

def print_grid(str, width):
    ret = ''
    lst = [*str]
    while lst:
        for i in range(width):
            ret += lst.pop(0)
        ret+= '\n'
    return ret

def print_bands(slide_list, row, width):
    ret = ''
    lst = [[*i] for i in slide_list]
    while lst:
        temp = lst[:row]
        lst = lst[row:]
        for a in range(len(temp[0])//width):
            for i in temp:
                ret += ''.join(i[a*width:(a+1)*width]) + '  '
            ret+='\n'
        ret+='\n'
    return ret

def main():
    start_time = time.process_time()
    lst = open(args[0], 'r').read().splitlines()
    stats = [0] * 4
    while time.process_time() - start_time < 90 and stats[0] < len(lst):
        start = lst[stats[0]]
        goal = ''.join(sorted([*start.replace('_', '')]))+'_'
        width = len(start)//find_height(start)
        path = solve(start, goal, width)
        stats[0]+=1
        if len(path) > 0:
            stats[1]+=1
            stats[2]+= len(path)

        if not (stats[0] + 1)%100: print('*', end='', flush=True)

    print()
    print('Total number of puzzles: ' + str(stats[0]))
    print('Total number of solvable puzzles: '  + str(stats[1]))
    print('Average path length for solvable puzzles: ' + '{0:.3g}'.format(stats[2] / stats[1]))
    print('Total Time: ' + '{0:.3g}'.format(time.process_time()-start_time) + 's')

if __name__ == '__main__': main()
