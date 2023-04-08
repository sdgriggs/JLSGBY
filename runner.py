import pygame
import pygame.locals
from Context import Context
import time


autoIncrement = .1 #(dummy value, will be calculated in increment function)

def autominer():
    global autoIncrement
    # calculate the number to increment by based off number of crops, conditions, etc.

    time.sleep(Context.tick)
    Context.food = Context.food + autoIncrement

def drawText(text, textColor, bgColor, x, y, fsize):
    font = pygame.font.Font('freesansbold.ttf', fsize)
    text = font.render(text, True, textColor, bgColor)
    textRect = text.get_rect()
    textRect.center = (x, y)
    screen.blit(text, textRect)



 
if __name__ == '__main__':

    pygame.init()
    infoObject = pygame.display.Info()
    screen = pygame.display.set_mode((infoObject.current_w, infoObject.current_h - 60))
    screen.fill((255,0,255))
    pygame.display.set_caption("Marmer")
    clock = pygame.time.Clock()
    running = True
    c = 0

    tickCounter = 0
    yearNum = 1
    solNum = 1
    hourNum = 0
    minNum = 0

    screen.fill((0,0,0))
    clock = pygame.time.Clock()
    running = True
    c = 0
    smallfont = pygame.font.SysFont('Corbel',35)

    context = Context()

    while running:

        autominer()

        # Update clock

        tickCounter += 1
        if tickCounter == Context.ticksPerMinute:
            tickCounter = 0
            minNum += 1

        if minNum == Context.minPerHour:
            minNum = 0
            hourNum += 1

        if hourNum == Context.hourPerSol:
            hourNum = 0
            solNum += 1

        if solNum == Context.solPerYear:
            solNum = 1
            yearNum += 1

        timeString = f"Year {yearNum}, Sol {solNum}        {str(hourNum).zfill(2)}:{str(minNum - minNum % Context.minuteIncrement).zfill(2)}"

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
        pygame.draw.rect(screen, "brown", pygame.Rect(0,0,infoObject.current_w, 100))

        drawText("you have " + str(f'{Context.food:.2f}') + " food", Context.black, Context.white, 100, 50, 20)
        drawText(timeString, Context.black, Context.white, 100, 100, 20)



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
            context.append_click_region(rect.x, rect.y, rect.width, rect.height, b  + "-buy")
            rect.x = 50
            rect.width = 50
            pygame.draw.rect(screen, pygame.Color(255, 0, 0), rect, border_radius=25)
            context.append_click_region(rect.x, rect.y, rect.width, rect.height, b  + "-sell")




        #TOP Status Bar
        pygame.draw.rect(screen, pygame.Color(69,24,4), pygame.Rect(0,0,infoObject.current_w, 100), border_bottom_left_radius=25, border_bottom_right_radius=25)





        # flip() the display to put your work on screen
        pygame.display.flip()

        
        clock.tick(60)  # limits FPS to 60

    pygame.quit()