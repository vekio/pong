#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pygame
import pandas as pd

# variables
WIDTH = 1200
HEIGHT = 600
BORDER = 20
VELOCITY = 4
FRAMERATE = 320

# classes
class Ball:
    RADIUS = 20
    
    def __init__(self,x,y,vx,vy):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        
    def show(self, colour):
        pygame.draw.circle(screen, colour, (self.x, self.y), self.RADIUS)
   
    def update(self):
        newx = self.x + self.vx
        newy = self.y + self.vy
        
        if newx < BORDER+self.RADIUS:
            self.vx = -self.vx
        elif newy < BORDER+self.RADIUS or newy > HEIGHT-BORDER-self.RADIUS:
            self.vy = -self.vy
        elif newx+Ball.RADIUS > WIDTH-Paddle.WIDTH \
            and abs(newy-paddle.y) < Paddle.HEIGHT//2:
            self.vx = -self.vx
        else:
            self.show(bgColor)
            self.x = newx
            self.y = newy
            self.show(fgColor)
        
class Paddle:    
    WIDTH = 50
    HEIGHT = 100
    
    def __init__(self,y):
        self.y = y
    
    def show(self,colour):
        pygame.draw.rect(screen, colour, 
                         pygame.Rect(WIDTH-self.WIDTH, 
                                     self.y-self.HEIGHT//2, 
                                     self.WIDTH, self.HEIGHT))
        
    def update(self):        
        newy = pygame.mouse.get_pos()[1]
        if newy-self.HEIGHT//2>BORDER \
            and newy+self.HEIGHT//2<HEIGHT-BORDER:
                self.show(bgColor)
                self.y = newy
                self.show(fgColor)

    def updateIA(self, newy):        
        if newy-self.HEIGHT//2>BORDER \
            and newy+self.HEIGHT//2<HEIGHT-BORDER:
                self.show(bgColor)
                self.y = newy
                self.show(fgColor)


# start the scenario
pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))

bgColor = pygame.Color("black")
fgColor = pygame.Color("white")

pygame.draw.rect(screen, fgColor, pygame.Rect(0,0,WIDTH,BORDER))
pygame.draw.rect(screen, fgColor, pygame.Rect(0,0,BORDER,HEIGHT))
pygame.draw.rect(screen, fgColor, pygame.Rect(0,HEIGHT-BORDER,WIDTH,BORDER))

# draw ball and paddle
ball = Ball(WIDTH-Ball.RADIUS-Paddle.WIDTH, HEIGHT//2, -VELOCITY, VELOCITY-1)
ball.show(fgColor)

paddle = Paddle(HEIGHT//2)
paddle.show(fgColor)

clock = pygame.time.Clock()

# file to take data
#sample = open("game.csv", "w")
#print("x,y,vx,vy,paddle.y", file=sample)

pong = pd.read_csv('game.csv')
pong = pong.drop_duplicates()

X = pong.drop(columns="paddle.y")
y = pong['paddle.y']

from sklearn.neighbors import KNeighborsRegressor

clf = KNeighborsRegressor(n_neighbors=3)
clf.fit(X,y)

df = pd.DataFrame(columns=['x', 'y', 'vx', 'vy'])

while True:
    e = pygame.event.poll()
    if e.type == pygame.QUIT:
        break
    
    clock.tick(FRAMERATE)
    
    pygame.display.flip()
    
    toPredict = df.append({'x': ball.x, 'y': ball.y, 'vx': ball.vx,
                           'vy': ball.vy,}, ignore_index=True)
    
    shouldMove = clf.predict(toPredict)
    paddle.updateIA(shouldMove)
    
    #paddle.update()
    ball.update()
    
    #print("{}, {}, {}, {}, {}".format(ball.x, ball.y, ball.vx,ball.vy,
    #                                  paddle.y),file=sample)
    
pygame.quit()
