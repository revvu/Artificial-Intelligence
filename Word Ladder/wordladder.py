import sys; args = sys.argv[1:]
# Reevu Adakroy, pd. 7
import time

start_time = time.time()
myWords = open(args[0], 'r').read().splitlines()

def fixListLength(lst, length):
    if len(lst) < length:
        lst += [0 for x in range(len(lst), length)]
    return lst

def degree_distribution(graph):
    degree = []
    for n in graph:
        degree = fixListLength(degree, len(graph[n])+1)
        degree[len(graph[n])] += 1
    return degree

def second_degree(graph, degree):
    for n in graph:
        if len(graph[n]) == degree:
            return n
    return ''

def neighbors(graph, str):
    return graph[str]

def connected_components(graph):
    #returns a list with index as size of component - 1 and value is count of that size
    keys = list(graph.keys())
    #remove from keys once seen
    lst=[]
    while keys:
        size = 0
        root = keys[0]
        parseMe = [root]
        dctSeen = { root: ''}
        while parseMe:
            item = parseMe.pop()
            keys.remove(item)
            size+=1
            for nbr in graph[item]:
                if nbr not in dctSeen:
                    parseMe.append(nbr)
                    dctSeen[nbr]=item
        fixListLength(lst, size)
        lst[size-1]+=1
    return lst

def Kx(graph, x):
    keys = list(graph.keys())
    count = 0
    while keys:
        size = 0
        root = keys[0]
        parseMe = [root]
        dctSeen = { root: ''}
        while parseMe:
            item = parseMe.pop()
            keys.remove(item)
            size+=1
            for nbr in graph[item]:
                if nbr not in dctSeen:
                    parseMe.append(nbr)
                    dctSeen[nbr]=item
        if size == x:
            key = list(dctSeen.keys())
            check = True
            for i in range(len(key)):
                for t in key[i+1:]:
                    check = check and t in graph[key[i]]
            if check:
                count += 1
    return count

def parsePath(dct, goal):
    str = goal
    lst=[]
    while str != '':
        lst.insert(0, str)
        str= dct[str]
    return lst

def shortestPath(graph, root, goal):
    parseMe = [root]
    dctSeen = { root: ''}
    while parseMe:
        item = parseMe.pop(0)
        if item == goal:
            return parsePath(dctSeen,goal)
        for nbr in graph[item]:
            if nbr not in dctSeen:
                parseMe.append(nbr)
                dctSeen[nbr]=item
    return []

def overlap(lst, lst2):
    return sum(n not in lst2 for n in lst)==0

#returns word farthest from root
def farthestPath(graph, root):
    parseMe = [root]
    dctSeen = { root: ''}
    dctSize = { root: 1}
    while parseMe:
        item = parseMe.pop(0)
        for nbr in graph[item]:
            if nbr not in dctSeen:
                parseMe.append(nbr)
                dctSeen[nbr]=item
                dctSize[nbr] = dctSize[item]+1
    sizeMax = 0
    keyMax = root
    for i in dctSize:
        if dctSize[i] > sizeMax:
            sizeMax = dctSize[i]
            keyMax = i
    return keyMax

def swap(lst, index):
    #swap last letter and letter at index
    if index == len(lst[0])-1:
        return lst
    ret = []
    for word in lst:
        ret.append(word[:index] + word[-1] + word[index+1:-1]+word[index])
    return ret

def withinLetterIndex(str1, str2):
    return str1[:-1] == str2[:-1]

def makeConnection(graph, lst, index):
    lst = swap(lst, index)
    for i in range(len(lst)):
        graph[lst[i]] = graph[lst[i]] + lst[:i]+lst[i+1:]
    return len(lst)*(len(lst)-1)//2

#version 1 ~16 seconds
#graph = {}
# for idx, n in enumerate(myWords):
#     if graph.get(n) is None:
#         graph[n] = []
#     for x in myWords[idx+1:]:
#         if withinLetter(n,x):
#             if x not in graph[n]:
#                 graph[n].append(x)
#                 edge_count += 1
#             if graph.get(x) is None:
#                 graph[x] = [n]
#             elif n not in graph[x]: graph[x].append(n)


#make graph
graph = {}
for word in myWords:
    graph[word] = []

# set a temporary string to be the current value and store index
# iterate through until the current string and the current value are no longer one letter apart in the right place
# make connection for that sublist for index to current index
# set new temp

def constructGraph(graph, myWords):
    edge_count = 0
    myWords.sort()
    tempIndex = 0
    for i in range(len(myWords)):
        if withinLetterIndex(myWords[tempIndex], myWords[i]):
            continue
        if i-tempIndex > 1:
            edge_count += makeConnection(graph, myWords[tempIndex:i], len(myWords[0])-1)
        tempIndex = i

    for index in range(len(myWords[0])-2, -1, -1):
        lst = swap(myWords, index)
        lst.sort()
        tempIndex = 0
        for i in range(len(lst)):
            if withinLetterIndex(lst[tempIndex], lst[i]):
                continue
            if i - tempIndex > 1:
                edge_count+= makeConnection(graph, lst[tempIndex:i], index)
            tempIndex = i
    return edge_count

def threeSigFigs(num):
    if num < 1:
        count = 0
        while num < 1:
            num = num*10
            count+=1
        return (num*100//1)/ 10**(count+2)
    else:
        count = 0
        while num > 1000:
            num = num // 10
            count += 1
        return (num// 1) * 10**count

def listFormat(lst):
    return str(lst).replace(',', '').replace('[', '').replace(']', '').replace('\'', '')

def printPart1():
    print('Word Count: '+str(len(myWords)))
    print('Edge Count: '+str(constructGraph(graph, myWords)))
    print('Degree list: '+listFormat(degree_distribution(graph)))
    print('Construction Time: ' + str(threeSigFigs(time.time()-start_time)) + 's')

#Part 2
def printPart2():
    print('Second degree word: ' + second_degree(graph, len(degree_distribution(graph))-2))
    c = connected_components(graph)
    print('Connected component size count: ' + str(sum(n != 0 for n in c)))
    print('Largest component size: ' + str(len(c)))
    print('K2 count: ' + str(c[1]))
    print('K3 count: ' + str(Kx(graph, 3)))
    print('K4 count: ' + str(Kx(graph, 4)))
    print('Neighbors: ' + listFormat(neighbors(graph, args[1])))
    print('Farthest: ' + farthestPath(graph, args[1]))
    print('Path: '+listFormat(shortestPath(graph, args[1], args[2])))


printPart1()
myWords.sort()
if len(args) == 3:
   printPart2()