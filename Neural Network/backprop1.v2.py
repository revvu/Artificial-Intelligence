import sys; args = sys.argv[1:]
# Reevu Adakroy pd. 7
# started 4/21/2021
import math
import random

alpha = 0.1
input_node_count = 100000
first_hidden_layer = 2
epochs_benchmark = 30000

def dot(lst1,lst2): return sum(lst1[i]*lst2[i] for i in range(len(lst1)))

def activation_function(x_lst): return [1/(1+math.exp(-x)) for x in x_lst]

def distance(x,y): return x*x+y*y

def query(inputs, weights):
    node_lst = inputs[::]
    #no activation on the last layer
    for layer in weights[:-1]:
        n = len(node_lst)
        node_lst = activation_function([dot(node_lst, layer[x:x+n]) for x in range(0, len(layer), n)])
    #assumes single output
    return weights[-1][0]*node_lst[0]

def generate_input(count):
    inputs = []
    t_o = []
    for i in range(count):
        x,y = random.uniform(-1.5,1.5), random.uniform(-1.5,1.5)
        inputs+=[[x,y,1]]
        t_o +=[int(distance(x,y)<=radius)]
    return inputs,t_o

# 3 guaranteed in input layer
def initialize_weights():
    return [[random.random() for i in range(3*first_hidden_layer)],[random.random() for i in range(first_hidden_layer)],[random.random()]]

def total_error(inputs, t_o, weights): return sum((t_o[i]-query(inputs[i], weights))**2 for i in range(len(t_o)))

def train_backprop(inputs, target, weights):
    layered_x = [inputs[::]]
    # no activation on the last layer
    for layer in weights[:-1]:
        n = len(layered_x[-1])
        layered_x += [activation_function([dot(layered_x[-1], layer[x:x + n]) for x in range(0, len(layer), n)])]
    # assumes single output
    final_output = weights[-1][0]*layered_x[-1][0]

    #error
    error = target-final_output
    #backprop final layer
    weights[2][0] += alpha*error*layered_x[-1][0]
    #backprop penultimate layer
    for i in range(first_hidden_layer):
        weights[1][i] += alpha*error*weights[2][0]*layered_x[-1][0]*(1-layered_x[-1][0])*layered_x[-2][i]
    #backprop deepest layer
    for j in range(first_hidden_layer):
        for i in range(3):
            weights[0][i+j*3]+=alpha*error*weights[2][0]*layered_x[-1][0]*(1-layered_x[-1][0])*weights[1][j]*layered_x[-2][j]*(1-layered_x[-2][j])*layered_x[-3][i]

def parse_input(input_text_lst):
    inputs = []
    targets = []

    for input_txt in input_text_lst:
        input_split = input_txt.split('=>')
        inputs += [[int(i) for i in input_split[0].strip().split(' ')]+[1]]
        targets += [int(input_split[1].strip())]
    return inputs, targets

def main():
    input_text_lst = open(args[0], 'r').read().splitlines()
    input_lst, target_outputs = parse_input(input_text_lst)
    weights = initialize_weights()

    # print('Layer counts: 3 ' + str(first_hidden_layer)+ ' 1 1')
    # for layer_weights in weights:
    #     print(' '.join([str(i) for i in layer_weights]))

    print('Layer counts: ' + str(len(input_lst[0])) + ' 2 1 1')
    for layer_weights in weights:
        print(' '.join([str(i) for i in layer_weights]))
    print(total_error(input_lst, target_outputs, weights))
    min_error = 0.05
    epoch_count = 0
    while True:
        for index in range(len(input_lst)):
            train_backprop(input_lst[index], target_outputs[index], weights)
        epoch_count += 1
        if epoch_count == epochs_benchmark and total_error(input_lst, target_outputs, weights) > 0.1:
            weights = initialize_weights()
            epoch_count = 0
        #     #elif epoch_count==epochs_benchmark: break
        if p := total_error(input_lst, target_outputs, weights) < min_error:
            min_error = p
            print('Layer counts: ' + str(len(input_lst[0])) + ' 2 1 1')
            # print(input_lst)
            # print(target_outputs)
            for layer_weights in weights:
                print(' '.join([str(i) for i in layer_weights]))

    # while True:
    #     for index in range(len(input_lst)):
    #         train_backprop(input_lst[index], t_o[index], weights)
    #     if p:=total_error(input_lst,t_o,weights)<min_error:
    #         min_error = p
    #         print('Layer counts: ' + str(len(input_lst[0])) + ' 2 1 1')
    #         for layer_weights in weights:
    #             print(' '.join([str(i) for i in layer_weights]))

if __name__ == '__main__': main()