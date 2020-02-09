# With all regards to Daniel Shiffman
# This is  my humble recreation  of his coding challenge #5 Space Invaders   https://www.youtube.com/watch?v=biN3v3ef-Y0&t=134s  using python and PyQt5


from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import QtGui
from PyQt5.QtGui import QPainter, QBrush, QPen
from PyQt5.QtCore import Qt, QTimer
import sys
import math


width = 600  # Width of window
height = 600 # Height of window


def calculateDistance(x1, y1, x2, y2):                  # Simple function to calculate distance between flowers and water to check its collision
    dist = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    return dist

class Ship:
    def __init__(self):
        self.x = width/2

    def move_left(self):
        self.x = self.x - 10

    def move_right(self):
        self.x = self.x + 10

    def update(self):
        return self.x

Direction = True

Ship_one = Ship()

class Flower:
    def __init__(self, x):
        self.x = x
        self.y = 50
        self.r = 60  # r is not actual radius in this case, its width and height of our circles

    def grow(self):
        self.r = self.r + 2

    def move_left(self):
        self.x = self.x - 1

    def move_right(self):
        self.x = self.x + 1

    def move_down(self):
        self.y = self.y + 10


Flowers = []
for i in range(5):
    Flowers.append(Flower(i*100+50))

class Drop():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.r = 8

    def move(self):
        self.y = self.y - 1

    def hit(self, flower):
        distance = calculateDistance(self.x, self.y, flower.x, flower.y)
        if distance < self.r + flower.r - 5:
            return True
        else:
            return False


Drops = []


class MyWindow(QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.setGeometry(200, 200, width, height) # 200px are our (0,0) coordinates or inception of canvas
        self.setWindowTitle("Space invaders")
        p = self.palette()
        p.setColor(self.backgroundRole(), QtGui.QColor(53,53,53))  # set background
        self.setPalette(p)
        self.timer = QTimer(self)  # timer is necessity to perform updates or changes
        self.timer.timeout.connect(self.change)
        self.timer.start(5)  # commit function change every 5 miliseconds

    def change(self):
        global Direction
        for i in range(0, len(Drops)):
            Drops[i].move()

        for i in range(len(Flowers)):
            for j in range(len(Drops)):
                if Drops[j].hit(Flowers[i]):   #check if water hits flower
                    del Drops[j]               # delete drop from array
                    Flowers[i].grow()
                    break
        self.update()

        if Flowers[len(Flowers)-1].x > width - 40: #Change direction if flowers move out from frame
            for i in range(len(Flowers)):
                Flowers[i].move_down()
                Direction = False
        elif Flowers[0].x < 10:
            for i in range(len(Flowers)):
                Flowers[i].move_down()
                Direction = True
        else:
            pass


        if Direction:
            for i in range(len(Flowers)):
                Flowers[i].move_right()  # if direction is True, all the flowers move right
        else:
            for i in range(len(Flowers)):
                Flowers[i].move_left()   # if direction is False, all the flowers move right

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setPen(QPen(Qt.black, 5, Qt.SolidLine))
        painter.setBrush(QBrush(Qt.yellow, Qt.SolidPattern))
        painter.drawRect(round(Ship_one.x), round(height - 60), 20, 60)  # draw our ship

        painter.setPen(QPen(QtGui.QColor(255,0,200), 5, Qt.SolidLine))
        painter.setBrush(QBrush(QtGui.QColor(255,0,200), Qt.SolidPattern))
        for i in range(5):
            painter.drawEllipse(round(Flowers[i].x), round(Flowers[i].y), round(Flowers[i].r), round(Flowers[i].r)) # draw all Flowers array

        painter.setPen(QPen(QtGui.QColor(150,0,255), 5, Qt.SolidLine))
        painter.setBrush(QBrush(QtGui.QColor(150,0,255), Qt.SolidPattern))
        for j in range(0, len(Drops)):
            painter.drawEllipse(round(Drops[j].x), round(Drops[j].y), round(Drops[j].r), round(Drops[j].r))        # draw all Drops array


    def keyPressEvent(self, e):   # means literraly what it says
        if e.key() == Qt.Key_Escape:
            self.close()
        elif e.key() == Qt.Key_A:
            Ship_one.move_left()
        elif e.key() == Qt.Key_D:
            Ship_one.move_right()
        elif e.key() == Qt.Key_W:
            Drops.append(Drop(Ship_one.x + 4, height - 60))
        else:
            pass



def window():
    app = QApplication(sys.argv)
    win = MyWindow()
    win.show()
    sys.exit(app.exec_())
    win.paintEvent()

window()