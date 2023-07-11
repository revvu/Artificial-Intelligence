import sys; args = sys.argv[1:]
# Reevu Adakroy

combo_boards = []

def flip_horizontal(board):
    #create a list of rows
    lst = []
    while board:
        lst+= [board[:8]]
        board = board[8:]
    #reverse the list
    lst = lst[::-1]
    big_lst = []
    for small_lst in lst:
        big_lst+=small_lst
    return big_lst

def rotate_90(board):
    new_board = []
    for i in range(8):
        j=56+i
        while j>=0:
            new_board+=[board[j]]
            j+=-8
    return new_board

def go_through_all_combos():
    #returns a set of all unique strings
    global combo_boards
    board = [i for i in range(64)]

    #rotate 0, 90, 180, 270
    for i in range(3):
        board=rotate_90(board)
        combo_boards += [board]
    board = rotate_90(board)
    #flip horizontal
    combo_boards+=[flip_horizontal(board)]
    #transpose = flip horizontal, rotate 90
    combo_boards+=[rotate_90(flip_horizontal(board))]
    #oppose transpose= rotate 90, flip horizontal
    board = flip_horizontal(rotate_90(board))
    combo_boards+=[board]
    #flip vertical = rotate 90, flip horizontal, rotate 270
    for i in range(3):
        board = rotate_90(board)
    combo_boards+=[board]
    for board in combo_boards:
        print(' '.join([str(i) for i in board]))

go_through_all_combos()
