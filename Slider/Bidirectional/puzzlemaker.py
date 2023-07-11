import random
import sys

sys.stdout = open('puzzles.txt', 'w')
PUZZLES = 500
str = '12345678_'
#str = 'ABCDEFGHIJKLMNO_'
lst = [*str]
for i in range(PUZZLES):
    random.shuffle(lst)
    print(''.join(lst))

