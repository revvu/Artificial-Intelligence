import sys; args = sys.argv[1:]
# Reevu Adakroy pd. 7
# started 5/31/2021
import math
import re

def parse_input():
    if '=' in args[1]: radius = float(args[1].split('=')[1])
    elif '>' in args[1]: radius = float(args[1].split('>')[1])
    else: radius = float(args[1].split('<')[1])

    weights_lines = open(args[0], 'r').read().splitlines()
    weights = []
    for line in weights_lines:
        extract_floats = [float(i) for i in re.findall(r'-?\d*\.\d+|\d+',line)]
        if extract_floats: weights+=[extract_floats]
    return weights, radius

def find_node_count(weights, start):
    # find node counts
    n = [start]
    for i in range(len(weights)):
        n += [len(weights[i]) // n[-1]]
    return n

def replicate_network(weights,radius):
    #find node counts
    n = find_node_count(weights,2)
    new_weights = []

    #2 --> 3, special case
    w0=[]
    for i in range(0,len(weights[0]),2):
        w0+=[weights[0][i]/(radius**0.5),0,weights[0][i+1]]
    for i in range(0,len(weights[0]),2):
        w0+=[0,weights[0][i]/(radius**0.5),weights[0][i+1]]
    new_weights+=[w0]

    for i in range(1,len(n)-2):
        nc = n[i]
        zeros = [0]*nc
        w_1,w_2 =[],[]
        for x in range(0, len(weights[i]), nc):
            w_1+=weights[i][x:x+nc]+zeros
            w_2+=zeros+weights[i][x:x+nc]
        new_weights+=[w_1+w_2]
    new_weights+=[weights[-1]*2]

#    new_weights+=[[(1+math.exp(-1*radius))/2]]
    if '>' in args[1]: new_weights += [[(1 + math.exp(-1 * 1)) / 2]]
    else:
        new_weights[-1]=[-1*weight for weight in new_weights[-1]]
        new_weights += [[1.85914]]
    return new_weights

def print_weights(weights):
    print('Layer counts: ' + str(find_node_count(weights,3))[1:-1])
    for layer_weights in weights:
        print(' '.join([str(i) for i in layer_weights]))

def main():
    weights,radius = parse_input()
    print_weights(replicate_network(weights,radius))

if __name__ == '__main__': main()