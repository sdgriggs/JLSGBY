class Context:
    # Resource Counters
    food = 0
    autoIncrement = .1 #(dummy value, will be calculated in increment function)
    #......
    # probably some crop names here
    #......


    # Timing Constants
    tick = .1
    ticksPerMinute = 20
    ticksPerHour = 120
    ticksPerDay = 2880

    # defining colors

    white = (255, 255, 255)
    black = (0, 0, 0)


    # define click regions
    click_regions = []

    # define plants
    plants = ["Plant 1", "A PLANT WITH A SUPER LONG NAME 2", "Plant 3"]


    def _handle_click_event(self, event, mouse):
        for region in self.click_regions:
            if 
        

    def init_click_regions(self):
        self.click_regions = []

    def append_click_region(self, x, y, width, height, str):
        self.click_regions.append({'x':x, 'y':y, 'width':width, 'height':height, 'desc': str})