import sys; args = sys.argv[1:]
# Reevu Adakroy pd. 7
# started 4/4/2021

import random

def classical(node_count, edge_count, node_lst):
    prefix_lst = [node_count-1]
    for i in range(2, node_count-1):
        prefix_lst.append(prefix_lst[-1]+node_count-i)
    # print(prefix_lst[0:10])
    # pairing_lst = []
    # for i in range(node_count):
    #     for j in range(i):
    #         pairing_lst+=[(i,j)]

    # randlst = set()
    # while len(randlst)<edge_count:
    #     randlst.add(random.randint(0,(node_count*node_count-node_count)//2))
    # randlst = [*range((node_count*node_count-node_count)//2)]
    randlst = random.sample(range((node_count*node_count-node_count)//2),edge_count)


    for num in randlst:
        #find first index this is greater than
        #change to binary search if needed
        index = 0
        # print('num: ' + str(num))
        # print('prefix: ' + str(prefix_lst[index]))
        while num>prefix_lst[index]: index+=1
        node_lst[index]+=1
        # print('index: ' + str(index))
        # print(index+num-prefix_lst[index]+1)
        node_lst[index+num-prefix_lst[index]+1]+=1

        # node1,node2 = pairing_lst[num]
        # node_lst[node1]+=1
        # node_lst[node2]+=1

    return node_lst

def incremental():
    return

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
    avg_degree = float(args[0])
    network_type = args[1][0].upper()
    node_count = int(args[2])

    edge_count = int(avg_degree*node_count/2)

    node_lst = [0]*node_count

    if network_type=='C':
        classical(node_count, edge_count, node_lst)
    else:
        return incremental()

    nodes_to_degrees(node_lst)

if __name__ == '__main__': main()