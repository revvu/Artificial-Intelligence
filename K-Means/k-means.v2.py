import sys; args = sys.argv[1:]
# Reevu Adakroy pd. 7
# started 5/4/2021
from PIL import Image
import random

def parse_input():
    if len(args)!=2:
        print('please provide two inputs, first the value of k followed by the name of the image file')
        exit(0)

    k = int(args[0])
    img = Image.open(args[1])
    width,height = img.size
    print('Size: ' + str(height) + ' x ' + str(width))
    print('Pixels: ' + str(height * width))

    pix = img.load()
    color_dict = {}
    for row in range(width):
        for col in range(height):
            if pix[row,col] in color_dict: color_dict[pix[row,col]]+=1
            else: color_dict[pix[row,col]]=1

    print('Distinct pixel count: ' + str(len(color_dict)))
    color_map = []
    max_color_count = 0
    max_color = (0,0,0)

    for color in color_dict:
        if color_dict[color]>max_color_count:
            max_color_count = color_dict[color]
            max_color = color
        color_map+=[(color,color_dict[color])]

    print('Most common pixel: ' + str(max_color))
    # k_lst = random.sample(list(color_dict), k)
    k_lst = []
    #instead of random, lets go for kinda spread out
    color_choices = sorted(list(color_dict))
    increment = len(color_dict)//k
    index = 0
    for i in range(k):
        print(color_choices[index])
        k_lst.append(color_choices[index])
        index += increment
    print(k_lst)
    return color_map,k_lst

def distance(p1,p2):
    return sum((p1[i]-p2[i])**2 for i in range(len(p1)))

def find_mean(color_lst):
    return tuple([sum(color[i]*count for color,count in color_lst)/len(color_lst) for i in range(3)])

def find_closest_center(color, k_lst):
    distance_lst = [(distance(color, color_center),color_center) for color_center in k_lst]
    return min(distance_lst)[1]

def k_mean_increment(k_lst, color_map):
    center_dict = {}
    for center in k_lst:
        center_dict[center] = []
    print("initial center dict length: " + str(len(center_dict)))
    if len(k_lst)!=len(center_dict):
        print("ASL;KFJAWE WHAT IS HAPPENING")
        #same center twice
    #find closest centers
    for color,count in color_map:
        center_dict[find_closest_center(color,k_lst)]+=[(color,count)]

    #set new centroids
    new_k_lst = [find_mean(center_dict[center]) if len(center_dict[center]) else center for center in center_dict]
    if len(new_k_lst)!=len(k_lst):
        print("MAJOR PROBLEM")
        print(len(k_lst))
        print(len(new_k_lst))
        print("final center dict length: " + str(len(center_dict)))

    #find delta
    change_lst = [distance(new_k_lst[i],k_lst[i]) for i in range(len(k_lst))]
    return change_lst,new_k_lst


def floodfill_recur():
    return

def floodfill():
    return

def main():
    color_map, k_lst = parse_input()
    print('color map [0]: ' + str(color_map[0]))

    # pix = img.load()
    # for i in range(100):
    #     pix[i,i] = (255,127,0)

    #start with naive color selection

    # img.save("kmeans/{}.png".format('2021radakroy'), "PNG")

    print('Final means: ')
    change_lst, k_lst = k_mean_increment(k_lst,color_map)
    while change_lst.count(0)<len(change_lst): change_lst, k_lst = k_mean_increment(k_lst,color_map)
    print(k_lst)
    # for i in k_lst:
    #     print(str(i + 1) + ': (,,) => ')
    print('Region counts: #,#,#,#,#')


if __name__ == '__main__': main()