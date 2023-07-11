import sys
import math

lines = sys.stdin.readlines()
for i in range(len(lines)):
    lines[i] = lines[i][:-1]

cow_count = int(lines[0])
cow_graph = {}
for i in range(1, cow_count+1):
    cow_graph[i]=[]

cow_to_num = {}
num_to_cow = {}
cow_direction = {}

east_lst = []
north_lst = []
count = 1


for cow in lines[1:]:
    direction, x, y, = cow.split(' ')
    cow_to_num[(int(x), int(y))] = count
    num_to_cow[count] = (int(x), int(y))
    cow_direction[count] = direction
    count+=1
    if direction=='E':
        east_lst.append((int(x), int(y)))
    else: north_lst.append((int(x), int(y)))

north_lst.sort(key=lambda x: x[1])
east_lst.sort()

cow_stop = {}

keeplooking = True

for cow1 in east_lst:
    if keeplooking:
        for cow2 in north_lst:
            #find the first cow that stops it
            meet_point = (cow2[0], cow1[1])
            x_compare = meet_point[0]-cow1[0]
            y_compare = meet_point[1]-cow2[1]

            if x_compare < 0 or y_compare < 0:
                continue

            if y_compare < x_compare:
                cow_graph[cow_to_num[cow2]].append(cow1)
                cow_stop[cow_to_num[cow1]] = cow2
                keeplooking = False
                break
    keeplooking = True

for cow2 in north_lst:
    if keeplooking:
        for cow1 in east_lst:
            # find the first cow that stops it
            meet_point = (cow2[0], cow1[1])
            x_compare = meet_point[0] - cow1[0]
            y_compare = meet_point[1] - cow2[1]

            if x_compare < 0 or y_compare < 0:
                continue

            if y_compare > x_compare:
                cow_graph[cow_to_num[cow1]].append(cow2)
                cow_stop[cow_to_num[cow2]] = cow1
                keeplooking = False
                break
    keeplooking = True

cow_graph_copy = {}
for cow in cow_graph:
    cow_graph_copy[cow] = cow_graph[cow]

for num in cow_graph_copy:
    if cow_direction[num] == 'E':
        for cow in cow_graph[num]:
            if num not in cow_stop:
                print('you actually stupid bro')
                continue
            if cow[1] > cow_stop[num][1]:
                del cow
    else:
        for cow in cow_graph[num]:
            if num not in cow_stop:
                print('you actually stupid bro')
                continue
            if cow[0] > cow_stop[num][0]:
                del cow

print(cow_graph)
print(cow_to_num)
print(cow_stop)