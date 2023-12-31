import pygame
pygame.init()
class Slide:
    def __init__(self,screen,Color=(0,0,0),y=0,x=-500,Per_Frame=2,Width=500,height=600):
        self.screen=screen
        self.Color=Color
        self.Vertical=y
        self.Horizontal=x
        self.PF=Per_Frame
        self.Width=Width
        self.height=height
        self.rect=pygame.Rect(self.Horizontal,self.Vertical,self.Width,self.height)
        
    def Update(self):
        #print(self.Horizontal)
        self.Horizontal+=self.PF
        self.rect=pygame.Rect(self.Horizontal,self.Vertical,self.Width,self.height)
    def Draw(self):
        pygame.draw.rect(self.screen,self.Color,self.rect)