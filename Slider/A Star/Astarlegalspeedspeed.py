import sys; args = sys.argv[1:]
# Reevu Adakroy, pd. 7
import time

def manhattan(pzl, goal, width):
    total = 0
    for i in range(len(pzl)):
        if pzl[i]=='_': continue
        s = goal.index(pzl[i])
        total+= abs(s // width - i // width) + abs(s % width - i % width)
    return total

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

def solvable(root, goal, width):
    return not (width%2 == 1 and (inversion_count(root)%2!=inversion_count(goal)%2) or width%2 == 0 and ((inversion_count(root)+root.index('_')//width)%2 != (inversion_count(goal)+goal.index('_')//width)%2))

def priorityInsert(lst, a):
    if not lst:
        lst.append(a)
    else:
        start = 0
        end = len(lst)
        while start != end and start != end-1:
            mid = (start+end)//2
            if lst[mid] < a:
                end = mid
            else: start = mid
        if a < lst[start]:
            lst.insert(end, a)
        else: lst.insert(start, a)

def solve(root, goal, width):
    #already solved
    if root == goal: return 0

    #not solvable
    if not solvable(root, goal, width): return -1

    #Create openSet
    openSet = [(p:=manhattan(root, goal, width), root, p)]
    #Create closedSet
    closedSet = {}

    while openSet:
        #find pzl with lowest estimate in openSet
        level, pzl, md = openSet.pop()
        level = level - md

        if pzl in closedSet: continue
        closedSet[pzl] = level

        for nbr in neighbors(pzl, width):
            if nbr == goal: return level+1
            if nbr in closedSet: continue
            md = manhattan(nbr, goal, width)
            est = level+1 + md
            priorityInsert(openSet, (est, nbr, md))
    return -1

def fixListLength(lst, length):
    return lst+[0]*(length-len(lst))       #length is always >= len(lst)

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
