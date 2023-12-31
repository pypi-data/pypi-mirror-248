import pygame

pygame.init()


# screen, xy, radius, vel, color, lightingradius,lightingalpha
class ParticleCircle:
    def __init__(self, screen, gravity: int, resistance):
        self.screen = screen
        self.particles = []
        self.g = gravity
        self.r = resistance

    def AddParticle(self, xy, radius, velocity, color, light_radius, light_alpha, right):
        self.particles.append([xy, radius, velocity, color, light_radius, light_alpha, right])

    def Draw(self):
        for i in self.particles:
            cy = i[0][1] + self.g - i[2] - self.r
            cvel = i[2] - self.r
            cr = i[1] - self.r
            clr = i[4] - self.r
            if i[6]:
                cx = i[0][0] - (i[2] - i[2] * 2)
            else:
                cx = i[0][0] - i[2]

            if cvel <= 0:
                cvel = 1
            if cr < 1:
                index = self.particles.index(i)
                self.particles.pop(index)
                continue
            '''if i[4] < 5:
                index = self.particles.index(i)
                self.particles.pop(index)
                continue'''
            index = self.particles.index(i)
            self.particles.pop(index)
            # print(i[4])
            circle = pygame.Surface((i[4] * 2, i[4] * 2), pygame.SRCALPHA)
            pygame.draw.circle(circle, (i[3][0], i[3][1], i[3][2], i[5]), (i[4], i[4]), i[4])
            self.screen.blit(circle, (i[0][0] - i[4], i[0][1] - i[4]))
            pygame.draw.circle(self.screen, i[3], (i[0][0], i[0][1]), i[1])
            self.particles.insert(index, [[cx, cy], cr, cvel, i[3], clr, i[5], i[6]])


class ParticleCircleHue:
    def __init__(self, screen, gravity: int, resistance):
        self.screen = screen
        self.particles = []
        self.g = gravity
        self.r = resistance

    def AddParticle(self, xy, radius, velocity, color, light_radius, light_alpha,hue,hue_radius,hue_alpha,right):
        self.particles.append([xy, radius, velocity, color, light_radius, light_alpha,hue,hue_radius,hue_alpha,right])

    def Draw(self):
        for i in self.particles:
            cy = i[0][1] + self.g - i[2] - self.r
            cvel = i[2] - self.r
            cr = i[1] - self.r
            clr = i[4] - self.r
            chlr = i[7] - self.r
            if i[9]:
                cx = i[0][0] - (i[2] - i[2] * 2)
            else:
                cx = i[0][0] - i[2]

            if cvel <= 0:
                cvel = 1
            if cr < 1:
                index = self.particles.index(i)
                self.particles.pop(index)
                continue
            '''if i[4] < 5:
                index = self.particles.index(i)
                self.particles.pop(index)
                continue'''
            index = self.particles.index(i)
            self.particles.pop(index)
            # print(i[4])
            check = i[4]*2>i[7]*2
            if check:
                circle = pygame.Surface((i[4] * 2, i[4] * 2), pygame.SRCALPHA)
                pygame.draw.circle(circle, (i[6][0], i[6][1], i[6][2], i[5]), (i[4], i[4]), i[7])
                pygame.draw.circle(circle, (i[3][0], i[3][1], i[3][2], i[5]), (i[4], i[4]), i[4])
                self.screen.blit(circle, (i[0][0] - i[4], i[0][1] - i[4]))
            else:
                circle = pygame.Surface((i[7] * 2, i[7] * 2), pygame.SRCALPHA)
                pygame.draw.circle(circle, (i[6][0], i[6][1], i[6][2], i[5]), (i[7], i[7]), i[7])
                pygame.draw.circle(circle, (i[3][0], i[3][1], i[3][2], i[5]), (i[7], i[7]), i[4])
                self.screen.blit(circle, (i[0][0] - i[7], i[0][1] - i[7]))
            pygame.draw.circle(self.screen, i[3], (i[0][0], i[0][1]), i[1])
            self.particles.insert(index, [[cx, cy], cr, cvel, i[3], clr, i[5], i[6],chlr,i[8],i[9]])


class ParticleSquare:
    def __init__(self, screen, gravity: int, resistance):
        self.screen = screen
        self.particles = []
        self.g = gravity
        self.r = resistance

    def AddParticle(self, xy, side, velocity, color, light_side, light_alpha, right):
        self.particles.append([xy, side, velocity, color, light_side, light_alpha, right])

    def Draw(self):
        for i in self.particles:
            cy = i[0][1] + self.g - i[2] - self.r
            cvel = i[2] - self.r
            cr = i[1] - self.r
            clr = i[4] - self.r
            if i[6]:
                cx = i[0][0] - (i[2] - i[2] * 2)
            else:
                cx = i[0][0] - i[2]

            if cvel <= 0:
                cvel = 1
            if cr < 1:
                index = self.particles.index(i)
                self.particles.pop(index)
                continue
            '''if i[4] < 5:
                continue'''
            index = self.particles.index(i)
            self.particles.pop(index)
            # print(i[4])
            square = pygame.Surface((i[4], i[4]), pygame.SRCALPHA)
            rect = pygame.Rect(0,0,i[4],i[4])
            pygame.draw.rect(square, (i[3][0], i[3][1], i[3][2],i[5]),rect)
            self.screen.blit(square, (i[0][0], i[0][1]))
            x = i[0][0] + i[4] / 2
            y = i[0][1] + i[4] / 2
            rect = pygame.Rect(x, y, i[1], i[1])
            rect.center = (x,y)
            pygame.draw.rect(self.screen, (i[3][0],i[3][1],i[3][2]), rect)
            self.particles.insert(index, [[cx, cy], cr, cvel, i[3], clr, i[5], i[6]])
