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
    return textRect

def drawGraph(title, x, y, width, height, color1, color2, data1, data2, screen, text_tag):
    if not len(data1) == len(data2):
        raise Exception("UGA BOOGA")
    
    pygame.draw.rect(screen, pygame.Color(225,225,245),pygame.Rect(x, y, width, height))
    drawText(title, pygame.Color(0,0,0), None, x + 20, y + 5, 20)
    pygame.draw.rect(screen, pygame.Color(0,0,0), pygame.Rect(x+5, y+5, 3, height - 10))
    pygame.draw.rect(screen, pygame.Color(0,0,0), pygame.Rect(x+3, y + height - 18, width - 10, 3))
    if(len(data1) < 2 or len(data2) < 2):
        return
    points1 = []
    points2 = []
    max_val = data1[0]
    min_val = data1[0]
    for d in data1:
        if d > max_val:
            max_val = d
        if d < min_val:
            min_val = d
    for d in data2:
        if d > max_val:
            max_val = d
        if d < min_val:
            min_val = d

    x_start = x+5
    y_start = y + 40
    x_end = x_start + width - 10
    y_end = y_start + height - 58
    drawText(str(max_val) + text_tag,pygame.Color(0,0,0), None, x + 12, y + 37, 10)
    drawText(str(min_val) + text_tag,pygame.Color(0,0,0), None, x + 12, y_end - 13, 10)    
    for i in range(0, len(data1)):
        d1 = data1[i]
        d2 = data2[i]
        divisor = (max_val - min_val)
        divisor = divisor if divisor > 0 else 1
        points1.append((x_start + (x_end - x_start ) / len(data1) * (i+1), y_end -
                        (y_end - y_start)*(d1 - min_val)/ divisor ))
        points2.append((x_start + (x_end - x_start ) / len(data1) * (i+1), y_end -
                        (y_end - y_start)*(d2 - min_val)/divisor  ))

    pygame.draw.lines(screen, color1, False, points1, 2)
    pygame.draw.lines(screen, color2, False, points2, 2)

    
def drawUVGraph(title, x, y, width, height, color1, data1, screen):

    
    pygame.draw.rect(screen, pygame.Color(225,225,245),pygame.Rect(x, y, width, height))
    drawText(title, pygame.Color(0,0,0), None, x + 20, y + 5, 20)
    pygame.draw.rect(screen, pygame.Color(0,0,0), pygame.Rect(x+5, y+5, 3, height - 10))
    pygame.draw.rect(screen, pygame.Color(0,0,0), pygame.Rect(x+3, y + height - 18, width - 10, 3))
    if(len(data1) < 2):
        return
    points1 = []
    
    max_val = data1[0]
    min_val = data1[0]
    for d in data1:
        if d > max_val:
            max_val = d
        if d < min_val:
            min_val = d
    x_start = x+5
    y_start = y + 40
    x_end = x_start + width - 10
    y_end = y_start + height - 58
    drawText("Very High",pygame.Color(0,0,0), None, x + 12, y + 37, 10)
    drawText("Low",pygame.Color(0,0,0), None, x + 12, y_end - 13, 10)  
    for i in range(0, len(data1)):
        d1 = data1[i]
        divisor = 4
        points1.append((x_start + (x_end - x_start ) / len(data1) * (i+1), y_end -
                        (y_end - y_start)*d1/ divisor ))
        

    pygame.draw.lines(screen, color1, False, points1, 2)


 
if __name__ == '__main__':

    pygame.init()
    infoObject = pygame.display.Info()
    screen = pygame.display.set_mode((infoObject.current_w, infoObject.current_h - 60))
    pygame.display.set_caption("Marmer")

    screen.fill((0,0,0))
    clock = pygame.time.Clock()
    running = True
    smallfont = pygame.font.SysFont('Rockwell',35)

    context = Context()

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


        #Left information pannel
        left_pannel_width = infoObject.current_w /4 * 3
        #pygame.draw.rect(screen, pygame.Color(193,168,14), pygame.Rect(0, 0, left_pannel_width, infoObject.current_h))
        img = pygame.image.load("assets\\gauthier-bassee-curiosity-image-site-22.png").convert()
        img_rect = img.get_rect()

        screen.blit(img, img_rect)


        

        #Right information pannel
        right_pannel_width = infoObject.current_w /4 
        pygame.draw.rect(screen, pygame.Color(253,166,0), pygame.Rect(infoObject.current_w - right_pannel_width, 0, right_pannel_width, infoObject.current_h))

        #Allocate the areas where clicks are valid
        context.init_click_regions()

        # Make our toggle buttons
        img = pygame.image.load("assets\\ice-cream.png").convert_alpha()

        img = pygame.transform.scale(img, (200,300))
        img_rect = img.get_rect()
        img_rect.topleft = ((infoObject.current_w / 4 * 3 - 220 , infoObject.current_h - 380))
        screen.blit(img, img_rect)
        context.append_click_region(img_rect.x, img_rect.y, img_rect.width, img_rect.height, "click")

        # Plant Portfolio Button
        pbRect = drawText("  Plant Portfolio  ", 'black', 'white', infoObject.current_w - right_pannel_width + 20, 110, 20)
        context.append_click_region(pbRect.x, pbRect.y, pbRect.width, pbRect.height, "switch-portfolio")

        # Graphs Button
        pbRect = drawText("  Stats and Trends ", 'black', 'white', infoObject.current_w - right_pannel_width / 2 + 10, 110, 20)
        context.append_click_region(pbRect.x, pbRect.y, pbRect.width, pbRect.height, "switch-graphs")

        if context.portfolioMode:
            for i in range(0, len(context.crops)):
                b = context.crops[i].name
                rect = drawText(b, 'white', None, infoObject.current_w - right_pannel_width + 25, 125 * (i+1) + 20, 25)
                quanRect = drawText(f"Quantity Owned: {context.crops[i].quantity}", 'white', None, infoObject.current_w - right_pannel_width + 25, 125 * (i+1) + 50, 15)
                costRect = drawText(f"Cost: {context.crops[i].buyValue} units", 'white', None, infoObject.current_w - right_pannel_width + 25, 125 * (i+1) + 65, 15)
                tempRect = drawText(f"Minimum Temperature: {context.crops[i].minGoodTemp}C", 'white', None, infoObject.current_w - right_pannel_width + 25, 125 * (i+1) + 80, 15)
                uvRect = drawText(context.crops[i].getUvTolerance(), 'white', None, infoObject.current_w - right_pannel_width + 25, 125 * (i+1) + 95, 15)
                fphRect = drawText(f'Food per Hour: {context.crops[i].foodPerHourPerPlant} units', 'white', None, infoObject.current_w - right_pannel_width + 25, 125 * (i+1) + 110, 15)

                buyRect = drawText("    Buy    ", 'black', 'green', infoObject.current_w - 100,  125 * (i+1) + 50, 20)
                context.append_click_region(buyRect.x, buyRect.y, buyRect.width, buyRect.height, "buy-" + b)

                sellRect = drawText("    Sell    ", 'black', 'red', infoObject.current_w - 100,  125 * (i+1) + 80, 20)
                context.append_click_region(sellRect.x, sellRect.y, sellRect.width, sellRect.height, "sell-" + b)


        else:

            graph_x = infoObject.current_w / 4 * 3 + 7
            drawGraph("Temps", graph_x,140,350,200, pygame.Color(255,0,0), pygame.Color(0,0,255), context.highs, context.lows, screen, " °C")
            drawGraph("Pressure", graph_x ,360,350,200, pygame.Color(0,255,0), pygame.Color(0,255,0), context.pressure, context.pressure, screen, " Pa")
            drawUVGraph("UV Index", graph_x,580,350,200, pygame.Color(191,64,191), context.uv, screen)


        # Discern good coords and dead zone
        context.win_x1 = 0
        context.win_x2 = infoObject.current_w - right_pannel_width
        context.win_y1 = 100
        context.win_y2 = infoObject.current_h

        context.dead_x1 = img_rect.topleft[0]
        context.dead_x2 = context.dead_x1 + img_rect.width
        context.dead_y1 = img_rect.topleft[1]
        context.dead_y2 = context.dead_y1 + img_rect.height



        pygame.draw.rect(screen, "brown", pygame.Rect(0,0,infoObject.current_w, 100))

        #pygame.draw.rect(screen, "white", pygame.Rect(infoObject.current_w / 2 - 200,infoObject.current_h / 2 - 100, 200, 200))


        #TOP Status Bar
        bgc = pygame.Color(69,24,4)


        pygame.draw.rect(screen, pygame.Color(69,24,4), pygame.Rect(0,0,infoObject.current_w, 100))


        drawText("Avaliable Food: " + str(f'{context.food:.2f}') + " units", Context.white, bgc, 850, 15, 20)
        drawText(f"Current Air Temp: {context.get_temp():.2f} °C", Context.white, bgc, 500, 65, 20)
        drawText(f"Current Air Pressure: {context.get_pressure():.2f} Pa", Context.white, bgc, 500, 15, 20)
        drawText(f"Current UV index: {context.get_uv()} ", Context.white, bgc, 850, 65, 20)
        drawText(f"Sunrise: {context.get_sunrise()}", Context.white, bgc, 300, 15, 20)
        drawText(f"Sunset: {context.get_sunset()}", Context.white, bgc, 300, 65, 20)
        drawText(context.get_time_string(), Context.white, bgc, 25, 40, 20)



        # Draw the plants!
        for crop in context.crops:
            for coords in crop.spriteCoords:
                img = pygame.image.load(crop.spriteFile).convert_alpha()
                img_rect = img.get_rect()
                img_rect.centerx = coords[0]
                img_rect.centery = coords[1]
                screen.blit(img, img_rect)
    


        # flip() the display to put your work on screen
        pygame.display.flip()

        
        clock.tick(60)  # limits FPS to 60

    pygame.quit()