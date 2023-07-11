import sys; args = sys.argv[1:]
# Reevu Adakroy pd. 7
# started 5/4/2021
from PIL import Image
import random
import time


image_stats = {}
img = Image.Image()
my_k, width,height = 0,0,0

di = [-1,-1,-1,0,0,1,1,1]
dj = [-1,0,1,-1,1,-1,0,1]

def stream(pix):
    vis = [[-1]*width for i in range(height)]
    label=0
    regions_lst = []
    for row in range(height):
        for col in range(width):
            set_color = pix[col,row]
            if f:=flood(pix,row,col,vis,set_color,label): regions_lst+=[f]
            label+=1
    print('Region counts: ' + str(regions_lst)[1:-1])

def flood(pix,start_row,start_col,vis,set_color,label):
    paint={(start_row,start_col)}
    count=0
    while paint:
        rw,cl=paint.pop()
        if not 0<=rw<height or not 0<=cl<width or vis[rw][cl]!=-1 or pix[cl,rw]!=set_color: continue
        vis[rw][cl]=label
        count+=1
        for i in range(len(di)): paint.add((rw+di[i],cl+dj[i]))
    return count

def parse_input():
    global my_k,width,height,img
    my_k,img = int(args[0]), Image.open(args[1])
    width,height=img.width,img.height
    #size
    image_stats['Size'] = str(width)+' x '+str(height)
    #pixel count
    image_stats['Pixels'] = str(height*width)

def create_color_dict(pix):
    color_dict = {}
    for row in range(width):
        for col in range(height):
            if pix[row,col] in color_dict: color_dict[pix[row, col]] += 1
            else: color_dict[pix[row,col]]=1
    # unique color count
    image_stats['Distinct pixel count'] = str(len(color_dict))

    max_color = tuple([0]*len(list(color_dict)[0]))
    max_color_count = 0
    for color in color_dict:
        if color_dict[color]>max_color_count:
            max_color=color
            max_color_count=color_dict[color]
    image_stats['Most common pixel'] = str(max_color)+' => '+str(max_color_count)

    return color_dict

def distance(p1,p2):
    return sum((p1[i]-p2[i])**2 for i in range(len(p1)))

def find_mean(color_lst,color_dict):
    total_color = [0]*len(color_lst[0])
    total_multiplier = 0
    for color in color_lst:
        total_multiplier+=color_dict[color]

    for color in color_lst:
        for i in range(len(color)):
            total_color[i]+=color[i]/total_multiplier*color_dict[color]
    return tuple(total_color)

def find_closest_centers(color_dict, k_lst):
    bucketed_colors = []
    for i in range(len(k_lst)):
        bucketed_colors.append([])

    for color in color_dict:
        min_distance = len(color)*256**2
        min_index = -1
        for i in range(len(k_lst)):
            if distance(k_lst[i],color)<min_distance:
                min_index = i
                min_distance=distance(k_lst[i],color)
        bucketed_colors[min_index].append(color)
    return bucketed_colors

def bucket_averages(bucketed_colors,color_dict):
    k_lst = []
    for bucket in bucketed_colors:
        k_lst.append(find_mean(bucket,color_dict))
    return k_lst

def initialize_ks(color_set):
    k_lst = [color_set.pop()]
    for x in range(my_k-1):
        cum_weights = [0]
        for color in color_set:
            min_distance = len(color)*256**2
            for i in range(len(k_lst)):
                if distance(k_lst[i], color) < min_distance:
                    min_distance = distance(k_lst[i], color)
            cum_weights+=[cum_weights[-1]+min_distance*min_distance]
        val = random.choices(list(color_set),cum_weights=cum_weights[1:],k=1)
        k_lst+=[val[0]]
        color_set.remove(val[0])
    return k_lst

def main():
    parse_input()
    pix = img.load()
    color_dict = create_color_dict(pix)

    for stat in image_stats:
        print(stat +': ' + image_stats[stat])

    start_time = time.process_time()

    old_k_lst = []
    k_lst = initialize_ks(set(color_dict))
    # print(k_lst)
    bucketed_colors = find_closest_centers(color_dict,k_lst)
    while old_k_lst!=k_lst:
        old_k_lst=k_lst
        bucketed_colors = find_closest_centers(color_dict,k_lst)
        k_lst=bucket_averages(bucketed_colors,color_dict)

    print(str(time.process_time() - start_time) + 's')

    print('Final means:')

    for i in range(len(k_lst)):
        print(str(i+1)+': '+str(k_lst[i])+' => '+str(len(bucketed_colors[i])))

    reverse_color_dict = {}
    for index in range(len(bucketed_colors)):
        for color in bucketed_colors[index]:
            reverse_color_dict[color]=tuple([int(k_lst[index][i]) for i in range(len(color))])

    for row in range(width):
        for col in range(height):
            pix[row,col]=reverse_color_dict[pix[row,col]]
    img.save('kmeans/{}.png'.format('2021radakroy'), 'PNG')
    stream(pix)

if __name__ == '__main__': main()