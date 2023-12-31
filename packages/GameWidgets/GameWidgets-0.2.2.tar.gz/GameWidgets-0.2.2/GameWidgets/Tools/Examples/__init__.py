def ParticleExCode():
    print("""
-------------ParticleExample code: ---------------


# import all required files.
import pygame
from random import randint
from GameWidgets.Engine.ParticleEffect import ParticleCircle

pygame.init()
# Start up the Window
res = (400, 400)
window = pygame.display.set_mode(res)
# set up clock
clock = pygame.time.Clock()
# Gravity
g = 8
# Create Particle class, you can make multiple with one object.
p = ParticleCircle(window, g, 0.5)
# Run var and main loop
run = True
while run:
    # get mouse pos out of tuple format
    mx = pygame.mouse.get_pos()[0]
    my = pygame.mouse.get_pos()[1]
    # Fill the window
    window.fill((0, 0, 0))
    # Set fps
    clock.tick(30)
    # Decide whether to make the particle move right or left by changing the last argument
    if randint(0, 1) == 0:
        r = randint(10, 20)
        p.AddParticle([mx, my], r, randint(-10,10),
                      (randint(100, 255), randint(100, 255), randint(100, 255)), r+3, 180, False)
    else:
        r = randint(10, 20)
        p.AddParticle([mx, my], r, randint(-10,10),
                      (randint(100, 255), randint(100, 255), randint(100, 255)), r+3, 180, True)
    # Drawing and updating the particles.
    p.Draw()
    # Hiding the mouse for effect
    pygame.mouse.set_visible(False)
    #pygame.mouse.set_cursor(*pygame.cursors.arrow)
    # Standard eventloop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # Update screen
    pygame.display.flip()
# quit if required.
pygame.quit()
#(randint(100, 255), randint(100, 255), randint(100, 255))""")
