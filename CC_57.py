# With all regards to Daniel Shiffman
# This is  my humble recreation  of his coding challenge #57 Mapping Earthquake Data   https://www.youtube.com/watch?v=ZiYdOwOrGyc&t=349s  using python and PyQt5
# Added ability to change color of earthquakes, and slight imitation of wave from random earthquake


from PIL import Image
from PyQt5 import QtWidgets
from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit
from PyQt5 import QtGui
from PyQt5.QtGui import QImage, QPalette
from PyQt5.QtGui import QPainter, QBrush, QPen
from PyQt5.QtCore import Qt, QTimer
import sys
import requests
import pandas as pd
import math
import random

clat = 0 # coordinates of zero point of screen
clon = 0

width = 1024
height = 512

df = pd.read_csv('https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_month.csv', header=0, usecols=[1, 2]) # load cvs file with pandas

a = []

for i in range(0, len(df)):
    a.append([df['longitude'][i], df['latitude'][i]])   # filter longitude and latitude from unnessesary data



from PIL.ImageQt import ImageQt

url = 'https://api.mapbox.com/styles/v1/mapbox/dark-v9/static/0,0,1,0,0/1024x512?access_token=pk.eyJ1IjoibWFkaWdvcjkyIiwiYSI6ImNrNTB5OWY3bzBtN2wza21pOXU1bXVza20ifQ.AYAS474vX3MtumiehnwcLg'

try:
    resp = requests.get(url, stream=True).raw  # load our url map

except requests.exceptions.RequestException as e:
    sys.exit(1)

try:
    img = Image.open(resp)

except IOError:
    print("Unable to open image")
    sys.exit(1)

zoom = 1


def mercX(lon):     # calculating x coordinates degrees
    lon = math.radians(lon)
    a = (256 / math.pi) * math.pow(2, zoom)
    b = lon + math.pi
    return a * b


def mercY(lat):   # calculating y coordinates from degrees
    lat = math.radians(lat)
    a = (256 / math.pi) * math.pow(2, zoom)
    b = math.tan(math.pi / 4 + lat / 2)
    c = math.pi - math.log(abs(b))
    return a * c


data = []
for i in range(0, len(a)):
    data.append([mercX(a[i][0]), mercY(a[i][1])])  # our final data array with x,y coordinates


class MyWindow(QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.setGeometry(0, 0, 1024, 512)
        self.setWindowTitle("Earthquakes")
        self.initUI()
        img1 = ImageQt(img)
        pixmap = QtGui.QPixmap.fromImage(img1)
        oImage = QImage(pixmap)   # reformat file to read it by PyQt5
        sImage = oImage.scaled(QSize(1024, 512))
        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(sImage))
        self.setPalette(palette)
        self.timer = QTimer(self)  # timer is necessity to perform updates or changes
        self.timer.timeout.connect(self.change)
        self.timer.start(50)  # commit function change every 50 milliseconds
        self.z = round(random.randint(0, len(data)))  # random data coordinates  to imitate earthquakes
        self.r = 10                     # initial radius of wave from earthquake
        self.speed = 1 # initial speed of wave from earthquake
        self.transparency = 255 # initial transparency of wave
        self.probability = round(random.randint(0, 10))  # probability of earthquakes
        self.red = 255 # red color which we can change through LineEdit
        self.green = 0 # green color which we can change through LineEdit
        self.blue = 255 # blue color which we can change through LineEdit

    def initUI(self):
        self.textbox = QLineEdit(self)
        self.textbox.move(0, 485)
        self.textbox.resize(200, 35)
        self.textbox.setPlaceholderText("r,g,b")
        self.textbox.setStyleSheet("font: bold 20px;"
                                   "font-family:arial;"
                                   "color:black;"
                                   "padding-bottom: 7px;"
                                   "padding-left: 15px;"
                                   )

        self.setFocus()  # set focus out from our textbox, to see hint(placeholder)

        self.b1 = QtWidgets.QPushButton(self)
        self.b1.setText("Change Color")
        self.b1.clicked.connect(self.clicked)
        self.b1.move(201, 485)

    def clicked(self):
        red = ''
        green = ''
        blue = ''
        color = self.textbox.text()
        commas = []
        for i in range(0, len(color)):
            if color[i] == ",":
                commas.append(int(i))  # check where is our commas to understand input format
        for j  in range(0, commas[0]):  #set red color, depending from first comma
            red =  red + color[j]
        red = int(red)


        b = commas[1]- commas[0] - 1     # lenght of green color
        for q in range(commas[1] - b, commas[1]):   # setting green color depending on second comma and differences between commas
            green = green + color[q]
        green = int(green)

        for w in range(commas[1]+1, len(color)):  # setting blue color, which depends from second comma and length of input
            blue = blue + color[w]
        blue = int(blue)

        self.red = red
        self.green = green
        self.blue = blue


    def change(self):
        self.speed = self.speed + 1  # add acceleration to wave
        self.r = self.r + self.speed # spread wave
        self.transparency = self.transparency - 10 # fade transparency
        if self.transparency < 10:
            self.transparency = 0 # if transparency < 0 il looks like black

        if self.r > 500:  # if radius > 500 choose new point and with probability 10% show it in paintEvent function
            self.r = 1
            self.speed = 1
            self.z = random.randint(0, len(data))
            self.transparency = 255
            self.probability = round(random.randint(0, 10))
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setBrush(QBrush(QtGui.QColor(self.red, self.green, self.blue, 10), Qt.SolidPattern))
        for i in range(0, len(data)):
            painter.drawEllipse(round(data[i][0]), round(data[i][1] - height / 2), 8, 8)  # show all earthquakes



        if self.probability == 1:
            painter.setPen(
                QPen(QtGui.QColor(self.red, self.green, self.blue, round(self.transparency)), 1, Qt.SolidLine))
            painter.setBrush(
                QBrush(QtGui.QColor(self.red, self.green, self.blue, round(self.transparency)), Qt.SolidPattern))
            painter.drawEllipse(round(data[self.z][0] - self.r / 2), round(data[self.z][1] - height / 2 - self.r / 2),
                                self.r, self.r)   # show wave


def window():
    app = QApplication(sys.argv)
    win = MyWindow()

    win.show()
    sys.exit(app.exec_())


window()
