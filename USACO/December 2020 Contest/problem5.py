import sys
import math

lines = sys.stdin.readlines()
for i in range(len(lines)):
    lines[i] = lines[i][:-1]

point_count = int(lines[0])
points_lst = []
for point in lines[1:]:
    x,y = point.split(' ')
    points_lst.append((int(x), int(y)))

x_dict = {}
y_dict = {}
for point in points_lst:
    if x_dict[point[0]] is None:
        x_dict[point[0]] = []
    if y_dict[point[1]] is None:
        y_dict[point[1]] = []
    x_dict[point[0]] = point
    y_dict[point[1]] = point




x_lst = []
y_lst = []

for point in points_lst:
    x_lst.append(point)
    y_lst.append(point)

x_lst.sort()
y_lst.sort(key=lambda i:i[1])

x_min = x_lst[0][0]
x_max = x_lst[-1][0]

y_min = y_lst[0][1]
y_max = y_lst[-1][1]

total = math.pow(2, point_count)


points_graph = {}
for point in points_lst:
    points_graph[point] = []


total = 0
for point in points_graph:
    if len(points_graph[point]) >= 3:
        total+= math.pow(2, len(points_graph[point])-2) + 1

total = math.pow(2, point_count) - total
print(int(total))