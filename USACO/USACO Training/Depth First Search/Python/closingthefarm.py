#USACO 2016 US Open Silver
#Reevu Adakroy 1/8/2021
#time: 28 min 41 sec

input_lines = open('closing.in', 'r').readlines()
output_file = open('closing.out', 'w')

N, M = input_lines[0].split(' ')
N = int(N)
M = int(M)

visited = [False]*N
adj = {}
for i in range(N):
    adj[i+1] = []

def dfs(node):
    if visited[node-1]: return
    visited[node-1] = True
    for nbr in adj[node]:
        dfs(nbr)

for _ in range(M):
    farm1, farm2 = input_lines[_+1].split(' ')
    farm1 = int(farm1)
    farm2 = int(farm2)
    adj[farm1]+=[farm2]
    adj[farm2]+=[farm1]

for _ in range(N):
    farm = int(input_lines[M+1+_])
    visited = [False]*N
    dfs(farm)
    ret_string = 'YES\n'
    for node in adj:
        if not visited[node-1]:
            ret_string = 'NO\n'
            break
    output_file.write(ret_string)
    #get rid of the thing
    for node in adj[farm]:
        adj[node].remove(farm)
    del adj[farm]