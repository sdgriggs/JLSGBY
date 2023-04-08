import pygame
import pygame.locals
import time

# GLOBAL VARIABLES

# Resource Counters
food = 0
autoIncrement = .1
#......
# probably some crop names here
#......


# Timing Constants
tick = .1
ticksPerMinute = 2
ticksPerHour = 120
ticksPerSol = 2880

minPerHour = 60
hourPerSol = 24
solPerYear = 668

minuteIncrement = 10

# defining colors

white = (255, 255, 255)
black = (0, 0, 0)

# resource - by - hour functions
def getTempAtHour(hour):
    return 0

def autominer():
    global food
    global autoIncrement

    # calculate the number to increment by based off number of crops, conditions, etc.

    time.sleep(tick)
    food = food + autoIncrement

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

    while running:

        autominer()

        # Update clock

        tickCounter += 1
        if tickCounter == ticksPerMinute:
            tickCounter = 0
            minNum += 1

        if minNum == minPerHour:
            minNum = 0
            hourNum += 1

        if hourNum == hourPerSol:
            hourNum = 0
            solNum += 1

        if solNum == solPerYear:
            solNum = 1
            yearNum += 1

        timeString = f"Year {yearNum}, Sol {solNum}        {str(hourNum).zfill(2)}:{str(minNum - minNum % minuteIncrement).zfill(2)}"

        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # fill the screen with a color to wipe away anything from last frame
        screen.fill("orange")
        

        # RENDER YOUR GAME HERE
        pygame.draw.rect(screen, "brown", pygame.Rect(0,0,infoObject.current_w, 100))

        drawText("you have " + str(f'{food:.2f}') + " food", black, white, 100, 50, 20)
        drawText(timeString, black, white, 100, 100, 20)

        # flip() the display to put your work on screen
        pygame.display.flip()

        
        clock.tick(60)  # limits FPS to 60

    pygame.quit()