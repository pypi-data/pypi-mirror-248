import pygame
import time


class Shade:
    def __init__(self, screen, color: tuple = (0, 0, 0), i_alpha: int = 20, res: tuple = (500, 500),interval:int = 0.1):
        self.screen = screen
        self.color = (color[0], color[1], color[2], 0)
        self.i = i_alpha
        self.surf = pygame.Surface(res, pygame.SRCALPHA)
        self.res = res
        self.start = False
        self.stime = 0
        self.ctime = 0
        self.interval = interval

    def Draw(self):
        pygame.draw.rect(self.surf, self.color, pygame.Rect(0,0, self.res[0], self.res[1]))
        self.screen.blit(self.surf, (0, 0))

    def Start(self):
        self.start = True
        self.stime = time.time()

    def Update(self):
        if self.start:
            self.ctime = time.time()
            if self.ctime - self.stime >= self.interval:
                c_alpha = self.color[3] + self.i
                if c_alpha >= 255:
                    return False
                else:
                    self.color = (self.color[0], self.color[1], self.color[2], c_alpha)
                    self.stime = time.time()
                    #print(self.color)
                    return True
