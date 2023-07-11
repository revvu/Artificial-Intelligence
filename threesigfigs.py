import math

def tsf(num):
    if num == 0:
        return 0.0
    if num > 1:
        ret = str(num) + '.'
        return round(num, 3 - ret.index('.'))
    count = 0
    while num < 1:
        count += 1
        num = num * 10
    return (num * 100 // 1) / 10 ** (count + 2)

print(tsf(1234))

print(math.floor(math.log(1234, 10)))

print('{0:.3g}'.format(1.2354230495823049582098))

