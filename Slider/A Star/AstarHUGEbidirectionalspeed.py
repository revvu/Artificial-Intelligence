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

def lookupIndex(goal):
    myDct = {}
    for i in goal:
        myDct[i]=goal.index(i)
    return myDct

def solve(root, goal, width):
    #already solved
    if root == goal: return 0

    #not solvable
    if not solvable(root, goal, width): return -1

    #Create openSet
    openSet = [(manhattan(root, goal, width), root, 0, root.find('_'), -1)]
    backSetOne = []
    backSetTwo = []
    #Create closedSet
    closedSet = {}

    indexTable = lookup(width, len(root))
    spaceTable = lookupIndex(goal)

    #BFS
    parseMe = [goal]
    dctSeen = {goal: 0}
    index = 0

    while openSet or backSetOne or backSetTwo:
        #find pzl with lowest estimate in openSet

        while not openSet:
            openSet, backSetOne, backSetTwo = backSetOne, backSetTwo, []

        est, pzl, level, s, gp = openSet[-1]

        if pzl in dctSeen:
            lst = []
            for i in openSet + backSetOne + backSetTwo:
                if i[1] in dctSeen:
                    lst.append(i[2] + dctSeen[pzl])
            return min(lst)

        est, pzl, level, s, gp = openSet.pop()

        if pzl in closedSet:
            continue
        closedSet[pzl] = level

        lst = [*pzl]

        for val in indexTable[s]:
            p = lst[:]
            priorPos = uPos = s
            nextPos=val[0]
            p[priorPos], p[uPos], p[nextPos], priorPos = p[uPos], p[nextPos], p[priorPos], nextPos
            nbr = ''.join(p)

            if nbr == gp: continue
            if nbr in closedSet: continue
            if nbr == goal: return level+1

            # if nbr in dctSeen:
            #     return level+1+dctSeen[nbr]

            md = est
            i = spaceTable[pzl[val[0]]]

            if val[1]: md += abs(s%width - i%width) - abs(val[0]%width - i%width)+1
            else: md += abs(s//width - i//width) - abs(val[0]//width - i//width)+1


            if md == est: openSet.append((md, nbr, level+1, val[0], pzl))
            elif md == est+1: backSetOne.append((md, nbr, level+1, val[0], pzl))
            else: backSetTwo.append((md, nbr, level+1, val[0], pzl))



        item = parseMe[index]
        index+=1

        s = item.index('_')

        lst = [*item]

        for val in indexTable[s]:
            p = lst[:]
            priorPos = uPos = s
            nextPos=val[0]
            p[priorPos], p[uPos], p[nextPos], priorPos = p[uPos], p[nextPos], p[priorPos], nextPos
            nbr = ''.join(p)

            if nbr not in dctSeen:
                parseMe.append(nbr)
                dctSeen[nbr]=dctSeen[item]+1

    return -1

def main():

    if not args:
        lst = []
        print('No list of puzzles provided')
        exit()

    else:
        lst = open(args[0], 'r').read().replace('.', '_').replace('0', '_').splitlines()

    goal = lst[0]
    index = 0
    start_process_time = time.process_time()
    total = 0
    while index<len(lst):
        start = lst[index]
        width = len(start)//find_height(start)
        start_time=time.process_time()
        path_length = solve(start, goal, width)
        total+=time.process_time()-start_time
        print(str(index)+': ' + start + ' solved in ' + str(path_length) + ' steps in ' + str(time.process_time() - start_time) +' seconds')
        index+=1
    print('Total process time: ' + str(total) + 's')
    print('Total time time: ' + str(time.process_time() - start_process_time) + 's')

if __name__ == '__main__': main()