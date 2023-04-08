import pygame
import pygame.locals
from Context import Context

if __name__ == '__main__':

    pygame.init()
    infoObject = pygame.display.Info()
    screen = pygame.display.set_mode((infoObject.current_w, infoObject.current_h - 60))
    screen.fill((0,0,0))
    clock = pygame.time.Clock()
    running = True
    c = 0
    context = Context()
    while running:
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                context._handle_click_event(event)

        # fill the screen with a color to wipe away anything from last frame
        screen.fill(pygame.Color(240,231,231))
        

        # RENDER YOUR GAME HERE


        #Right information pannel
        right_pannel_width = infoObject.current_w /4 
        pygame.draw.rect(screen, pygame.Color(253,166,0), pygame.Rect(infoObject.current_w - right_pannel_width, 0, right_pannel_width, infoObject.current_h))

        #Left information pannel
        left_pannel_width = infoObject.current_w /4 * 3
        pygame.draw.rect(screen, pygame.Color(193,168,14), pygame.Rect(0, 0, left_pannel_width, infoObject.current_h))

        #TOP Status Bar
        pygame.draw.rect(screen, pygame.Color(69,24,4), pygame.Rect(0,0,infoObject.current_w, 100), border_bottom_left_radius=25, border_bottom_right_radius=25)





        # flip() the display to put your work on screen
        pygame.display.flip()
        
        clock.tick(60)  # limits FPS to 60

    pygame.quit()