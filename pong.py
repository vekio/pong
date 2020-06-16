#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pygame

# Variables
WIDTH = 1200
HEIGHT = 600
BORDER = 20
VELOCITY = 1
FRAMERATE = 320

# Classes
class Ball:
    RADIUS = 20
    
    def __init__(self,x,y,vx,vy):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        
    def show(self, colour):
        global screen
        pygame.draw.circle(screen, colour, (self.x, self.y), self.RADIUS)
   
    def update(self, paddle):
        global bgColor, fgColor
        
        newx = self.x + self.vx
        newy = self.y + self.vy
        
        if newx < BORDER+self.RADIUS:
            self.vx = -self.vx
        elif newy < BORDER+self.RADIUS or newy > HEIGHT-BORDER-self.RADIUS:
            self.vy = -self.vy
        elif newx+Ball.RADIUS > WIDTH-Paddle.WIDTH and abs(newy-paddle.y) < Paddle.HEIGHT//2:
            self.vx = -self.vx
        else:
            self.show(bgColor)
            self.x += self.vx
            self.y += self.vy
            self.show(fgColor)
        
class Paddle:    
    WIDTH = 50
    HEIGHT = 100
    
    def __init__(self,y):
        self.y = y
    
    def show(self,colour):
        global screen
        pygame.draw.rect(screen, colour, pygame.Rect(WIDTH-self.WIDTH, self.y-self.HEIGHT//2, self.WIDTH, self.HEIGHT))
        
    def update(self):
        global bgColor, fgColor
        
        newy = pygame.mouse.get_pos()[1]
        
        if newy < BORDER+self.HEIGHT//2 or newy > HEIGHT-BORDER-self.HEIGHT//2:
            pass
        else:            
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
ballplay = Ball(WIDTH-Ball.RADIUS-Paddle.WIDTH, HEIGHT//2, -VELOCITY, VELOCITY)
ballplay.show(fgColor)

paddleplay = Paddle(HEIGHT//2)
paddleplay.show(fgColor)

# clock for ball velocity
clock = pygame.time.Clock()

while True:
    e = pygame.event.poll()
    if e.type == pygame.QUIT:
        break
    
    clock.tick(FRAMERATE)
    
    pygame.display.flip()
    
    ballplay.update(paddleplay)
    paddleplay.update()
    
pygame.quit()
