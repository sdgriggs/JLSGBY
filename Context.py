
import math
import weather_data.soldata as soldata
import crops as crops


class Context:
    # Resource Counters
    food = 0

    #......
    # probably some crop names here
    #......


    # Timing Constants
    tick = .1
    ticksPerMinute = 1
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


    sol_data = soldata.getAggregatedSolData()

    current_env = soldata.getRandomizedSolData(0, sol_data)

    tickCounter = 0
    yearNum = 1
    solNum = 1
    hourNum = 0
    minNum = 0

    def next_tick(self):
        self.tickCounter += 1
        if self.tickCounter == Context.ticksPerMinute:
            self.tickCounter = 0
            self.minNum += 1

        if self.minNum == Context.minPerHour:
            self.minNum = 0
            self.hourNum += 1

        if self.hourNum == Context.hourPerSol:
            self.hourNum = 0
            self.increment_sol()






    def get_temp(self):
        if 60 * self.hourNum + self.minNum < self.current_env['sunrise'] or 60 * self.hourNum + self.minNum > self.current_env['sunset']:
            return self.current_env['min_temp']
        return self.current_env['max_temp']
    
    def get_pressure(self):
        return self.current_env['pressure']
    
    def get_uv(self):
        return self.current_env['uv_index']
    
    def get_sunrise(self):
        return self._format_time(self.current_env['sunrise'])
         
    
    def get_sunset(self):
        return self._format_time(self.current_env['sunset'])

    def _format_time(self, min_since_midnight):
        hr = str(math.floor(min_since_midnight / 60))
        min = str(math.floor(min_since_midnight % 60))
        if len(hr) < 2:
            hr = '0' + hr
        if len(min) < 2:
            min = '0' + min
        return hr + ":" + min
    

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
    
    def increment_sol(self):
        
        if self.solNum == Context.solPerYear:
            self.solNum = 1
            self.yearNum += 1
        
        self.current_env = soldata.getRandomizedSolData(self.solNum - 1, self.sol_data)

    def get_time_string(self):
        return f"Year {self.yearNum}, Sol {self.solNum}        {str(self.hourNum).zfill(2)}:{str(self.minNum - self.minNum % Context.minuteIncrement).zfill(2)}"

