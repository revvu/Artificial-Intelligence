import sys; args = sys.argv[1:]
# Reevu Adakroy, pd. 7
import time

def manhattan(pzl, goal, width):
    total = 0
    for i in range(len(pzl)):
        if pzl[i]=='_': continue
        s = goal.index(pzl[i])
        total+= single_manhattan(s, i, width)
    return total

def single_manhattan(s, i, width):
    return abs(s // width - i // width) + abs(s % width - i % width)

def find_height(str):
    n = int(len(str)**0.5)
    while len(str) % n != 0:
        n+= -1
    return n

def inversion_count(str):
    str = str.replace('_', '')
    return sum(str[x]>y for x in range(len(str)) for y in str[x+1:])

def swap(str, index1, index2):
    pzl = [*str]
    pzl[index1], pzl[index2] = pzl[index2], pzl[index1]
    return ''.join(pzl)

def neighbors(str, myDct):
    s = str.index('_')
    return [(swap(str, val[0], s), val[0], s, val[1]) for val in myDct[s]]

def parsePath(dct, goal):
    str = goal
    lst=[]
    while str != '':
        lst.insert(0, str)
        str= dct[str]
    return lst

def solvable(root, goal, width):
    return not (width%2 == 1 and (inversion_count(root)%2!=inversion_count(goal)%2) or width%2 == 0 and ((inversion_count(root)+root.index('_')//width)%2 != (inversion_count(goal)+goal.index('_')//width)%2))

def lookup(width, length):
    myDct = {}
    for s in range(length):
        lst = []
        col = s%width
        row = s // width

        if col > 0:
            lst.append((s-1, True))
        if col < width - 1:
            lst.append((s+1, True))
        if row > 0:
            lst.append((s - width, False))
        if row < length // width - 1:
            lst.append((s+width, False))
        myDct[s]=lst

    return myDct

def solve(root, goal, width):
    #already solved
    if root == goal: return 0

    #not solvable
    if not solvable(root, goal, width): return -1

    #Create openSet
    openSet = [(manhattan(root, goal, width), root, 0, root.find('_'))]
    backSetOne = []
    backSetTwo = []
    #Create closedSet
    closedSet = {}

    indexTable = lookup(width, len(root))

    while openSet or backSetOne or backSetTwo:
        #find pzl with lowest estimate in openSet
        while not openSet:
            openSet, backSetOne, backSetTwo = backSetOne, backSetTwo, []

        est, pzl, level, s = openSet.pop()

        if pzl in closedSet: continue
        closedSet[pzl] = level

        for val in indexTable[s]:
            nbr = (swap(pzl, val[0], s), val[0], s, val[1])
            if nbr[0] == goal:
                return level+1
            if nbr[0] in closedSet:
                continue
            md = est
            i = goal.index(pzl[nbr[1]])
            if nbr[3]: md += abs(nbr[2]%width - i%width) - abs(nbr[1]%width - i%width)
            else: md += abs(nbr[2]//width - i//width) - abs(nbr[1]//width - i//width)
            estimate = 1 + md
            if estimate == est: openSet.append((estimate, nbr[0], level+1, nbr[1]))
            elif estimate == est+1: backSetOne.append((estimate, nbr[0], level+1, nbr[1]))
            else: backSetTwo.append((estimate, nbr[0], level+1, nbr[1]))

    return -1

def main():
    start_total_time = time.process_time()

    if not args:
        lst = []
        print('No list of puzzles provided')
        exit()

    else:
        lst = open(args[0], 'r').read().replace('.', '_').replace('0', '_').splitlines()

    goal = lst[0]
    index = 0
    start_process_time = time.process_time()
    while index<len(lst):
        start = lst[index]
        width = len(start)//find_height(start)
        start_time=time.process_time()
        path_length = solve(start, goal, width)
        print(str(index)+': ' + start + ' solved in ' + str(path_length) + ' steps in ' + str(time.process_time() - start_time) +' seconds')
        index+=1
    print('Total process time: ' + str(time.process_time()-start_process_time) + 's')
    print('Total time time: ' + str(time.process_time() - start_total_time) + 's')

if __name__ == '__main__': main()