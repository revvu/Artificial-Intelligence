import sys; args = sys.argv[1:]
# Reevu Adakroy pd. 7
# started 4/21/2021
import math

weights = open(args[0], 'r').read().splitlines()
function_int = int(args[1][1])

def T(x):
    if function_int==1: return x
    if function_int==2:
        if x>=0: return x
        else: return 0
    if function_int==3:
        return 1/(1+math.exp(-x))
    if function_int==4:
        return 2/(1+math.exp(-x))-1

def dot_product(lst1,lst2):
    return sum(lst1[i]*lst2[i] for i in range(len(lst1)))

def update(node_lst, weight_lst):
    new_node_lst = []

    while weight_lst:
        new_node_lst+=[dot_product(weight_lst[-len(node_lst):], node_lst)]
        weight_lst = weight_lst[:-len(node_lst)]
        #if weight_lst: node_lst = [T(x) for x in node_lst]
    return new_node_lst[::-1]

node_lst = [float(i) for i in args[2:]]
weight_lst = [float(i) for i in weights[0].split(' ')]
node_lst = update(node_lst, weight_lst)

for line in weights[1:-1]:
    node_lst = [T(x) for x in node_lst]
    weight_lst = [float(i) for i in line.split(' ')]
    node_lst = update(node_lst, weight_lst)

if len(weights)>1:
    node_lst = [T(x) for x in node_lst]
    weight_lst = [float(i) for i in weights[-1].split(' ')]
    node_lst = [node_lst[i]*weight_lst[i] for i in range(len(node_lst))]

print(weights)
print(str(node_lst)[1:-1])