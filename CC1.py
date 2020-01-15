# With all regards to Daniel Shiffman
# This is  my humble recreation  of his coding challenge #1 Starfield in Processing   https://www.youtube.com/watch?v=17WoOqgXsRM  using python and tkinter

import tkinter as tk
import random
speed = 0             # lets assign speed to any value, that we change later
width = 400           # width of our canvas
height = 400          # height of our canvas
offset_x = width / 2  # we need offset instead of function translate in js, without we will see 1/4 of directions of our stars
offset_y = height / 2
Number_of_stars = 100

def map(n, start1, stop1, start2, stop2):      # implementation of map function that stretch our values to canvas scale
    return ((n-start1)/(stop1-start1))*(stop2-start2)+start2


def motion(event):
    global speed
    x, y = event.x, event.y
    speed = map(x, 0, width, 0, 50)  # changes speed according to mouse x position


root = tk.Tk()

canvas = tk.Canvas(root, bg="black", height=width, width=width)
canvas.pack()
root.configure(background='black')


class Star():
    def __init__(self):
        self.x = random.randint(-width, width)
        self.y = random.randint(-height, height)
        self.z = random.randint(1, width)

        self.pz = self.z
        sx = map(self.x / self.z, 0, 1, 0, width)
        sy = map(self.y / self.z, 0, 1, 0, height)
        r = map(self.z, 0, width, 16, 0)

        self.oval = canvas.create_oval(sx-r+offset_x, sy-r+offset_y, sx+r+offset_x, sy+r+offset_y, outline="white", fill="white", width=1) # use r correction to get circle instead of oval
        px = map(self.x / self.pz, 0, 1, 0, width)
        py = map(self.y / self.pz, 0, 1, 0, height)
        self.line = canvas.create_line(px+offset_x, py+offset_y, sx+offset_x, sy+offset_x, fill='white')

    def update(self):
        self.z = self.z - speed

        if self.z < 1:
            self.z = width
            self.x = random.randint(-width, width)
            self.y = random.randint(-height, height)
            self.pz = self.z

    def show(self):
        sx = map(self.x / self.z, 0, 1, 0, width)
        sy = map(self.y / self.z, 0, 1, 0, height)
        r = map(self.z, 0, width, 16, 0)
        canvas.coords(self.oval, sx-r+offset_x, sy-r+offset_y, sx+r+offset_x, sy+r+offset_y)

        px = map(self.x / self.pz, 0, 1, 0, width)
        py = map(self.y / self.z, 0, 1, 0, height)

        self.pz = self.z
        canvas.coords(self.line, px+offset_x, py+offset_y, sx+offset_x, sy+offset_y)


Stars_array = []
for i in range(Number_of_stars):  # Create array of Class examples
    Stars_array.append(Star())


def draw():
    for i in range(len(Stars_array)): # make of all our Stars show and move
        Stars_array[i].show()
        Stars_array[i].update()


def main():
    root.after(30, main) # update function main  in 30 miliseconds
    draw()


main()
root.bind('<Motion>', motion)
root.mainloop()

