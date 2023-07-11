import sys; args = sys.argv[1:]
# Reevu Adakroy, pd. 7
import time
import random

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

    #middle
    if not row in {0, len(str)//width - 1} and not col in {0, width-1}:
        return [swap(str, s, s+width), swap(str, s, s+1), swap(str, s-width,s), swap(str, s-1, s)]

    #corner
    if row==0 and col==0:
        return [swap(str, s, s+1), swap(str, s, s+width)]
    if row==0 and col==width-1:
        return [swap(str, s-1, s), swap(str, s, s+width)]
    if row==len(str)//width-1 and col==0:
        return [swap(str, s, s+1), swap(str, s-width, s)]
    if row==len(str)//width-1 and col==width-1:
        return [swap(str, s-1, s), swap(str, s-width, s)]

    #edge
    if row == 0:
        return [swap(str, s-1, s), swap(str, s, s+1), swap(str, s, s+width)]
    if row == len(str)//width-1:
        return [swap(str, s-1, s), swap(str, s, s+1), swap(str, s-width, s)]
    if col == 0:
        return [swap(str, s, s+1), swap(str, s, s+width), swap(str, s-width, s)]
    if col == width-1:
        return [swap(str, s-1, s), swap(str, s, s+width), swap(str, s-width, s)]
    return []

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

    parseMe = [root]
    dctSeen = { root: ''}
    while parseMe:
        item = parseMe.pop(0)
        if item == goal:
            return parsePath(dctSeen,goal)
        for nbr in neighbors(item, width):
            if nbr not in dctSeen:
                parseMe.append(nbr)
                dctSeen[nbr]=item
    return []

def fixListLength(lst, length):
    return lst+[0]*(length-len(lst))       #length is always >= len(lst)

def rand500():
    return [''.join(random.sample('12345678_', 9)) for x in range(500)]

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


