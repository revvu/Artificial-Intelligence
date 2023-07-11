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

points_graph = {}
for point in points_lst:
    points_graph[point] = []

for point in points_lst:
    for point2 in points_lst:
        if point[0] >= point2[0] and point[1] >= point2[1]:
            points_graph[point].append(point2)

total = 0
for point in points_graph:
    if len(points_graph[point]) >= 3:
        total+= math.pow(2, len(points_graph[point])-2) + 1

total = math.pow(2, point_count) - total
print(int(total))