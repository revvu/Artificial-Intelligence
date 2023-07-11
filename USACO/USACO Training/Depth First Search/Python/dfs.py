#Reevu Adakroy 1/8/2021
#simple dfs

N = 10**10
visited = [False] * N
adj = [0]*N
def dfs(node):
    if visited[node]: return
    visited[node] = True
    #process node
    for nbr in adj[node]:
        dfs(nbr)

