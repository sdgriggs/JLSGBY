
import math

import crops as crops


class Context:
    # Resource Counters
    food = 0

    #......
    # probably some crop names here
    #......


    # Timing Constants
    tick = .1
    ticksPerMinute = 2
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


   
    current_env = {'temp': 0, 'pressure': 0, 'uv': 'Low', 'sunrise': 540, 'sunset': 1440}

    def get_temp(self):
        return self.current_env['temp']
    
    def get_pressure(self):
        return self.current_env['pressure']
    
    def get_uv(self):
        return self.current_env['uv']
    
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