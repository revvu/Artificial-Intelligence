import sys; args = sys.argv[1:]
# Reevu Adakroy pd. 7
# started 5/31/2021
import math
import random
import time

alpha = 0.1
input_node_count = 1500000
first_hidden_layer = 20 #20 was good
epochs = 1

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
    if '=' in args[0]: radius = float(args[0].split('=')[1])
    elif '>' in args[0]: radius = float(args[0].split('>')[1])
    else: radius = float(args[0].split('<')[1])
    inputs = []
    t_o = []
    for i in range(count):
        x,y = random.uniform(-1.5,1.5), random.uniform(-1.5,1.5)
        inputs+=[[x,y,1]]
        t_o +=[int(distance(x,y)<=radius)]
    return inputs,t_o

# 3 guaranteed in input layer
def initialize_weights():
    #weights determined by extended run on radius = 1
    if '=' in args[0]: radius = float(args[0].split('=')[1])
    elif '>' in args[0]: radius = float(args[0].split('>')[1])
    else:radius = float(args[0].split('<')[1])
    scalar_weight = (radius**0.5)
    #inverted_sig = math.log(scalar_weight/(1-scalar_weight))
    #can invert graph around circle based on > <
    # return [[scalar_weight,0,0,0,scalar_weight,0,0,0,1],[3.180707114261468, -12.361129701362556, 10.54952605351938, 0.38993428967093946, 12.764642170911124,
    #   10.734097573129961, -0.2373263480293963, -0.014445791649172935, 5.3639055271450164, 8.146807686562967,
    #   0.95566757442353, -6.954237864962222, -0.23777328127194147, -0.014071747407718342, 5.291899834284723,
    #   10.584489174863718, 1.0640325417536958, -5.1058681927160325, 10.256104656694188, -1.6871447684535206,
    #   9.232750656190818, -0.23791322609681437, -0.012717629742454942, 5.022068519819604, 5.15292961047265,
    #   11.720505635174536, -10.866855227597036, -0.2376949248274653, -0.01404594935773984, 5.280417156279643,
    #   -0.23804165997234528, -0.013315983255340036, 5.13997737042248, 17.371150695761035, 1.340162220581748,
    #   -16.298712687254582, 12.397993326865588, 1.9738312728266607, 9.63302342764085, 5.371746199577546,
    #   0.40918207464306816, -3.5136688434729324, 9.497474838884571, -6.036900233021706, 8.117326492277346,
    #   -0.23762745393767357, -0.01413097712534326, 5.297698614857837, 6.81844798869907, -10.887918729760976,
    #   -10.725750253533354, 7.739809707798509, 11.158408939423387, 11.822015413203728, 8.571988439840041,
    #   -9.388869875001816, 11.214659545873054, 8.20443988500979, 6.648540264530319, 8.258946987946688],
    #  [23.72781618485041, 23.03380743383276, -16.9989611024171, -10.340360840132405, -16.26944728653813,
    #   -15.58770723359628, 12.579911461182745, -13.61142250550365, -29.6557125149389, -16.106239887318566,
    #   -14.727960312633801, -22.977460615429415, 17.826033182172548, -5.229456240402667, 13.621591564914135,
    #   -16.28605643953751, -29.99076945730261, 18.231385996266717, 14.629713964528298, 15.03170255293104],
    #  [1.0058556819471776]]
    return [#[inverted_sig,0,0,0,inverted_sig,0,0,0,1],
            [1.6891173998311007/scalar_weight, -16.312877683665814/scalar_weight, 13.964202215398771, -0.09135916348756999/scalar_weight, 16.556571468502074/scalar_weight,
      14.155430105482456, -0.23167920994602642/scalar_weight, -0.0027310107540579115/scalar_weight, 5.971300730960183, 12.041160116439626/scalar_weight,
      0.6702019406530748/scalar_weight, -10.866889284156976, -0.23050539263235995/scalar_weight, -0.0028553934741355584/scalar_weight, 5.920992306378716,
      13.26249309872333/scalar_weight, 0.7511121542990674/scalar_weight, -6.9731513695200675, 15.859433222907933/scalar_weight, -3.401608534442879/scalar_weight,
      13.219528722231464, -0.22607764794550536/scalar_weight, -0.003308826997470765/scalar_weight, 5.73219664816043, 7.11327513942418/scalar_weight,
      13.929213170318274/scalar_weight, -13.103632047671788, -0.23035710540496268/scalar_weight, -0.002868987388458954/scalar_weight, 5.9116811403383105,
      -0.22803494183293374/scalar_weight, -0.0031095018229803217/scalar_weight, 5.813950022494064, 23.27332980705493/scalar_weight, 1.4050196050032695/scalar_weight,
      -21.567049319767246, 14.530257590493978/scalar_weight, 4.974270247552081/scalar_weight, 12.590595635243554, 7.97559239788746/scalar_weight,
      0.3497409737444594/scalar_weight, -5.154682461362649, 10.146912523289606/scalar_weight, -8.18328866561296/scalar_weight, 10.391940014068396,
      -0.23063483066089385/scalar_weight, -0.0028400625844489592/scalar_weight, 5.923922975506661, 8.689338882722927/scalar_weight, -12.97723908337739/scalar_weight,
      -13.018128097157769, 8.945568108630654/scalar_weight, 14.908330169085403/scalar_weight, 15.07972216003748, 10.673591998041369/scalar_weight,
      -14.071575303273004/scalar_weight, 15.229596889894077, 8.824790145190255/scalar_weight, 8.894861812255574/scalar_weight, 9.950505361703662],
     [27.226076672830935, 27.089030126359706, -22.792545186338604, -13.266390184178812, -22.061074578810818,
      -17.49517692678643, 25.030088824222112, -19.39447354204361, -39.5449002563529, -21.897543398809646,
      -20.51501595542412, -27.83715317218425, 25.49481145025655, -8.051673329214948, 19.142813235828914,
      -22.077846379575167, -39.5932268502189, 22.925884644977693, 21.87130554664238, 18.343348467839647],
     [1.0020291934357413]]
    #return [[random.random() for i in range(3*first_hidden_layer)],[random.random() for i in range(first_hidden_layer)],[random.random()]]

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
    for i in range(len(weights[1])):
        weights[1][i] += alpha*error*weights[2][0]*layered_x[-1][0]*(1-layered_x[-1][0])*layered_x[-2][i]
    #backprop deepest layer
    for j in range(first_hidden_layer):
        for i in range(3):
            weights[0][i+j*3]+=alpha*error*weights[2][0]*layered_x[-1][0]*(1-layered_x[-1][0])*weights[1][j]*layered_x[-2][j]*(1-layered_x[-2][j])*layered_x[-3][i]

def goof_count(weights):
    test_input_lst, test_t_o = generate_input(100000)
    goofs = 0
    for index in range(len(test_input_lst)):
        if round(query(test_input_lst[index],weights))!=test_t_o[index]: goofs+=1
    return goofs

def print_weights(weights):
    print('Layer counts: 3 ' + str(first_hidden_layer)+ ' 1 1')
    for layer_weights in weights:
        print(' '.join([str(i) for i in layer_weights]))


def main():
    weights = initialize_weights()

    print_weights(weights)

    # input_lst, t_o = generate_input(1000000)
    # for index in range(len(input_lst)):
    #     train_backprop(input_lst[index], t_o[index], weights)
    #
    # while True:
    #     input_lst, t_o = generate_input(100000)
    #     for index in range(len(input_lst)):
    #         train_backprop(input_lst[index], t_o[index], weights)
    #     print(g:=goof_count(weights))
    #     if g < 150: print(weights)

    print(goof_count(weights))
    # print(query([0,0.2,1],weights))

if __name__ == '__main__': main()