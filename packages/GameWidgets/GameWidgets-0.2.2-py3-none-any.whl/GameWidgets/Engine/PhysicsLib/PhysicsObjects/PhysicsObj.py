import pygame
pygame.init()

class PhysicsObj:
    def __init__(self, world, start_pos:tuple):
        self.gravity = world.gravity
        self.air_res = world.air_resistance
        self.allthings = world.solids
        self.xpos = start_pos[0]
        self.ypos = start_pos[1]
        self.xvel = 0
        self.yvel = 0
        self.g = False

    def set_rect(self, rect:pygame.Rect):
        self.rect = rect
    
    def change_acc(self,xvel:tuple,yvel:tuple):
        self.xvel = xvel
        self.yvel = yvel

    def return_pos(self):
        return (self.xpos,self.ypos)
    
    def update_pos(self):
        if self.g != True:
            self.friction = self.air_res
        else:
            self.friction = 0.5
        
        if self.rect.collidelist(self.allthings):
            self.g = True
        else:
            self.g = False

        if self.xvel > 0:
            self.x += self.xvel - self.air_res - self.friction
        elif self.xvel <0:
            self.x -= self.xvel + self.air_res + self.friction
        
        

