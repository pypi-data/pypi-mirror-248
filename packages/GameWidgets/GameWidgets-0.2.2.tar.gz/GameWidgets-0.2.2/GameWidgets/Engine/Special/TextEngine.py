import pygame
pygame.init()
class PreCompTextEngine:
    def __init__(self,screen,characters:list,fontfile:str,charWidth:int,charHeight:int):
        self.screen = screen
        self.character = characters
        self.fontfile = fontfile
        self.characterWidth = charWidth
        self.characterHeight = charHeight
        self.font = pygame.image.load(self.fontfile)
        self.imgcharacters = []
        x = 0
        for i in range(len(self.character)):
            self.imgcharacters.append(pygame.Surface.subsurface(self.font,((x,0),(self.characterWidth,self.characterHeight))))
            x += self.characterWidth
        print(self.imgcharacters)
    
    def Print(self,text:str,x,y):
        text = text.split()
        for i in range(len(text)):
            pass