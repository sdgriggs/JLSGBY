import pygame
import pygame.locals

if __name__ == '__main__':

    pygame.init()
    infoObject = pygame.display.Info()
    screen = pygame.display.set_mode((infoObject.current_w, infoObject.current_h - 60))
    screen.fill((255,0,255))
    clock = pygame.time.Clock()
    running = True
    c = 0
    while running:
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # fill the screen with a color to wipe away anything from last frame
        screen.fill("orange")
        

        # RENDER YOUR GAME HERE
        pygame.draw.rect(screen, "brown", pygame.Rect(0,0,infoObject.current_w, 100))
        # flip() the display to put your work on screen
        pygame.display.flip()
        
        clock.tick(60)  # limits FPS to 60

    pygame.quit()