#Simple implemintation  of Q learning, agent tries to find target
#Based on github repository  https://github.com/MorvanZhou/Reinforcement-learning-with-tensorflow   and youtube videos https://www.youtube.com/playlist?list=PLXO45tsB95cIplu-fLMpUEEZTwrDNh6Ba


from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QTableWidget, QTableWidgetItem, QLineEdit
from PyQt5 import QtGui
from PyQt5.QtGui import QPainter, QBrush, QPen
from PyQt5.QtCore import Qt, QTimer
import sys
import numpy as np
import pandas as pd

width = 400
height = 400

x = 10
y = 10

learning_rate=0.01
reward_decay=0.9
e_greedy=0.9
actions = ['u', 'd', 'r', 'l']


class QLearningTable:
    def __init__(self):
        self.q_table = pd.DataFrame(columns=actions, dtype=np.float64)

    def choose_action(self, observation):
        self.check_state_exist(observation)
        if np.random.uniform() < e_greedy:
            state_action = self.q_table.loc[observation, :] # returns [q1,q2,q3,q4]
            action = np.random.choice(state_action[state_action == np.max(state_action)].index) # returns index of action
        else:
            #choose random action
            global actions
            action = np.random.choice(actions)
        return action # 'u', 'd', 'r', 'l'


    def check_state_exist(self, state):
        if state not in self.q_table.index:
            self.q_table = self.q_table.append(pd.Series([0]*len(actions), index=self.q_table.columns, name=state))

    def learn(self, s, a, r, s_):
#        print(s,a,r,s_)
        global x, y
        self.check_state_exist(s_)
        q_predict = self.q_table.loc[s, a]
        if s_ !='terminal':
            q_target = r + reward_decay*self.q_table.loc[s_, :].max()
        else:
            q_target = r
            x, y = 10, 10
        self.q_table.loc[s,a] += learning_rate * (q_target - q_predict)

    def step(self,action):
        global x,y
        s = (x,y)
        q = False # means done action
        if action == "u": # up
            if y != 10:
                y = y - 100
                q = True
        elif action == "d": # down
                if y != 310:
                    y = y + 100
                    q= True
        elif action == "r": #right
            if x != 310:
                x = x + 100
                q = True
        elif action == "l": #left
            if x != 10:
                x = x - 100
                q = True

        s_ = (x, y)

        if  s_ == (10+100,10+200): # wall
            reward = -50
            s_ = 'terminal'
        elif s == (10+200,10+100): #wall
            reward = -50
            s_ = 'terminal'
        elif s == (10+300,10+300): #trap
            reward = -20
            s_ = 'terminal'
        elif s == (10+200,10+200): # target
            reward = 100
            s_ = 'terminal'
#            print("target")
        else:
            reward = 0
        if s_ != "terminal":
            x = s_[0]
            y = s_[1]
        else:
            pass

        return s, s_,reward, q



table = QLearningTable()






class MyWindow(QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.setGeometry(0, 0, 800, 500)
        self.setWindowTitle("Space invaders")
        p = self.palette()
        p.setColor(self.backgroundRole(), QtGui.QColor(53,53,53))
        self.setPalette(p)
        self.timer = QTimer(self)  # timer is necessity to perform updates or changes
        self.timer.timeout.connect(self.change)
        self.timer.start(50)  # commit function change every 50 milliseconds

        self.labelPlayer = QLabel(self)
        self.labelPlayer.setText('Player')
        self.labelPlayer.move(110, 430)
        self.labelPlayer.setFont(QtGui.QFont("Times", 20, QtGui.QFont.Bold))


        self.labelTrap = QLabel(self)
        self.labelTrap.setText('Trap')
        self.labelTrap.move(310, 430)
        self.labelTrap.setFont(QtGui.QFont("Times", 20, QtGui.QFont.Bold))

        self.labelTarget = QLabel(self)
        self.labelTarget.setText('Target')
        self.labelTarget.move(510, 430)
        self.labelTarget.setFont(QtGui.QFont("Times", 20, QtGui.QFont.Bold))

        self.labelWall = QLabel(self)
        self.labelWall.setText('Wall')
        self.labelWall.move(710, 430)
        self.labelWall.setFont(QtGui.QFont("Times", 20, QtGui.QFont.Bold))

        self.labelq1 = QLabel(self)
        self.labelq1.setText('0.0 0.0 0.0 0.0')
        self.labelq1.move(410, 40)
        self.labelq1.setFont(QtGui.QFont("Times", 10, QtGui.QFont.Bold))

        self.labelq2 = QLabel(self)
        self.labelq2.setText('0.0 0.0 0.0 0.0')
        self.labelq2.move(510, 40)
        self.labelq2.setFont(QtGui.QFont("Times", 10, QtGui.QFont.Bold))

        self.labelq3 = QLabel(self)
        self.labelq3.setText('0.0 0.0 0.0 0.0')
        self.labelq3.move(610, 40)
        self.labelq3.setFont(QtGui.QFont("Times", 10, QtGui.QFont.Bold))

        self.labelq4 = QLabel(self)
        self.labelq4.setText('0.0 0.0 0.0 0.0')
        self.labelq4.move(710, 40)
        self.labelq4.setFont(QtGui.QFont("Times", 10, QtGui.QFont.Bold))

        self.labelq5 = QLabel(self)
        self.labelq5.setText('0.0 0.0 0.0 0.0')
        self.labelq5.move(410, 140)
        self.labelq5.setFont(QtGui.QFont("Times", 10, QtGui.QFont.Bold))

        self.labelq6 = QLabel(self)
        self.labelq6.setText('0.0 0.0 0.0 0.0')
        self.labelq6.move(510, 140)
        self.labelq6.setFont(QtGui.QFont("Times", 10, QtGui.QFont.Bold))

        self.labelq7 = QLabel(self)
        self.labelq7.setText('0.0 0.0 0.0 0.0')
        self.labelq7.move(610, 140)
        self.labelq7.setFont(QtGui.QFont("Times", 10, QtGui.QFont.Bold))

        self.labelq8 = QLabel(self)
        self.labelq8.setText('0.0 0.0 0.0 0.0')
        self.labelq8.move(710, 140)
        self.labelq8.setFont(QtGui.QFont("Times", 10, QtGui.QFont.Bold))

        self.labelq9 = QLabel(self)
        self.labelq9.setText('0.0 0.0 0.0 0.0')
        self.labelq9.move(410, 240)
        self.labelq9.setFont(QtGui.QFont("Times", 10, QtGui.QFont.Bold))

        self.labelq10 = QLabel(self)
        self.labelq10.setText('0.0 0.0 0.0 0.0')
        self.labelq10.move(510, 240)
        self.labelq10.setFont(QtGui.QFont("Times", 10, QtGui.QFont.Bold))

        self.labelq11 = QLabel(self)
        self.labelq11.setText('0.0 0.0 0.0 0.0')
        self.labelq11.move(610, 240)
        self.labelq11.setFont(QtGui.QFont("Times", 10, QtGui.QFont.Bold))

        self.labelq12 = QLabel(self)
        self.labelq12.setText('0.0 0.0 0.0 0.0')
        self.labelq12.move(710, 240)
        self.labelq12.setFont(QtGui.QFont("Times", 10, QtGui.QFont.Bold))

        self.labelq13 = QLabel(self)
        self.labelq13.setText('0.0 0.0 0.0 0.0')
        self.labelq13.move(410, 340)
        self.labelq13.setFont(QtGui.QFont("Times", 10, QtGui.QFont.Bold))

        self.labelq14 = QLabel(self)
        self.labelq14.setText('0.0 0.0 0.0 0.0')
        self.labelq14.move(510, 340)
        self.labelq14.setFont(QtGui.QFont("Times", 10, QtGui.QFont.Bold))

        self.labelq15 = QLabel(self)
        self.labelq15.setText('0.0 0.0 0.0 0.0')
        self.labelq15.move(610, 340)
        self.labelq15.setFont(QtGui.QFont("Times", 10, QtGui.QFont.Bold))

        self.labelq16 = QLabel(self)
        self.labelq16.setText('0.0 0.0 0.0 0.0')
        self.labelq16.move(710, 340)
        self.labelq16.setFont(QtGui.QFont("Times", 10, QtGui.QFont.Bold))


    def paintEvent(self, event):
        global x, y
        painter = QPainter(self)
        painter.setPen(QPen(Qt.black, 1, Qt.SolidLine))
        painter.setBrush(QBrush(Qt.yellow, Qt.SolidPattern))
        for i in range(1,5):
            painter.drawLine(100*i,0,100*i,height)
            painter.drawLine(0,100*i,width,100*i)




        painter.setPen(QPen(QtGui.QColor(0,0,0), 5, Qt.SolidLine)) # wall
        painter.setBrush(QBrush(QtGui.QColor(0,0,0), Qt.SolidPattern))
        painter.drawRect(10+100,10+200,80,80)

        painter.setPen(QPen(QtGui.QColor(0,0,0), 5, Qt.SolidLine)) # wall
        painter.setBrush(QBrush(QtGui.QColor(0,0,0), Qt.SolidPattern))
        painter.drawRect(10+200,10+100,80,80)

        painter.setPen(QPen(QtGui.QColor(0,255,0), 5, Qt.SolidLine)) # target
        painter.setBrush(QBrush(QtGui.QColor(0,255,0), Qt.SolidPattern))
        painter.drawRect(10+200,10+200,80,80)

        painter.setPen(QPen(QtGui.QColor(255,0,0), 5, Qt.SolidLine)) # trap
        painter.setBrush(QBrush(QtGui.QColor(255,0,0), Qt.SolidPattern))
        painter.drawRect(10+300,10+300,80,80)

        painter.setPen(QPen(QtGui.QColor(255,255,0), 5, Qt.SolidLine)) # player
        painter.setBrush(QBrush(QtGui.QColor(255,255,0), Qt.SolidPattern))
        painter.drawRect(x,y,80,80)

        painter.setPen(QPen(QtGui.QColor(255,255,0), 5, Qt.SolidLine)) # player legend
        painter.setBrush(QBrush(QtGui.QColor(255,255,0), Qt.SolidPattern))
        painter.drawRect(10,410,80,80)

        painter.setPen(QPen(QtGui.QColor(255,0,0), 5, Qt.SolidLine)) # trap
        painter.setBrush(QBrush(QtGui.QColor(255,0,0), Qt.SolidPattern))
        painter.drawRect(210,410,80,80)

        painter.setPen(QPen(QtGui.QColor(0,255,0), 5, Qt.SolidLine)) # target
        painter.setBrush(QBrush(QtGui.QColor(0,255,0), Qt.SolidPattern))
        painter.drawRect(410,410,80,80)

        painter.setPen(QPen(QtGui.QColor(0,0,0), 5, Qt.SolidLine)) # wall
        painter.setBrush(QBrush(QtGui.QColor(0,0,0), Qt.SolidPattern))
        painter.drawRect(610,410,80,80)



    def change(self):
        current_state = (x, y)
        a = table.choose_action(str(current_state))
        s, s_, reward, q = table.step(a)
        if q == True:
            table.learn(str(s), a, reward, str(s_))
        self.updateQTable() # update text
        self.update()

    def updateQTable(self):
        a = (10,10)
        if str(a) in table.q_table.index:
            q = str(round(table.q_table.loc[str(a), 'u'], 1)) + " " + str(round(table.q_table.loc[str(a), 'd'], 1)) + " " + str(round(table.q_table.loc[str(a), 'l'], 1)) + " " + str(round(table.q_table.loc[str(a), 'r'], 1))
            self.labelq1.setText(q)

        b = (110,10)
        if str(b) in table.q_table.index:
            q = str(round(table.q_table.loc[str(b), 'u'], 1)) + " " + str(round(table.q_table.loc[str(b), 'd'], 1)) + " " + str(round(table.q_table.loc[str(b), 'l'], 1)) + " " + str(round(table.q_table.loc[str(b), 'r'], 1))
            self.labelq2.setText(q)

        c = (210,10)
        if str(c) in table.q_table.index:
            q = str(round(table.q_table.loc[str(c), 'u'], 1)) + " " + str(round(table.q_table.loc[str(c), 'd'], 1)) + " " + str(round(table.q_table.loc[str(c), 'l'], 1)) + " " + str(round(table.q_table.loc[str(c), 'r'], 1))
            self.labelq3.setText(q)

        d = (310,10)
        if str(d) in table.q_table.index:
            q = str(round(table.q_table.loc[str(d), 'u'], 1)) + " " + str(round(table.q_table.loc[str(d), 'd'], 1)) + " " + str(round(table.q_table.loc[str(d), 'l'], 1)) + " " + str(round(table.q_table.loc[str(d), 'r'], 1))
            self.labelq4.setText(q)

        f = (10,110)
        if str(f) in table.q_table.index:
            q = str(round(table.q_table.loc[str(f), 'u'], 1)) + " " + str(round(table.q_table.loc[str(f), 'd'], 1)) + " " + str(round(table.q_table.loc[str(f), 'l'], 1)) + " " + str(round(table.q_table.loc[str(f), 'r'], 1))
            self.labelq5.setText(q)

        g = (110,110)
        if str(g) in table.q_table.index:
            q = str(round(table.q_table.loc[str(g), 'u'], 1)) + " " + str(round(table.q_table.loc[str(g), 'd'], 1)) + " " + str(round(table.q_table.loc[str(g), 'l'], 1)) + " " + str(round(table.q_table.loc[str(g), 'r'], 1))
            self.labelq6.setText(q)

        h = (210,110)
        if str(h) in table.q_table.index:
            q = str(round(table.q_table.loc[str(h), 'u'], 1)) + " " + str(round(table.q_table.loc[str(h), 'd'], 1)) + " " + str(round(table.q_table.loc[str(h), 'l'], 1)) + " " + str(round(table.q_table.loc[str(h), 'r'], 1))
            self.labelq7.setText(q)

        i = (310,110)
        if str(i) in table.q_table.index:
            q = str(round(table.q_table.loc[str(i), 'u'], 1)) + " " + str(round(table.q_table.loc[str(i), 'd'], 1)) + " " + str(round(table.q_table.loc[str(i), 'l'], 1)) + " " + str(round(table.q_table.loc[str(i), 'r'], 1))
            self.labelq8.setText(q)

        j = (10,210)
        if str(j) in table.q_table.index:
            q = str(round(table.q_table.loc[str(j), 'u'], 1)) + " " + str(round(table.q_table.loc[str(j), 'd'], 1)) + " " + str(round(table.q_table.loc[str(j), 'l'], 1)) + " " + str(round(table.q_table.loc[str(j), 'r'], 1))
            self.labelq9.setText(q)

        k = (110,210)
        if str(k) in table.q_table.index:
            q = str(round(table.q_table.loc[str(k), 'u'], 1)) + " " + str(round(table.q_table.loc[str(k), 'd'], 1)) + " " + str(round(table.q_table.loc[str(k), 'l'], 1)) + " " + str(round(table.q_table.loc[str(k), 'r'], 1))
            self.labelq10.setText(q)

        l = (210,210)
        if str(l) in table.q_table.index:
            q = str(round(table.q_table.loc[str(l), 'u'], 1)) + " " + str(round(table.q_table.loc[str(l), 'd'], 1)) + " " + str(round(table.q_table.loc[str(l), 'l'], 1)) + " " + str(round(table.q_table.loc[str(l), 'r'], 1))
            self.labelq11.setText(q)

        m = (310,210)
        if str(m) in table.q_table.index:
            q = str(round(table.q_table.loc[str(m), 'u'], 1)) + " " + str(round(table.q_table.loc[str(m), 'd'], 1)) + " " + str(round(table.q_table.loc[str(m), 'l'], 1)) + " " + str(round(table.q_table.loc[str(m), 'r'], 1))
            self.labelq12.setText(q)

        n = (10,310)
        if str(n) in table.q_table.index:
            q = str(round(table.q_table.loc[str(n), 'u'], 1)) + " " + str(round(table.q_table.loc[str(n), 'd'], 1)) + " " + str(round(table.q_table.loc[str(n), 'l'], 1)) + " " + str(round(table.q_table.loc[str(n), 'r'], 1))
            self.labelq13.setText(q)

        o = (110,310)
        if str(o) in table.q_table.index:
            q = str(round(table.q_table.loc[str(o), 'u'], 1)) + " " + str(round(table.q_table.loc[str(o), 'd'], 1)) + " " + str(round(table.q_table.loc[str(o), 'l'], 1)) + " " + str(round(table.q_table.loc[str(o), 'r'], 1))
            self.labelq14.setText(q)

        p = (210,310)
        if str(p) in table.q_table.index:
            q = str(round(table.q_table.loc[str(p), 'u'], 1)) + " " + str(round(table.q_table.loc[str(p), 'd'], 1)) + " " + str(round(table.q_table.loc[str(p), 'l'], 1)) + " " + str(round(table.q_table.loc[str(p), 'r'], 1))
            self.labelq15.setText(q)

        r = (310,310)
        if str(r) in table.q_table.index:
            q = str(round(table.q_table.loc[str(r), 'u'], 1)) + " " + str(round(table.q_table.loc[str(r), 'd'], 1)) + " " + str(round(table.q_table.loc[str(r), 'l'], 1)) + " " + str(round(table.q_table.loc[str(r), 'r'], 1))
            self.labelq16.setText(q)

def window():
    app = QApplication(sys.argv)
    win = MyWindow()
    win.show()
    sys.exit(app.exec())
    win.paintEvent()

window()



