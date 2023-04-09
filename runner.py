import pygame
import pygame.locals
from Context import Context
import time
import weather_data.soldata


autoIncrement = 0 #(dummy value, will be calculated in increment function)

def autominer():
    global autoIncrement
    # calculate the number to increment by based off number of crops, conditions, etc.

    time.sleep(Context.tick)
    context.doTickUpdate()

def drawText(text, textColor, bgColor, x, y, fsize):
    font = pygame.font.SysFont('Rockwell', fsize)
    text = font.render(text, True, textColor, bgColor)
    textRect = text.get_rect()
    textRect.topleft = (x, y)
    screen.blit(text, textRect)

def drawGraph(title, x, y, width, height, color, data, screen):
    pygame.draw.rect(screen, pygame.Color(255,255,255),pygame.Rect(x, y, width, height))
    drawText(title, color, pygame.Color(255,255,255), x + 20, y + 5, 20)
    pygame.draw.rect(screen, color, pygame.Rect(x+5, y+5, 3, height - 10))
    pygame.draw.rect(screen, color, pygame.Rect(x+3, y + height - 18, width - 10, 3))
    points = []
    max_val = -9999999999
    min_val = 9999999999
    for d in data:
        if d > max_val:
            max_val = d
        if d < min_val:
            min_val = d
    x_start = x+5
    y_start = y + 40
    x_end = x_start + width - 10
    y_end = y_start + height - 58
    for i in range(0, len(data)):
        d = data[i]
        points.append((x_start + (x_end - x_start ) / len(data) * (i+1), y_end -
                        (y_end - y_start)*(d - min_val)/(max_val - min_val)  ))
    pygame.draw.lines(screen, color, False, points, 2)

    


 
if __name__ == '__main__':

    pygame.init()
    infoObject = pygame.display.Info()
    screen = pygame.display.set_mode((infoObject.current_w, infoObject.current_h - 60))
    screen.fill((255,0,255))
    pygame.display.set_caption("Marmer")
    clock = pygame.time.Clock()
    running = True



    screen.fill((0,0,0))
    clock = pygame.time.Clock()
    running = True
    c = 0
    smallfont = pygame.font.SysFont('Rockwell',35)

    context = Context()
    this_sol_data = {}

    while running:

        autominer()

        # Update clock

        context.next_tick()



        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                context._handle_click_event(event, pygame.mouse.get_pos())
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
        for i in range(0, len(context.crops)):
            b = context.crops[i].name
            text = smallfont.render(b + f"({context.crops[i].quantity})", True, 'black')
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

        pygame.draw.rect(screen, "brown", pygame.Rect(0,0,infoObject.current_w, 100))

        #drawText("you have " + str(f'{Context.food:.2f}') + " food", Context.black, Context.white, 500, 300, 20)
        #drawText(timeString, Context.black, Context.white, 500, 400, 20)


        #TOP Status Bar
        bgc = pygame.Color(69,24,4)
        pygame.draw.rect(screen, pygame.Color(69,24,4), pygame.Rect(0,0,infoObject.current_w, 100), border_bottom_left_radius=25, border_bottom_right_radius=25)


        drawGraph("High Temps", 1168,120,350,200, pygame.Color(0,0,0), context.highs, screen)

        drawText("Avaliable Food: " + str(f'{context.food:.2f}') + " units", Context.white, bgc, 850, 15, 20)
        drawText(f"Current Air Temp: {context.get_temp():.2f} °C", Context.white, bgc, 500, 65, 20)
        drawText(f"Current Air Pressure: {context.get_pressure():.2f} Pa", Context.white, bgc, 500, 15, 20)
        drawText(f"Current UV index: {context.get_uv()} ", Context.white, bgc, 850, 65, 20)
        drawText(f"Sunrise: {context.get_sunrise()}", Context.white, bgc, 300, 15, 20)
        drawText(f"Sunset: {context.get_sunset()}", Context.white, bgc, 300, 65, 20)
        drawText(context.get_time_string(), Context.white, bgc, 25, 40, 20)





        # flip() the display to put your work on screen
        pygame.display.flip()

        
        clock.tick(60)  # limits FPS to 60

    pygame.quit()