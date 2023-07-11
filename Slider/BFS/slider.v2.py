import sys; args = sys.argv[1:]
# Reevu Adakroy, pd. 7
import time
import random
from queue import PriorityQueue

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

    #if swap rows, then inversion count may have changed
    lst = []
    if col > 0:
        lst.append((swap(str, s-1, s), True))
    if col < width-1:
        lst.append((swap(str, s, s+1), True))
    if row > 0:
        str2 = swap(str, s-width, s)
        m = inversion_count(str[s-width:s+1]) - inversion_count(str2[s-width:s+1])
        lst.append((str2, m>0))
        lst.append((str2, True))

    if row < len(str)//width-1:
        str2 = swap(str, s, s+width)
        m = inversion_count(str[s:s+width+1]) - inversion_count(str2[s:s+width+1])
        lst.append((str2, m>0))
        lst.append((str2, True))

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
    r = inversion_count(root)
    g = inversion_count(goal)
    if width%2 == 1 and (r%2!=g%2):
        return []
    #if even, the parity of inversion count + row of _ of start and goal equal
    elif width%2 == 0 and ((r+root.index('_')//width)%2 != (g+goal.index('_')//width)%2):
        return []

    parseMe = [root]
    good_index = 1
    dctSeen = { root: '' }
    while parseMe:
        item = parseMe.pop(0)
        if item == goal:
            return parsePath(dctSeen,goal)
        for nbr in neighbors(item, width):
            if nbr[0] not in dctSeen:
                if nbr[1]:
                    parseMe.insert(good_index, nbr[0])
                    good_index+=1
                else:
                    parseMe.append(nbr[0])
                dctSeen[nbr[0]]=item
    return []

def parseDegree(dct):
    lst = []
    for i in dct:
        lst = fixListLength(lst, dct[i]+1)
        lst[dct[i]] += 1
    return lst

def degreeDistribution(root, width):
    parseMe = [root]
    dctSeen = { root: 0}
    while parseMe:
        item = parseMe.pop(0)
        for nbr in neighbors(item, width):
            if nbr not in dctSeen:
                parseMe.append(nbr)
                dctSeen[nbr]=dctSeen[item]+1
    return parseDegree(dctSeen)

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
    if args:
        start_time = time.process_time()
        start = args[0]
        goal = ''.join(sorted([*args[0].replace('_', '')]))+'_' if len(args) != 2 else args[1]

        width = len(start) // find_height(start)

        lst = solve(start, goal, width)
        if len(lst) == 0:
            print(print_grid(start, width))
        else:
            print(print_bands(lst, 5, width))

        print('Steps: ' + str(len(lst)-1))
        print('Time: ' + '{0:.3g}'.format(time.process_time()-start_time) + 's')

    else:
        PUZZLES = 500
        goal = '12345678_'
        startTime = time.process_time()
        statsCtr = [0]*5
        # 0: Impossible cnt 1: Possible cnt, 2: Impossibles Total time 3: Possibles Total time, 4: Sum of path lengths

        for i in range(PUZZLES):
            start = ''.join(random.sample('12345678_', 9))
            my_time = time.process_time()
            width = len(start)//find_height(start)
            path = solve(start, goal, width)
            end = time.process_time() - my_time
            statsCtr[4] += len(path)
            if len(path) == 0:
                statsCtr[0]+=1
                statsCtr[2]+=end
            else:
                statsCtr[1]+=1
                statsCtr[3]+=end

            if not (i + 1) % 25: print("*", end='', flush=True)

        endTime = time.process_time() - startTime
        print()
        print('Total Time: ' + '{0:.3g}'.format(endTime) + 's')
        print('Average Impossible time: ' + '{0:.3g}'.format(statsCtr[2] / statsCtr[0]))
        print('Impossible count: ' + str(statsCtr[0]))
        print('Average path length: ' + '{0:.3g}'.format(statsCtr[4] / PUZZLES))
        print('Average Possible Time: ' + '{0:.3g}'.format(statsCtr[3] / statsCtr[1]))

if __name__ == '__main__': main()
#print(degreeDistribution('12345678_', 3))