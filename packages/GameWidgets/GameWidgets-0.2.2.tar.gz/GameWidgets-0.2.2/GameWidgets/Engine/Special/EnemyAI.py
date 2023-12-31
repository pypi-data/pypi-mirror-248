import pygame
import math
pygame.init()

class Enemy:
    def __init__(self,screen,xy,speed,follow):
        self.screen = screen
        self.width = 50
        self.height = 50
        self.x,self.y = xy[0],xy[1]
        self.surf = pygame.Surface((self.width,self.height))
        self.radius = self.surf.get_width()/2
        self.rect = self.surf.get_rect()
        self.rect.topleft = (self.x,self.y)
        self.speed = speed
        self.player = follow

    def Draw(self):
        self.rect.center = (self.x,self.y)
        pygame.draw.circle(self.surf,(255,0,0),(self.surf.get_width()/2,self.surf.get_height()/2),self.radius)
        self.screen.blit(self.surf,self.rect)

    def pathfind(self):
        pygame.draw.line(self.screen,(255,255,255),(self.x,self.y),(self.player.x,self.player.y))
        self.distancex = self.player.x - self.x
        self.distancey = self.player.y - self.y
        #print(self.distancex,self.distancey)
        self.changex = self.distancex/(self.speed*2)
        self.changey = self.distancey/(self.speed*2)        
        '''if self.changex < 0 or self.changey < 0:
            if self.changex < 0:
                self.changex *= -1
            if self.changey < 0:
                self.changey *= -1
        else:
            if self.changex > 0:
                self.changex *= -1
            if self.changey > 0:
                self.changey *= -1'''
        #print(self.changex,self.changey)
        self.changex /= self.speed
        self.changey /= self.speed
        self.x += self.changex
        self.y += self.changey
    
    def detect(self):
        return self.rect.colliderect(self.player.rect)