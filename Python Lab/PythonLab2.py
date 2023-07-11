# Reevu Adakroy
# Period 7
# Python Lab 2

def string_times(str, n):
  return str*n

def front_times(str, n):
  return str[:3]*n

def string_bits(str):
  return str[::2]

def string_splosion(str):
  return ''.join(str[:n] for n in range(len(str)+1))

def last2(str):
  return sum(str[n:n+2]==str[-2:] for n in range(len(str)-2))
  #return str.count(str[-2:])-1

def array_count9(nums):
  #return sum(n==9 for n in nums)
  return nums.count(9)

def array_front9(nums):
  return 9 in nums[:4]

def array123(nums):
  #return ' 1 2 3 ' in ' '+' '.join(str(i) for i in nums)+' '
  return (1,2,3) in zip(nums, nums[1:], nums[2:])

def string_match(a, b):
  return sum(a[n]==b[n] and a[n+1]==b[n+1] for n in range(0, min(len(a), len(b))-1))

#Logic-2
def make_bricks(small, big, goal):
  return goal%5<=small>=goal-5*big

def lone_sum(a, b, c):
  return sum(x for x in [a, b, c] if ((a==x) + (b==x) + (c==x)) == 1 )

def lucky_sum(a, b, c):
  #return (a != 13)*1 and (a*(b == 13) or (a+b)*(c == 13) or a+b+c)
  return [a+b+c, a+b, a, 0][3*(a==13) or 2*(b==13) or c==13]

def no_teen_sum(a, b, c):
  return sum(n for n in [a, b, c] if(n<13 or n>19 or n==15 or n==16))

def round_sum(a, b, c):
  return sum(10*(n%10 // 5 + n // 10) for n in [a, b, c])

def close_far(a,b,c):
  return bool((abs(b-c) > 1) and ((abs(b-a)>1) + (abs(c-a)>1))%2)

def make_chocolate(small, big, goal):
  #return -1 if 5*big+small < goal or goal%5>small else goal%5 if(goal//5 < big) else goal-5*big
  #return [-1, goal-5*big, goal%5][(goal%5<=small>=goal-5*big) + (goal//5<big)*(goal%5<=small)]
  #return [-1, goal-5*big, goal%5][((small>=goal-5*big)+(goal//5<big))*(goal%5<=small)]
  return [-1, p:=goal-5*big, goal%5][((small>=p)+(goal//5<big))*(goal%5<=small)]

#String-2
def double_char(str):
  return ''.join(n*2 for n in str)

def count_hi(str):
  #return sum(z[0]+z[1]=='hi' for z in zip(str, str[1:]))
  #return sum([*z]==[*'hi'] for z in zip(str, str[1:]))
  return str.count('hi')

def cat_dog(str):
  #return len(p:=[n=='g' for i, n in enumerate(str[2:]) if((q:=str[i] + str[i+1] + n)=='dog' or q=='cat')])==2*sum(p)
  return str.count('dog')==str.count('cat')

def count_code(str):
  #return sum(str[i]+str[i+1]+n=='coe' for i, n in enumerate(str[3:]))
  #return sum([*z]==[*'coe'] for z in zip(str, str[1:],str[3:]))
  return [*zip(str, str[1:],str[3:])].count(('c','o','e'))

def end_other(a, b):
  return a[-len(b)+0:].lower() == b.lower() or b[-len(a)+0:].lower() == a.lower()

def xyz_there(str):
  return 'xyz' in str.replace('.x', ' ')

#List-2
def count_evens(nums):
  return sum(not n%2 for n in nums)

def big_diff(nums):
  return max(nums) - min(nums)

def centered_average(nums):
  return (sum(nums) - max(nums) - min(nums))//(len(nums)-2)
  #return sum(nums.sort()[1:-1])//(len(nums)-2)

def sum13(nums):
  return sum(z[1] for z in zip([0]+nums, nums) if z[0]!=13!=z[1])

def sum67(nums):
  return 0 if len(nums)==0 else (nums[0]+sum67(nums[1:]) if nums[0]!=6 else sum67(nums[nums.index(7)+1:]))
  #return len(nums) and [nums[0]+sum67(nums[1:]), sum67(nums[nums.index(7)+1:])][(nums[0]!=6)+1]

def has22(nums):
  #return bool(sum(z[0]==z[1]==2 for z in zip(nums, nums[1:])))
  #return 2 in nums and (nums[0]==2==nums[1] or has22(nums[1:])
  return (2,2) in zip(nums, nums[1:])