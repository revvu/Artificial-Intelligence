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

def incremental(total_node_count, avg_degree, node_lst):
    node_lst = []
    #start with close to avg_degree using int(avg_degree)+1 nodes
    sample = []
    starter_edges = int(avg_degree)
    for node_index in range(starter_edges+1):
        node_lst+=[starter_edges+1]
        sample+=[node_index]

    current_edge_count = starter_edges*(starter_edges+1)//2

    for node_index in range(starter_edges+1, total_node_count):

        edge_count = int((node_index+1)*avg_degree-2*current_edge_count)//2
        edge_count=min(edge_count,node_index)
        current_edge_count+=edge_count

        randlst = random.choices(sample, k=edge_count)

        for num in randlst:
            node_lst[num]+=1
            sample+=[num]
        node_lst+=[edge_count+1]
        sample+=[node_index]

    for node_index in range(len(node_lst)):
        node_lst[node_index]+=-1

    return node_lst

def nodes_to_degrees(node_lst):
    deg_dict = {}

    for index in range(len(node_lst)):
        if node_lst[index] not in deg_dict:
            deg_dict[node_lst[index]]=1
        else:
            deg_dict[node_lst[index]]+=1

    sum = 0
    for deg in deg_dict:
        sum+=deg*deg_dict[deg]

    print(sum)
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
    else: node_lst = incremental(node_count, avg_degree, node_lst)

    nodes_to_degrees(node_lst)
    print('Elapsed Time: ' + str(time.process_time() - start_time) + 's')

if __name__ == '__main__': main()