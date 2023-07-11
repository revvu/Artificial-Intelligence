import sys; args = sys.argv[1:]
# Reevu Adakroy pd. 7
# started 4/13/2021
# tkinter circle method inspired by https://stackoverflow.com/questions/17985216/draw-circle-in-tkinter-python
import tkinter as tk
import time
import random

firefly_count = 2
r = 0.08
bumpAmount = 0.005
threshold = 0.95

potential_lst = []

def parse_input():
    if len(args)!=4:
        print('please fix input')
        exit()
    global firefly_count,r,bumpAmount,threshold
    #firefly count
    firefly_count = int(args[0])
    r = float(args[1])
    bumpAmount = float(args[2])
    threshold = float(args[3])

parse_input()

def create_circle_template(self, x, y, r, color):
    return self.create_oval(x-r, y-r, x+r, y+r, fill=color)
tk.Canvas.create_circle = create_circle_template

# f(t+delta(t)) = f(t) + r(1-f(t))
def update_potential(potential_lst):
    all_pass = False

    firefly_bump_count = 0
    #update potential
    for firefly in range(firefly_count):
        potential_lst[firefly] = potential_lst[firefly]+r*(1-potential_lst[firefly])

    while not all_pass:
        all_pass = True
        firefly_bump_count=0
        #count the cross
        for firefly in range(firefly_count):
            if potential_lst[firefly]>=threshold:
                all_pass = False
                firefly_bump_count+=1
        #go through update for threshold
        for firefly in range(firefly_count):
            if potential_lst[firefly]>=threshold or potential_lst[firefly]==0: potential_lst[firefly]=0
            else: potential_lst[firefly]+=bumpAmount*firefly_bump_count

def synchronous_check(potential_lst):
    return potential_lst.count(potential_lst[0])==len(potential_lst)

window = tk.Tk()
canvas = tk.Canvas(window, width=1000, height=100, bg="black")
canvas.grid()

for firefly in range(firefly_count):
    potential_lst+=[random.uniform(0,1)]

finished = True
for seconds in range(455):
    finished = False
    canvas.delete("all")
    update_potential(potential_lst)
    for n in range(firefly_count):
        #print(potential_lst[n])
        canvas.create_circle(50+n*100, 50, 20*potential_lst[n], ["cadetblue1","gold"][synchronous_check(potential_lst)])
    window.update()
    time.sleep(0.05)

window.destroy()

window.mainloop()