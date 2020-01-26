# With all regards to Daniel Shiffman
# This is  my humble recreation  of his coding challenge #3 Purple Rain    https://www.youtube.com/watch?v=KkyIDI6rQJI  using python and pygame



import pygame
import random

width = 400
height = 400

pygame.init()
clock = pygame.time.Clock()
Display = pygame.display.set_mode((width, height))
pygame.display.set_caption('Purple Rain')
Display.fill((230, 230, 250))

Drops = []

def map(n, start1, stop1, start2, stop2):      # implementation of map function that stretch our values to canvas scale
    return ((n-start1)/(stop1-start1))*(stop2-start2)+start2

class Drop:
    def __init__(self):
        self.x = random.randint(0, width)
        self.y = random.randint(-500, -100)
        self.z = random.randint(0, 20)
        self.len = map(self.z, 0, 20, 10, 20)
        self.yspeed = map(self.z, 0, 20, 4, 10)


    def fall(self):
        self.y = self.y + self.yspeed
        grav = map(self.z, 0, 20, 0, 0.2)
        self.yspeed = self.yspeed + grav

        if (self.y > height):
            self.y = random.randint(-200, -100)
            self.yspeed = map(self.z, 0, 20, 4, 10)

    def show(self):
        pygame.draw.rect(Display, (138, 43, 226), (int(self.x), int(self.y), 1, int(self.len)))
#        print(self.x, self.y)

for i in range(500):
    Drops.append(Drop())


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
    Display.fill((230, 230, 250))

    for i in range(len(Drops)):
        Drops[i].fall()
        Drops[i].show()
    pygame.display.update()
    clock.tick(60)


pygame.display.update()


