import crops as crops

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

    # define crop type objects. store as a list for easy iteration
    crops = [
        crops.generic(),
        crops.coldResistant(),
        crops.uvResistant(),
        crops.hybrid(),
        crops.cashcow()
    ]

    # define plant names
    cropNames = []

    for cropType in crops:
        cropNames.append(cropType.name)

    def _handle_click_event(self, event, mouse):
        #for region in self.click_regions:
        #    if 
        pass

    def init_click_regions(self):
        self.click_regions = []

    def append_click_region(self, x, y, width, height, str):
        self.click_regions.append({'x':x, 'y':y, 'width':width, 'height':height, 'desc': str})