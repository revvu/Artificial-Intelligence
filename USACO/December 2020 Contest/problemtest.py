myWords = open('input.txt', 'r').read().splitlines()
f = open('output.txt', 'w')
f.write(myWords[2])
f.close()