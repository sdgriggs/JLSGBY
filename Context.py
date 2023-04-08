class Context:
    # Resource Counters
    food = 0

    #......
    # probably some crop names here
    #......


    # Timing Constants
    tick = .1
    ticksPerMinute = 20
    ticksPerHour = 120
    ticksPerDay = 2880
    minuteIncrement = 10

    minPerHour = 60
    hourPerSol = 24
    solPerYear = 668   

    # defining colors

    white = (255, 255, 255)
    black = (0, 0, 0)


    # define click regions
    click_regions = []

    # define plants
    plants = ["Plant 1",
              "A PLANT WITH A SUPER LONG NAME 2",
              "Plant 3",]
    

    temp = -18

    pressure = 800

    uv = "Medium"

    sunrise = '08:25'

    sunset = '22:19'


    def _handle_click_event(self, event, mouse):
        for region in self.click_regions:
            #print(region['desc'])
            #print(region['x'] <= mouse[0] <= region['x'] + region['width'])
            #print(region['y'] <= mouse[0] <= region['y'] + region['height'])
            if region['x'] <= mouse[0] <= region['x'] + region['width'] and region['y'] <= mouse[1] <= region['y'] + region['height']:
                print(region['desc'])

    def init_click_regions(self):
        self.click_regions = []

    def append_click_region(self, x, y, width, height, str):
        self.click_regions.append({'x':x, 'y':y, 'width':width, 'height':height, 'desc': str})