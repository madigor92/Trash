# With all regards to Daniel Shiffman
# This is  my humble recreation  of his coding challenge #3 Snake   https://www.youtube.com/watch?v=AaGK-fj-BAM&t=860s  using python and pygame



width = 400
height = 400
import pygame
import random
import math

pygame.init()

x_food = random.randint(0, width / 10 - 1) * 10
y_food = random.randint(0, height / 10 - 1) * 10

gameDisplay = pygame.display.set_mode((width, height))
pygame.display.set_caption('Snake')
clock = pygame.time.Clock()
gameDisplay.fill((200,205,233))


class Snake():
    def __init__(self):
        self.x = 10
        self.y = 0
        self.xspeed = 10
        self.yspeed = 0
        self.tail = [[self.x, self.y]]




    def update(self):
        self.x = self.x + self.xspeed
        self.y = self.y + self.yspeed
        if len(self.tail) > 1:
            for i in range(len(self.tail)-1):
                self.tail[i] = self.tail[i+1]
        self.tail[len(self.tail)-1] = [self.x, self.y]


    def show(self):
        gameDisplay.fill((200, 205, 233))
        if len(self.tail) == 1:
            pygame.draw.rect(gameDisplay, (255, 0, 0), (self.tail[0][0], self.tail[0][1], 20, 20),1)
        elif len(self.tail) > 1:
            for i in range(len(self.tail) - 1):
                pygame.draw.rect(gameDisplay, (255, 0, 0), (self.tail[i][0], self.tail[i][1], 20, 20),1)
        pygame.draw.rect(gameDisplay, (255, 0, 255), (x_food, y_food, 20, 20))



Snake_one = Snake()

def key_handl():
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_LEFT:
            Snake_one.xspeed = -10
            Snake_one.yspeed = 0
        if event.key == pygame.K_RIGHT:
            Snake_one.xspeed = 10
            Snake_one.yspeed = 0
        if event.key == pygame.K_UP:
            Snake_one.yspeed = -10
            Snake_one.xspeed = 0
        if event.key == pygame.K_DOWN:
            Snake_one.yspeed = 10
            Snake_one.xspeed = 0


def qwerty():
    Snake_one.job()
    print(123)

def init_food():
    global x_food,y_food
    x_food = random.randint(0, width / 10 - 1) * 10
    y_food = random.randint(0, height / 10 - 1) * 10

def eat(pos_x, pos_y):
    dist = math.sqrt((x_food - pos_x)**2 + (y_food - pos_y)**2)
    if dist <= 1:
        init_food()
        Snake_one.tail.append([Snake_one.x - Snake_one.xspeed, Snake_one.y - Snake_one.yspeed])



while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    eat(Snake_one.x, Snake_one.y)
    Snake_one.show()
    Snake_one.update()
    key_handl()
    pygame.display.update()
    clock.tick(10)



schedule.every(2).seconds.do(qwerty)

pygame.display.update()
clock.tick(120)