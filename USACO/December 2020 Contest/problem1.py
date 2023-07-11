import sys
import math

lines = sys.stdin.readlines()
for i in range(len(lines)):
    lines[i] = lines[i][:-1]

cow_count = int(lines[0])
cow_graph = {}
for i in range(1, cow_count+1):
    cow_graph[str(i)]=[]

for pair in lines[1:]:
    cow1, cow2 = pair.split(' ')
    cow_graph[cow1].append(cow2)
    cow_graph[cow2].append(cow1)


dctSeen = set()
spot = '1'
days = 0
parseMe = ['1']

while parseMe:
    item = parseMe.pop()
    dctSeen.add(item)

    count_cows = 0
    for cow in cow_graph[item]:
        if cow not in dctSeen:
            count_cows+=1
    days+=count_cows + math.ceil(math.log2(count_cows+1))
    for nbr in cow_graph[item]:
        if nbr not in dctSeen:
            parseMe.append(nbr)

print(days)
