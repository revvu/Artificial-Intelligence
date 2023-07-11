import sys; args = sys.argv[1:]
# Reevu Adakroy pd. 7
# started 4/4/2021
import time
import random

def classical(node_count, edge_count, node_lst):
    prefix_lst = [node_count-1]
    for i in range(2, node_count-1):
        prefix_lst.append(prefix_lst[-1]+node_count-i)

    randlst = random.sample(range((node_count*node_count-node_count)//2),edge_count)
    randlst.sort()
    index = 0
    for num in randlst:
        while num>prefix_lst[index]: index+=1
        node_lst[index]+=1
        node_lst[index+num-prefix_lst[index]+1]+=1

    return node_lst

def incremental(node_count, edge_count, node_lst):
    # assumes trivially greater than two nodes with one edge
    #also assumes

    for i in range(len(node_lst)):
        node_lst[i]+=1
    used_edges = set()
    used_edges.add((-1,-1))
    a,b=-1,-1
    for i in range(edge_count):
        while (a,b) in used_edges:
            a,b = sorted(random.choices(range(node_count),weights=node_lst,k=2))
        used_edges.add((a,b))
        node_lst[a]+=1
        node_lst[b]+=1

    for i in range(len(node_lst)):
        node_lst[i]+=-1

    return node_lst

def nodes_to_degrees(node_lst):
    deg_dict = {}

    for index in range(len(node_lst)):
        if node_lst[index] not in deg_dict:
            deg_dict[node_lst[index]]=1
        else:
            deg_dict[node_lst[index]]+=1

    print(deg_dict)

def main():
    if len(args)!=3:
        print('problem with input')
        exit()

    start_time = time.process_time()

    avg_degree = float(args[0])
    network_type = args[1][0].upper()
    node_count = int(args[2])

    edge_count = int(avg_degree*node_count/2)
    node_lst = [0]*node_count
    if network_type=='C': classical(node_count, edge_count, node_lst)
    else: incremental(node_count, edge_count, node_lst)

    nodes_to_degrees(node_lst)
    print('Elapsed Time: ' + str(time.process_time() - start_time) + 's')

if __name__ == '__main__': main()