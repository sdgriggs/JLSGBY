import math
import weather_data.soldata as soldata
import random

from enum import Enum
 
class GameState(Enum):
    TITLE = 1
    HELP  = 2
    GAME  = 3


class Crop:
    def __init__(self):
        self.name = "Parent crop."
        self.quantity = 0           # All start at 0 quantity.
        self.minGoodTemp = 10       # Dummy value.
        self.safeUvLevels = {"Very_High": False, "High": False, "Moderate": False, "Low":False}          # Dummy value.
        self.sellValue = 0              # Dummy value.
        self.buyValue = 0      # Dummy value.
        self.foodPerHourPerPlant = 0        # Dummy value
        self.spriteFile = ""
        self.spriteCoords = []
        self.thresh = 0

    # Increases the number of plants of this crop by one. It is the implementing function's responsibility to check that there are sufficient funds.
    def addPlant(self, x1, y1, x2, y2, dead_x1, dead_y1, dead_x2, dead_y2):
        self.quantity += 1
        # Possibly increase price per plant on purchase?

        coords = [random.randint(x1, x2), random.randint(y1, y2)]

        while dead_x1 <= coords[0] <= dead_x2 and dead_y1 <= coords[1] <= dead_y2:
            coords = [random.randint(x1, x2), random.randint(y1, y2)]

        self.spriteCoords.append(coords)

    # Decreases the number of plants, if possible. Returns true on a success and false on a failure.
    def sellPlant(self):
        if self.quantity >= 1:
            self.quantity -= 1
            self.spriteCoords.pop()
            return True
        else:
            return False
    
    # Returns the total food value generated by this plant per tick.
    def getFoodPerTick(self, temp, uvLevel):
        valuePercent = 1.0

        if temp < self.minGoodTemp:
            valuePercent -= .5
        
        if not self.safeUvLevels[uvLevel]:
            valuePercent -= .5


        return self.quantity * self.foodPerHourPerPlant * valuePercent / Context.ticksPerHour

    
    # Returns a brief string description for the crop.
    def getUvTolerance(self):
        uvTolerance = ""
        if self.safeUvLevels["High"]:
            uvTolerance += "High"
        elif self.safeUvLevels["Moderate"]:
            uvTolerance += "Moderate"
        elif self.safeUvLevels["Low"]:
            uvTolerance += "Low"

        return f"UV Tolerance: {uvTolerance}"
    
class generic(Crop):

    def __init__(self):
        self.name = "Super Tomato"
        self.quantity = 0           # All start at 0 quantity.
        self.minGoodTemp = -50      
        self.safeUvLevels = {"Very_High": False, "High": False, "Moderate": True, "Low":True}     
        self.sellValue = 10              
        self.buyValue = 20     
        self.foodPerHourPerPlant = 5
        self.spriteFile = "assets\\green_plant.png"
        self.spriteCoords = []   
        self.thresh = 0     


class uvResistant(Crop):

    def __init__(self):
        self.name = "Resistant Radishes"
        self.quantity = 0           # All start at 0 quantity.
        self.minGoodTemp = -50      
        self.safeUvLevels = {"Very_High": False, "High": True, "Moderate": True, "Low":True}       
        self.sellValue = 15             
        self.buyValue = 25     
        self.foodPerHourPerPlant = 3.5        
        self.spriteFile = "assets\\red_plant.png"
        self.spriteCoords = []   
        self.thresh = 1000   

class coldResistant(Crop):

    def __init__(self):
        self.name = "Freeze Free Lettuce"
        self.quantity = 0           # All start at 0 quantity.
        self.minGoodTemp = -90      
        self.safeUvLevels = {"Very_High": False, "High": False, "Moderate": True, "Low":True}     
        self.sellValue = 15              
        self.buyValue = 25     
        self.foodPerHourPerPlant = 2
        self.spriteFile = "assets\\blue_plant.png"
        self.spriteCoords = []      
        self.thresh = 500         

class hybrid(Crop):

    def __init__(self):
        self.name = "Uber Tubers"
        self.quantity = 0           # All start at 0 quantity.
        self.minGoodTemp = -30      
        self.safeUvLevels = {"Very_High": False, "High": False, "Moderate": True, "Low":True}      
        self.sellValue = 15              
        self.buyValue = 30     
        self.foodPerHourPerPlant = 6.5 
        self.spriteFile = "assets\\potato.png"
        self.spriteCoords = []   
        self.thresh = 5000       

class cashcow(Crop):

    def __init__(self):

        self.name = "Super Sweet Strawberries"

        self.quantity = 0           # All start at 0 quantity.
        self.minGoodTemp = -10      
        self.safeUvLevels = {"Very_High": False, "High": False, "Moderate": False, "Low":True}     
        self.sellValue = 15              
        self.buyValue = 30     
        self.foodPerHourPerPlant = 25    
        self.spriteFile = "assets\\cash_cow.png"
        self.spriteCoords = [] 
        self.thresh = 10000    

class Context:
    #constants
    # Maximum number of days that history is kept for
    MAX_HISTORY = 30

    #mapping for uv
    UV_MAPPING = {'Very_High': 4, 'High': 3, 'Moderate': 2, 'Low':1}

    PEOPLE_THRESH = 15000

    ADTL_PERSON_THRESH = 500

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
            generic(),    
            coldResistant(),
            uvResistant(),
            hybrid(),
            cashcow()
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


        # plant sprites and stuff
        self.coords = []

    def update_crops(self):
            self.crops = []
            for c in self.crp:
                if c.thresh <= self.totalfood or self.reset:
                    self.crops.append(c)

    def update_people(self):
        
        if self.totalfood >= self.PEOPLE_THRESH:
            self.population = round((self.totalfood - self.PEOPLE_THRESH)/self.ADTL_PERSON_THRESH)
            
            if self.first_person == "Shown":
                return
            elif self.first_person == "Insufficent-Food" and self.population >= 1:
                self.first_person = "To-Show"
            
            
    
    
    def next_tick(self):
        self.doTickUpdate()
        self.update_crops()
        self.update_people()
        self.tickCounter += 1

        if self.tickCounter >= Context.ticksPerMinute:
            self.tickCounter = 0
            self.minNum += 1

        if self.minNum >= Context.minPerHour:
            self.minNum = 0
            self.hourNum += 1

        if self.hourNum >= Context.hourPerSol:
            self.hourNum = 0
            self.increment_sol()

    def get_temp(self, minutes = None):
        min_temp = self.current_env['min_temp']
        max_temp = self.current_env['max_temp']
        if minutes == None:
            minutes = self.minNum + self.hourNum * 60
        minutesInDay = 1440
        temp_range = max_temp - min_temp


        linearthreshold = 90
        #if we're less than the linear threshold in we'll do a linear approximation
        #in the hopes we can somewhat smoothly catch up or wait for the sinusoidal approximation
        #when switching between days
        if minutes < linearthreshold:
            cosapprox = min_temp + .5 * temp_range + .5 * temp_range * math.cos((linearthreshold + self.current_env['sunrise'] + 60) * 2 * math.pi / minutesInDay)
            m = (cosapprox - self.prevTemp) / linearthreshold
            b = self.prevTemp
            return m * minutes + b
        #if we're an hour in we'll do a sinusoidal approximation
        return min_temp + .5 * temp_range + .5 * temp_range * math.cos((minutes + self.current_env['sunrise'] + 60) * 2 * math.pi / minutesInDay)
#        if 60 * self.hourNum + self.minNum < self.current_env['sunrise'] or 60 * self.hourNum + self.minNum > self.current_env['sunset']:
#            return self.current_env['min_temp']
#        return self.current_env['max_temp']
    
    def get_pressure(self):
        return self.current_env['pressure']
    
    def get_uv(self):
        if 60 * self.hourNum + self.minNum < self.current_env['sunrise'] or 60 * self.hourNum + self.minNum > self.current_env['sunset']:
            return "Low"
        return self.current_env['uv_index']
    
    def get_sunrise(self):
        return self._format_time(self.current_env['sunrise'])
         
    
    def get_sunset(self):
        return self._format_time(self.current_env['sunset'])
    
    def get_production(self):
        return self.gainedFood * self.ticksPerHour
    
    def get_consumption(self):
        return self.consumedFood * self.ticksPerHour
    
    def get_net(self):
        return self.get_production() - self.get_consumption()

    def _format_time(self, min_since_midnight):
        hr = str(math.floor(min_since_midnight / 60))
        min = str(math.floor(min_since_midnight % 60))
        if len(hr) < 2:
            hr = '0' + hr
        if len(min) < 2:
            min = '0' + min
        return hr + ":" + min
    
    def doTickUpdate(self):
        self.gainedFood = 0
        self.consumedFood = self.population * 3 /self.ticksPerDay
        for crop in self.crops:

            self.gainedFood += crop.getFoodPerTick(self.get_temp(), self.get_uv())

        self.food += self.gainedFood - self.consumedFood
        self.totalfood += self.gainedFood - self.consumedFood

    def _handle_click_event(self, event, mouse):
        
        for region in self.click_regions:

            if region['x'] <= mouse[0] <= region['x'] + region['width'] and region['y'] <= mouse[1] <= region['y'] + region['height']:

                command = region['desc'].split('-')
               
                if command[0] == "sell":
                    crop = self.cropDict[command[1]]
                    if crop.sellPlant():
                        self.food += crop.sellValue
                        self.totalfood += crop.sellValue
                    

                elif command[0] == "buy":
                    crop = self.cropDict[command[1]]
                    if self.food >= crop.buyValue:
                        crop.addPlant(self.win_x1, self.win_y1, self.win_x2, self.win_y2, self.dead_x1, self.dead_y1, self.dead_x2, self.dead_y2)
                        self.food -= crop.buyValue

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
        if self.solNum > Context.solPerYear:
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
        return f"Year {self.yearNum}, Sol {self.solNum}        {str(self.hourNum).zfill(2)}:{str(self.minNum - self.minNum % Context.minuteIncrement).zfill(2)}"


