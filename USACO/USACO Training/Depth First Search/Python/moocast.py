#USACO 2016 December Moocasy
#Reevu Adakroy
#14 min 55 sec

#for each cow, do a dfs
input_lines = open('moocast.in', 'r').readlines()
output_file = open('moocast.out', 'w')

N = int(input_lines[0])

visited = [False]*N
adj = {}
cowID = {}

for i in range(N):
    adj[i]=[]

def dfs(node):
    if visited[node]: return
    visited[node]=True
    for nbr in adj[node]:
        dfs(nbr)

def distance(x1, y1, x2, y2):
    return ((x2-x1)**2+(y1-y2)**2)**0.5

for line in range(N):
    x,y,p = input_lines[line+1].split(' ')
    x = int(x)
    y = int(y)
    p = int(p)
    cowID[(x,y,p)]=line

for x,y,p in cowID:
    for x2,y2,p2 in cowID:
        if x==x2 and y==y2 and p==p2: continue
        if distance(x,y,x2,y2)<=p:
            adj[cowID[(x,y,p)]]+=[cowID[(x2,y2,p2)]]

max_reach = 0
for cow in adj:
    dfs(cow)
    max_reach = max(visited.count(True), max_reach)
    visited = [False]*N

output_file.write(str(max_reach))