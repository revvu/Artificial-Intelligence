import sys; args = sys.argv[1:]
# Reevu Adakroy, Tharun Saravanan pd. 7

width = 0

def parse_input():
    global width
    board = args[0]
    if len(args)==2:
        width = int(args[1])
    else:
        width = len(board)//find_height(board)
    return board

def find_height(board):
    n = int(len(board)**0.5+0.5)
    while len(board)%n:
        n+=-1
    return n

def flip_horizontal(board, width):
    #create a list of rows
    lst = []
    while board:
        lst+= [board[:width]]
        board = board[width:]
    #reverse the list
    lst = lst[::-1]
    #join the list and return
    return ''.join(lst)

def rotate_90(board, width):
    new_board = ""
    for i in range(width):
        j=len(board)-width+i
        while j>=0:
            new_board+=board[j]
            j+=-width
    return new_board

def go_through_all_combos(board):
    #returns a set of all unique strings
    combos = set()
    height = len(board)//width
    #rotate 0, 90, 180, 270
    for i in range(4):
        board=rotate_90(board, [width, height][i%2])
        # print("rotation: " + board)
        combos.add(board)

    #flip horizontal
    combos.add(flip_horizontal(board, width))
    # print("flip horizontal: " + flip_horizontal(board, width))

    #transpose = flip horizontal, rotate 90
    combos.add(rotate_90(flip_horizontal(board, width), width))
    # print("transpose: " + rotate_90(flip_horizontal(board, width), width))

    #oppose transpose= rotate 90, flip horizontal
    # print("input to oppose transpose: " + board)
    board = flip_horizontal(rotate_90(board, width), height)
    combos.add(board)

    # print("oppose transpose: " + board)
    #flip vertical = rotate 90, flip horizontal, rotate 270
    for i in range(3):
        board = rotate_90(board, [height, width][i%2])
    combos.add(board)
    # print("verital: " + board)
    return combos

lst = go_through_all_combos(parse_input())
for i in lst:
    print(i)
