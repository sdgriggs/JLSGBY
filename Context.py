import math
import weather_data.soldata as soldata
import random
import Plant
import GameInfo

from enum import Enum
 
class GameState(Enum):
    TITLE = 1
    HELP  = 2
    GAME  = 3

class Context:
    #constants
    # Maximum number of days that history is kept for
    MAX_HISTORY = 30

    #mapping for uv
    UV_MAPPING = {'Very_High': 4, 'High': 3, 'Moderate': 2, 'Low':1}

    PEOPLE_THRESH = 15000

    ADTL_PERSON_THRESH = 500

    DAILY_FOOD_INTAKE_PER_PERSON = 10


    # defining colors
    white = (255, 255, 255)
    black = (0, 0, 0)



    #instance variable
    def __init__(self):
        self.gameState = GameState.TITLE

        self.first_person = "Insufficent-Food"
    # Resource Counters
        self.food = 0
        self.totalfood = self.food
        self.population = 0
        self.gainedFood = 0
        self.consumedFood = 0
        self.totalConsumedFood = self.consumedFood

        # define click regions
        self.click_regions = []

        # define last 30 days of highs/lows/pressure/uv
        self.highs = []
        self.lows =  []
        self.pressure = []
        self.uv = []


        # define the crop window
        self.win_x1 = 0
        self.win_x2 = 0
        self.win_y1 = 0
        self.win_y2 = 0
        # define the clicking deadzone
        self.dead_x1 = 0
        self.dead_x2 = 0
        self.dead_y1 = 0
        self.dead_y2 = 0

            # define crop type objects. store as a list for easy iteration
        self.crp = [
            Plant.Generic(),    
            Plant.ColdResistant(),
            Plant.UVResistant(),
            Plant.Hybrid(),
            Plant.CashCow()
        ]

        self.crops = []
        self.cropDict = {}

        for crop in self.crp:
            self.cropDict.update({crop.name: crop})


        self.sol_data = soldata.getAggregatedSolData()

        #as long as we start after 1 prevTemp can be any placeholder value
        self.prevTemp = 1
        self.current_env = soldata.getRandomizedSolData(0, self.sol_data)

        self.tickCounter = 0
        self.yearNum = 1
        self.solNum = 1

        self.hourNum = 8
        #min as in minutes
        self.minNum = 0

        self.answer = 'Not-asked'

        self.reset = False

        # controls toggle gui
        self.portfolioMode = True

        self.sold_plants = True
        self.bought_plants = True


        # plant sprites and stuff
        self.coords = []

        self.new_plants = 0
        

    def update_crops(self):
            self.crops = []
            for c in self.crp:
                if c.thresh <= self.totalfood or self.reset:
                    self.crops.append(c)

    def update_people(self):
        
        availableFood = self.totalfood - self.totalConsumedFood - self.PEOPLE_THRESH

        if availableFood >= 0:
            self.population = round((availableFood)/self.ADTL_PERSON_THRESH)
            
            if self.first_person == "Shown":
                return
            elif self.first_person == "Insufficent-Food" and self.population >= 1:
                self.first_person = "To-Show"
                
        elif self.population > 0:
            self.population = 0
            
            
    
    
    def next_tick(self):
        self.foodTickUpdate()
        self.update_crops()
        self.update_people()
        self.tickCounter += 1

        if self.tickCounter >= GameInfo.TICKS_PER_MINUTE:
            self.tickCounter = 0
            self.minNum += 1

        if self.minNum >= GameInfo.MIN_PER_HOUR:
            self.minNum = 0
            self.hourNum += 1

        if self.hourNum >= GameInfo.HOUR_PER_SOL:
            self.hourNum = 0
            self.increment_sol()

    def get_temp(self, minutes = None):
        min_temp = self.current_env['min_temp']
        max_temp = self.current_env['max_temp']
        if minutes == None:
            minutes = self.minNum + self.hourNum * 60
        minutesInSol = GameInfo.MIN_PER_HOUR * GameInfo.HOUR_PER_SOL
        temp_range = max_temp - min_temp


        linearthreshold = 90
        #if we're less than the linear threshold in we'll do a linear approximation
        #in the hopes we can somewhat smoothly catch up or wait for the sinusoidal approximation
        #when switching between days
        if minutes < linearthreshold:
            cosapprox = min_temp + .5 * temp_range + .5 * temp_range * math.cos((linearthreshold + self.current_env['sunrise'] + 60) * 2 * math.pi / minutesInSol)
            m = (cosapprox - self.prevTemp) / linearthreshold
            b = self.prevTemp
            return m * minutes + b
        #if we're an hour in we'll do a sinusoidal approximation
        return min_temp + .5 * temp_range + .5 * temp_range * math.cos((minutes + self.current_env['sunrise'] + 60) * 2 * math.pi / minutesInSol)
    
    def get_pressure(self):
        return self.current_env['pressure']
    
    def get_uv(self):
        timeInMinutes = GameInfo.MIN_PER_HOUR * self.hourNum + self.minNum
        if  timeInMinutes < self.current_env['sunrise'] or timeInMinutes > self.current_env['sunset']:
            return "Low"
        return self.current_env['uv_index']
    
    def get_sunrise(self):
        return self._format_time(self.current_env['sunrise'])
         
    
    def get_sunset(self):
        return self._format_time(self.current_env['sunset'])
    
    def get_production(self):
        return self.gainedFood * GameInfo.TICKS_PER_HOUR
    
    def get_consumption(self):
        return self.consumedFood * GameInfo.TICKS_PER_HOUR
    
    def get_net(self):
        return self.get_production() - self.get_consumption()

    def _format_time(self, min_since_midnight):
        hr = str(math.floor(min_since_midnight / 60))
        mins = str(math.floor(min_since_midnight % 60))
        if len(hr) < 2:
            hr = '0' + hr
        if len(mins) < 2:
            mins = '0' + mins
        return hr + ":" + mins
    
    def foodTickUpdate(self):
        self.gainedFood = 0
        self.consumedFood = self.population * Context.DAILY_FOOD_INTAKE_PER_PERSON / GameInfo.TICKS_PER_SOL * 100
        for crop in self.crops:

            self.gainedFood += crop.getFoodPerTick(self.get_temp(), self.get_uv())

        netFood = self.gainedFood - self.consumedFood
        self.food += netFood
        self.totalConsumedFood -= self.consumedFood
        self.totalfood += self.gainedFood

    def _handle_click_event(self, event, mouse):
        
        self.new_plants = 0
        for region in self.click_regions:
            
            if region['x'] <= mouse[0] <= region['x'] + region['width'] and region['y'] <= mouse[1] <= region['y'] + region['height']:

                command = region['desc'].split('-')
               
                if command[0] == "sell":
                    crop = self.cropDict[command[1]]
                    if crop.sellPlant():
                        self.food += crop.sellValue
                        self.totalfood += crop.sellValue
                    self.sold_plants = True
                    

                elif command[0] == "buy":
                    crop = self.cropDict[command[1]]
                    if self.food >= crop.buyValue:
                        crop.addPlant(self.win_x1, self.win_y1, self.win_x2, self.win_y2, self.dead_x1, self.dead_y1, self.dead_x2, self.dead_y2)
                        self.food -= crop.buyValue
                        
                    self.bought_plants = True

                elif command[0]  == "click":
                    
                    self.food += 1
                    self.totalfood += 1

                elif command[0] == "switch":
                    if command[1] == "portfolio":
                        self.portfolioMode = True
                    else:
                        self.portfolioMode = False

                elif command[0] == "exit":
                    self.first_person = "Shown"
                
                elif command[0] == 'stay':
                    self.answer = 'stay'

                elif command[0] == 'leave':
                    self.answer = 'leave'
                    self.reset = True
                    self.population = 0
                    self.totalfood = 0
                    for crop in self.crops:
                        while crop.sellPlant():
                            pass
                    self.food = 0
                    self.first_person = "Insufficent-Food"
                    self.answer = "Not-asked"
              

    def init_click_regions(self):
        self.click_regions = []

    def append_click_region(self, x, y, width, height, str):
        self.click_regions.append({'x':x, 'y':y, 'width':width, 'height':height, 'desc': str})
    
    def increment_sol(self):
        
        self.consumedFood += self.population * 3
        self.food -= self.consumedFood

        self.solNum += 1
        if self.solNum > GameInfo.SOL_PER_YEAR:
            self.solNum = 1
            self.yearNum += 1
        
        self.highs.append(self.current_env['max_temp'])
        while len(self.highs) > Context.MAX_HISTORY:
            self.highs = self.highs[1:]
        
        self.lows.append(self.current_env['min_temp'])
        while len(self.lows) > Context.MAX_HISTORY:
            self.lows = self.lows[1:]


        self.pressure.append(self.current_env['pressure'])
        while len(self.pressure) > Context.MAX_HISTORY:
            self.pressure = self.pressure[1:]

        self.uv.append(Context.UV_MAPPING[self.current_env['uv_index']])
        while len(self.uv) > Context.MAX_HISTORY:
            self.uv = self.uv[1:]

        #we use a custom minute such that we save the previous value
        self.prevTemp = self.get_temp(minutes = 23 * 60 + 59)
        #and now we update current_env
        self.current_env = soldata.getRandomizedSolData(self.solNum - 1, self.sol_data)
    
    def get_time_string(self):
        return f"Year {self.yearNum}, Sol {self.solNum}        {str(self.hourNum).zfill(2)}:{str(self.minNum - self.minNum % GameInfo.MINUTE_INCREMENT).zfill(2)}"


