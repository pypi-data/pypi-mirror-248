import pygame
import time

pygame.init()


class Entity:
    def __init__(self, screen):
        self.screen = screen
        self.stime = 0
        self.ctime = 0
        self.animationStart = False
        self.xyanituple = 0
        self.animations = {}
        self.frame = 0
        self.lastframe = None

    def CreateAnimation(self, frames: tuple, name: str, size: tuple):
        items = []
        for i in frames:
            img = pygame.image.load(i)
            img = pygame.transform.scale(img,size)
            items.append(img)
        self.animations[name] = items
        print(self.animations)

    def StartAnimation(self):
        self.animationStart = True
        self.stime = time.time()

    def Animate(self, Speed: int,name:str):
        if self.animationStart:
            self.ctime = time.time()
            if self.ctime - self.stime >=Speed:
                for key in self.animations:
                    if key == name:
                        try:
                            self.frame += 1
                            test = self.animations[key][self.frame]
                        except:
                            self.frame = 0

                self.stime = time.time()
                #self.screen.blit(self.lastframe[self.frame], self.xyanituple)

    def Draw(self, name:str, pos):
        self.screen.blit(self.animations[name][self.frame], pos)



