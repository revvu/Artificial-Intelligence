def swap(pzl , num1 , num2, num3):
    lst = [*pzl]
    lst[num1], lst[num2], lst[num3] = lst[num3], '.', lst[num1]
    return ''.join(lst)

def neighbors(puzzle, lookup):
    lst = []

    for i in range(len(puzzle)):
        if puzzle[i] == '.': continue
        for val in lookup[i]:
            if puzzle[val[0]] == '.' and puzzle[val[1]] != '.' or (puzzle[val[0]] != '.' and puzzle[val[1]] == '.'):
                lst.append((swap(puzzle, val[0], i, val[1]), val[2]))
    return lst

def isSolved(puzzle):
    return sum(n=='1' for n in [*puzzle]) == 1

def lookupTable():
    myDct = {
        0: [],
        1: [(0,3, '1/')],
        2: [(0,5, ('2'+r'\'')[:2])],
        3: [(1,6, '3/')],
        4: [(1,8, ('4'+r'\'')[:2]), (2,7, '4/'), (3,5, '4-')],
        5: [(2,9, ('5'+r'\'')[:2])],
        6: [(3, 10, '6/')],
        7: [(3,12, ('7'+r'\'')[:2]),(4,11, '7/'),(6,8, '7-')],
        8: [(4, 13, ('8'+r'\'')[:2]), (5, 12, '8/'), (7,9, '8-')],
        9: [(5, 14,'9/')],
        10: [],
        11: [(10, 12, '11-')],
        12: [(11, 13, '12-')],
        13: [(12, 14, '13-')],
        14: []
    }
    return myDct

def createList():
    output = []
    for x in range(15):
        output.append(('.'* x) + '1' + ('.' * (14-x)))
    return output

def solve(puzzle, goal):
    #if odd, the parity of inversion count of start and goal equal

    if puzzle in goal: return puzzle.find('.')

    parseMe = [puzzle]
    dctSeen = {puzzle: str(puzzle.find('.')) + ' '}

    lookup = lookupTable()

    while parseMe:
        pzl = parseMe.pop(0)
        for nbr, st in neighbors(pzl, lookup):
            if nbr in goal: return dctSeen[pzl] + st
            if nbr not in dctSeen:
                parseMe.append(nbr)
                dctSeen[nbr]=dctSeen[pzl]+st+' '

    return []

start = '.11111111111111'

lookup = lookupTable()

#variation 1:
goal = createList()[0]

#variation 2:
#goal = createList()[1:]

print(solve(start, goal))