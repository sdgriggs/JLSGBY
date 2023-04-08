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
    smallfont = pygame.font.SysFont('Corbel',35)

    context = Context()

    while running:
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                context._handle_click_event(event, pygame.mouse)

        # fill the screen with a color to wipe away anything from last frame
        screen.fill(pygame.Color(240,231,231))
        

        # RENDER YOUR GAME HERE


        #Right information pannel
        right_pannel_width = infoObject.current_w /4 
        pygame.draw.rect(screen, pygame.Color(253,166,0), pygame.Rect(infoObject.current_w - right_pannel_width, 0, right_pannel_width, infoObject.current_h))

        #Left information pannel
        left_pannel_width = infoObject.current_w /4 * 3
        pygame.draw.rect(screen, pygame.Color(193,168,14), pygame.Rect(0, 0, left_pannel_width, infoObject.current_h))
        #Allocate the areas where clicks are valid
        context.init_click_regions()
        for i in range(0, len(context.plants)):
            b = context.plants[i]
            text = smallfont.render(b, True, 'black')
            rect = text.get_rect()
            rect.x = 100
            rect.y = 100 * i + 200
            pygame.draw.rect(screen, pygame.Color(193, 168, 14), rect)
            screen.blit(text, rect)
            rect.x = rect.topright[0]
            rect.width = 50
            pygame.draw.rect(screen, pygame.Color(0, 255, 0), rect, border_radius=25)
            context.append_click_region(rect.x, rect.y, rect.width, rect.heigh, b  + "-buy")
            rect.x = 50
            rect.width = 50
            pygame.draw.rect(screen, pygame.Color(255, 0, 0), rect, border_radius=25)
            context.append_click_region(rect.x, rect.y, rect.width, rect.heigh, b  + "-sell")




        #TOP Status Bar
        pygame.draw.rect(screen, pygame.Color(69,24,4), pygame.Rect(0,0,infoObject.current_w, 100), border_bottom_left_radius=25, border_bottom_right_radius=25)





        # flip() the display to put your work on screen
        pygame.display.flip()
        
        clock.tick(60)  # limits FPS to 60

    pygame.quit()