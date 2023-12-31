import pygame
pygame.init()

class Circle():
    def __init__(self,screen:None,world:None,radius:int,startpos:tuple,Xacc:float,Yacc:float,color:tuple,
                 loss:float):
        self.screen = screen
        self.world = world
        self.r = radius
        self.x = startpos[0]
        self.y = startpos[1]
        self.xc = Xacc
        self.c = color
        self.yc = Yacc
        self.l = loss
        self.xacc = Xacc
        self.res = self.world.air_resistance
        self.g = self.world.gravity
        self.grounded = False
        self.f = self.world.friction
        self.rect = pygame.Rect(self.x, self.y, self.r*2,self.r*2)
        self.collide = self.world.solids
        self.peak = False
    
    def draw(self):
        self.rect.center = (self.x,self.y)
        pygame.draw.circle(self.screen, self.c,self.rect.topleft,self.r)

    def Update(self):
        if self.rect.collidelist(self.collide):
            self.grounded = True
        else:
            self.grounded = False
        if self.grounded == False:
            if self.peak == False and self.xc <= 0:
                self.xc = self.xacc
            self.xc -= self.res
            self.yc += self.g
            self.yc -= self.res
            self.x += self.xc
            self.y += self.yc


