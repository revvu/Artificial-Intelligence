import sys; args = sys.argv[1:]
# Reevu Adakroy pd. 7
# started 4/21/2021
import math
import random

alpha = 0.1
epochs_benchmark = 30000

def dot(lst1,lst2):
    if len(lst1)!=len(lst2): print('dot product problem bro')
    return sum(lst1[i]*lst2[i] for i in range(len(lst1)))

def activation_function(x_lst): return [1/(1+math.exp(-x)) for x in x_lst]

def query(inputs, weights):
    #hardcoded feedfordward
    layered_x = [inputs]
    first_hidden_y = [dot(inputs,weights[0][:(len(weights[0])+1)//2]), dot(inputs,weights[0][(len(weights[0])+1)//2:])]
    layered_x += [activation_function(first_hidden_y)]
    second_hidden_y = [dot(layered_x[-1],weights[1])]
    layered_x += [activation_function(second_hidden_y)]
    final_output = dot(layered_x[-1],weights[2])
    return final_output

def total_error(input_lst, target_outputs, weights):
    total = 0
    # print(input_lst)
    # print(target_outputs)
    # print(query(input_lst[0],weights))
    for index in range(len(input_lst)):
        total+= (target_outputs[index]-query(input_lst[index], weights))**2
    return total

def train_backprop(inputs, target, weights):
    #hardcoded feedfordward
    layered_x = [inputs]
    # first half of weights, then second half of weights
    first_hidden_y = [dot(inputs,weights[0][:(len(weights[0])+1)//2]), dot(inputs,weights[0][(len(weights[0])+1)//2:])]
    layered_x += [activation_function(first_hidden_y)]
    second_hidden_y = [dot(layered_x[-1],weights[1])]
    layered_x += [activation_function(second_hidden_y)]
    final_output = dot(layered_x[-1],weights[2])

    #error
    error = target-final_output
    #backprop final layer
    weights[2][0] += alpha*error*layered_x[-1][0]

    #backprop penultimate layer
    weights[1][0] += alpha*error*weights[2][0]*layered_x[-1][0]*(1-layered_x[-1][0])*layered_x[-2][0]
    weights[1][1] += alpha*error*weights[2][0]*layered_x[-1][0]*(1-layered_x[-1][0])*layered_x[-2][1]

    #backprop deepest layer
    for i in range((len(weights[0])+1)//2):
        weights[0][i]+= alpha*error*weights[2][0]*layered_x[-1][0]*(1-layered_x[-1][0])*weights[1][0]*layered_x[-2][0]*(1-layered_x[-2][0])*layered_x[-3][i]
    for i in range((len(weights[0])+1)//2):
        weights[0][i+((len(weights[0])+1)//2)]+= alpha*error*weights[2][0]*layered_x[-1][0]*(1-layered_x[-1][0])*weights[1][1]*layered_x[-2][1]*(1-layered_x[-2][1])*layered_x[-3][i]

def parse_input(input_text_lst):
    inputs = []
    targets = []

    for input_txt in input_text_lst:
        input_split = input_txt.split('=>')
        inputs += [[int(i) for i in input_split[0].strip().split(' ')]+[1]]
        targets += [int(input_split[1].strip())]
    return inputs, targets

def main():
    input_text_lst = open(args[0],'r').read().splitlines()
    input_lst,target_outputs = parse_input(input_text_lst)

    # print(input_lst)
    # print(target_outputs)

    #weights hardcoded for _ 2 1 1
    weights = []
    #first hidden layer
    weights += [[random.random() for i in range((len(input_lst[0]))*2)]]
    #second hidden layer
    weights += [[random.random(),random.random()]]
    #last hidden layer
    weights += [[random.random()]]

    # #first hidden layer
    # weights += [[0.25,0.5,0.5,0.75,0.5,0.25]]
    # #second hidden layer
    # weights += [[0.5,0.5]]
    # #last hidden layer
    # weights += [[0.5]]
    print('Layer counts: ' + str(len(input_lst[0])) + ' 2 1 1')
    for layer_weights in weights:
        print(' '.join([str(i) for i in layer_weights]))

    min_error = 0.05
    epoch_count = 0
    while True:
        for index in range(len(input_lst)):
            train_backprop(input_lst[index], target_outputs[index], weights)
        epoch_count+=1
        if epoch_count==epochs_benchmark and total_error(input_lst,target_outputs,weights)>0.1:
            weights = []
            # first hidden layer
            weights += [[random.random() for i in range((len(input_lst[0])) * 2)]]
            # second hidden layer
            weights += [[random.random(), random.random()]]
            # last hidden layer
            weights += [[random.random()]]
            epoch_count = 0
    #     #elif epoch_count==epochs_benchmark: break
        if p:=total_error(input_lst,target_outputs,weights)<min_error:
            min_error = p
            print('Layer counts: ' + str(len(input_lst[0])) + ' 2 1 1')
            # print(input_lst)
            # print(target_outputs)
            for layer_weights in weights:
                print(' '.join([str(i) for i in layer_weights]))

    # weights = [[1.6202927083949337, 2.181797604404205, -3.0339189405245177, 1.25403798269567, 0.6857182825776896, -1.1509684262680107], [2.629313480063969, -0.017434957141041454], [0.4655467693958602]]
    # print(total_error(input_lst, target_outputs, weights))

    # print('Layer counts: ' + str(len(input_lst[0]))+ ' 2 1 1')
    # for layer_weights in weights:
    #     print(' '.join([str(i) for i in layer_weights]))
    # print(total_error(input_lst,target_outputs,weights))

if __name__ == '__main__': main()