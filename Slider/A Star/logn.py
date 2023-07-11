def priorityInsert(lst, a):
    if not lst:
        lst.append(a)
    else:
        start = 0
        end = len(lst)
        while start != end and start != end-1:
            mid = (start+end)//2
            if lst[mid] < a:
                end = mid
            else: start = mid
        if a < lst[start]:
            lst.insert(end, a)
        else: lst.insert(start, a)


lst = []
# for i in range(5):
#     lst.append((i, 'a' + str(i)))


print(lst)
priorityInsert(lst, 2)
print(lst)
priorityInsert(lst, 4)
print(lst)
priorityInsert(lst, 5)
print(lst)
priorityInsert(lst, 10)
print(lst)
priorityInsert(lst, 4)
print(lst)