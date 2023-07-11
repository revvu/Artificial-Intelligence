#USACO 2019 US Open Fence Planning
#Reevu Adakroy 1/9/2021

input_lines = open('fenceplan.in', 'r').readlines()
output_file = open('fenceplan.out', 'w')

N,M = input_lines[0].split(' ')
N = int(N)
M = int(M)

IDcow = {}
adj = {}
for i in range(N):
    adj[i] = []

visited =[False]*N

def dfs(node, comp):
    if visited[node]: return
    visited[node] = True
    comp+=[IDcow[node]]
    for nbr in adj[node]:
        dfs(nbr, comp)

for i in range(N):
    x,y = input_lines[i+1].split(' ')
    x = int(x)
    y = int(y)
    IDcow[i] = (x,y)

for i in range(M):
    a, b = input_lines[N+1+i].split(' ')
    a = int(a)
    b = int(b)
    adj[a-1] += [b-1]
    adj[b-1] += [a-1]

perimeters = []
for i in range(N):
    if visited[i]: continue
    comp = []
    dfs(i, comp)

    minx = comp[0][0]
    maxx = comp[0][0]
    miny = comp[0][1]
    maxy = comp[0][1]

    for cow in comp:
        x,y = cow
        minx = min(x, minx)
        maxx = max(x, maxx)
        miny = min(y, miny)
        maxy = max(y, maxy)

    perimeters+=[2*(maxx-minx+maxy-miny)]

output_file.write(str(min(perimeters)))
print(N)
print(M)
print(IDcow)
print(adj)
