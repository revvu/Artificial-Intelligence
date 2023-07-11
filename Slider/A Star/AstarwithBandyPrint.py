import sys; args = sys.argv[1:]
# Reevu Adakroy, pd. 7
import time

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
        str= dct[str][1]
    return lst

def solvable(root, goal, width):
    return not (width%2 == 1 and (inversion_count(root)%2!=inversion_count(goal)%2) or width%2 == 0 and ((inversion_count(root)+root.index('_')//width)%2 != (inversion_count(goal)+goal.index('_')//width)%2))

def solve(root, goal, width):
    #already solved
    if root == goal: return [root]

    #not solvable
    if not solvable(root, goal, width): return ['Unsolvable']

    #Create openSet
    openSet = [(manhattan(root, goal, width), root, '')]
    #Create closedSet
    closedSet = {}

    while openSet:
        #find pzl with lowest estimate in openSet
        openSet.sort()
        level, pzl, pnt = openSet.pop(0)
        level = level - manhattan(pzl, goal, width)

        if pzl in closedSet: continue
        closedSet[pzl] = (level, pnt)

        for nbr in neighbors(pzl, width):
            if nbr == goal:
                closedSet[goal] = (level+1, pzl)
                return parsePath(closedSet, goal)
            if nbr in closedSet: continue
            est = level+1 + manhattan(nbr, goal, width)
            openSet.append((est, nbr, pzl))
    return []

def fixListLength(lst, length):
    return lst+[0]*(length-len(lst))       #length is always >= len(lst)

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
        print(str(index)+': ' + start + ' solved in ' + str(len(path_length)-1) + ' steps in ' + str(time.process_time() - start_time) +' seconds')
        print(print_bands(path_length, 5, width))
        index+=1
    print('Total process time: ' + str(time.process_time()-start_process_time) + 's')
    print('Total time time: ' + str(time.process_time() - start_total_time) + 's')

if __name__ == '__main__': main()
