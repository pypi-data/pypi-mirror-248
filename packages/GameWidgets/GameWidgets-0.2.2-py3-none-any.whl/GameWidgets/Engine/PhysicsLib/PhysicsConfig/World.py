import pygame
pygame.init()

class World():
    def __init__(self,gravity:float,air_resistance:float):
        self.gravity = gravity
        self.air_resistance = air_resistance
        self.solids = []

    def AddSolid(self,solid:pygame.Rect,friction:float,absobtion:float,hardness:float):
        self.solids.append(solid)