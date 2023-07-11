import sys; args = sys.argv[1:]
# Reevu Adakroy, pd. 7
import time

def speedmanhattan(pzl, goal, width):
    total = 0
    #I called them sets but they're dictionaries
    pzl_set = {}
    goal_set = {}
    for i in range(len(pzl)):
        pzl_set[pzl[i]] = i

    for i in range(len(goal)):
        goal_set[goal[i]] = i

    for ch in pzl_set:
        total+= single_manhattan(pzl_set[ch], goal_set[ch], width)

    return total



def manhattan(pzl, goal, width):
    total = 0
    for i in range(len(pzl)):
        if pzl[i]=='_': continue
        s = goal.index(pzl[i])
        total+= single_manhattan(s, i, width)
    return total

def single_manhattan(s, i, width):
    return abs(s // width - i // width) + abs(s % width - i % width)

def find_height(st):
    n = int(len(st)**0.5)
    while len(st) % n != 0:
        n+= -1
    return n

def inversion_count(st):
    st = st.replace('_', '')
    return sum(st[x]>y for x in range(len(st)) for y in st[x+1:])

def swap(str, index1, index2):
    pzl = [*str]
    pzl[index1], pzl[index2] = pzl[index2], pzl[index1]
    return ''.join(pzl)

def neighbors(st, myDct):
    s = st.index('_')
    return [(swap(st, val[0], s), val[0], s, val[1]) for val in myDct[s]]

def parsePath(dct, goal):
    s = goal
    lst=[]
    while s != '':
        lst.insert(0, s)
        s= dct[s]
    return lst

def solvable(root, goal, width):
    return not (width%2 == 1 and (inversion_count(root)%2!=inversion_count(goal)%2) or width%2 == 0 and ((inversion_count(root)+root.index('_')//width)%2 != (inversion_count(goal)+goal.index('_')//width)%2))

def lookup(width, length):
    myDct = {}
    for s in range(length):
        myDct[s] = []
        col = s%width
        row = s // width

        if col > 0:
            myDct[s].append((s-1, True))
        if col < width - 1:
            myDct[s].append((s+1, True))
        if row > 0:
            myDct[s].append((s - width, False))
        if row < length // width - 1:
            myDct[s].append((s+width, False))

    return myDct

def lookupIndex(goal):
    myDct = {}
    for ch in goal:
        myDct[ch]=goal.index(ch)
    return myDct


def solve(root, goal, width):
    #already solved
    if root == goal: return 0

    #not solvable
    if not solvable(root, goal, width): return -1

    #Create openSet
    #you will always get either f, f+1, or f+2. once f is finished, shift.

    # openSetList = [[(speedmanhattan(root, goal, width), root, 0, root.find('_'), -1)], [], []]
    #set of list of lists is slower than 3 lists

    #don't need actual value for manhattan distance, just need to compare between
    #-1 is filler for lack of parent
    openSet, backSetOne, backSetTwo = [(0, root, 0, root.find('_'), -1)], [], []
    #Create closedSet
    closedSet = {}

    indexTable = lookup(width, len(root))
    spaceTable = lookupIndex(goal)

    while openSet or backSetOne or backSetTwo:
        #find pzl with lowest estimate in openSet
        while not openSet:
            openSet, backSetOne, backSetTwo = backSetOne, backSetTwo, []

        est, pzl, level, s, gp = openSet.pop()

        if pzl in closedSet: continue
        closedSet[pzl] = level

        lst = [*pzl]
        #don't want to make the list every time, just make it once and make shallow copies

        for val in indexTable[s]:
            p = lst[:]
            priorPos = uPos = s
            nextPos=val[0]
            p[priorPos], p[uPos], p[nextPos], priorPos = p[uPos], p[nextPos], p[priorPos], nextPos
            nbr = ''.join(p)

            #skip grandparents
            if nbr == gp: continue

            #already saw it
            if nbr in closedSet: continue

            #we have arrived :)
            if nbr == goal: return level+1

            #reset md to stored
            md = est
            i = spaceTable[pzl[val[0]]]

            #val[1] stores whether it was a row shift or a column shift (False --> row change)
            if val[1]: md += abs(s%width - i%width) - abs(val[0]%width - i%width)+1
            else: md += abs(s//width - i//width) - abs(val[0]//width - i//width)+1
            #no more manhattan calculating for the whole puzzle :)))
            #+1 for the change in level

            #[openSet, backSetOne, backSetTwo][est-md].append((md, nbr, level+1, val[0], pzl))
            #if else ladder seems slightly faster than list
            if md == est: openSet.append((md, nbr, level+1, val[0], pzl))
            elif md == est+1: backSetOne.append((md, nbr, level+1, val[0], pzl))
            else: backSetTwo.append((md, nbr, level+1, val[0], pzl))

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