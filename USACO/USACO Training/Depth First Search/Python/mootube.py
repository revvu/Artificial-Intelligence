#USACO 2018 January MooTube
#Reevu Adakroy 1/9/2021

input_lines = open('mootube.in', 'r').readlines()
output_file = open('mootube.out', 'w')

N,Q = input_lines[0].split(' ')
N = int(N)
Q = int(Q)
K=0
adj = {}
for i in range(N):
    adj[i+1] = []

visited = [False]*5001
vids = 0
def dfs(node):
    visited[node]=True
    for nbr, r in adj[node]:
        if visited[nbr]: continue
        if r >= K:
            global vids
            vids+=1
            dfs(nbr)

for i in range(N-1):
    v1, v2, r = input_lines[i+1].split(' ')
    v1 = int(v1)
    v2 = int(v2)
    r = int(r)
    adj[v1]+=[(v2, r)]
    adj[v2] += [(v1, r)]

for i in range(Q):
    new_K, v = input_lines[N+i].split(' ')
    v = int(v)
    K = int(new_K)
    visited[v]=True
    dfs(v)
    output_file.write(str(vids)+'\n')
    visited = [False]*5001
    vids = 0
output_file.close()
