import math
import weather_data.soldata as soldata
import crops as crops
import random

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

    # Increases the number of plants of this crop by one. It is the implementing function's responsibility to check that there are sufficient funds.
    def addPlant(self, x1, y1, x2, y2, dead_x1, dead_y1, dead_x2, dead_y2):
        self.quantity += 1
        # Possibly increase price per plant on purchase?

        coords = [random.randint(x1, x2), random.randint(y1, y2)]

        while dead_x1 <= coords[0] <= dead_x2:
            coords[0] = random.randint(x1, x2)
        
        while dead_y1 <= coords[0] <= dead_y2:
            coords[1] = random.randint(y1, y2)

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
        self.name = "Generic Plant"
        self.quantity = 0           # All start at 0 quantity.
        self.minGoodTemp = -50      
        self.safeUvLevels = {"Very_High": False, "High": False, "Moderate": True, "Low":True}     
        self.sellValue = 10              
        self.buyValue = 20     
        self.foodPerHourPerPlant = 5
        self.spriteFile = "assets\\green_plant.png"
        self.spriteCoords = []        


class uvResistant(Crop):

    def __init__(self):
        self.name = "UV Resistant Plant"
        self.quantity = 0           # All start at 0 quantity.
        self.minGoodTemp = -50      
        self.safeUvLevels = {"Very_High": False, "High": True, "Moderate": True, "Low":True}       
        self.sellValue = 15             
        self.buyValue = 25     
        self.foodPerHourPerPlant = 3.5        
        self.spriteFile = "assets\\red_plant.png"
        self.spriteCoords = []       

class coldResistant(Crop):

    def __init__(self):
        self.name = "Cold Resistant Plant"
        self.quantity = 0           # All start at 0 quantity.
        self.minGoodTemp = -90      
        self.safeUvLevels = {"Very_High": False, "High": False, "Moderate": True, "Low":True}     
        self.sellValue = 15              
        self.buyValue = 25     
        self.foodPerHourPerPlant = 2
        self.spriteFile = "assets\\blue_plant.png"
        self.spriteCoords = []               

class hybrid(Crop):

    def __init__(self):
        self.name = "UV Resistant, Weak to Cold"
        self.quantity = 0           # All start at 0 quantity.
        self.minGoodTemp = -30      
        self.safeUvLevels = {"Very_High": False, "High": False, "Moderate": True, "Low":True}      
        self.sellValue = 15              
        self.buyValue = 30     
        self.foodPerHourPerPlant = 6.5 
        self.spriteFile = "assets\\potato.png"
        self.spriteCoords = []           

class cashcow(Crop):

    def __init__(self):

        self.name = "Cash cow"

        self.quantity = 0           # All start at 0 quantity.
        self.minGoodTemp = -10      
        self.safeUvLevels = {"Very_High": False, "High": False, "Moderate": False, "Low":True}     
        self.sellValue = 15              
        self.buyValue = 30     
        self.foodPerHourPerPlant = 25    
        self.spriteFile = "assets\\cash_cow.png"
        self.spriteCoords = []     

class Context:
    # Maximum number of days that history is kept for
    MAX_HISTORY = 30

    #mapping for uv
    UV_MAPPING = {'Very_High': 4, 'High': 3, 'Moderate': 2, 'Low':1}
    # Resource Counters
    food = 50

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


    # define last 30 days of highs/lows/pressure/uv
    highs = []
    lows =  []
    pressure = []
    uv = []

    # define the crop window
    win_x1 = 0
    win_x2 = 0
    win_y1 = 0
    win_y2 = 0
    # define the clicking deadzone
    dead_x1 = 0
    dead_x2 = 0
    dead_y1 = 0
    dead_y2 = 0

    sol_data = soldata.getAggregatedSolData()

    current_env = soldata.getRandomizedSolData(0, sol_data)

    tickCounter = 0
    yearNum = 1
    solNum = 1

    hourNum = 23

    minNum = 0

    # controls toggle gui
    portfolioMode = True


    # plant sprites and stuff
    coords = []

    def next_tick(self):
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
        generic(),
        coldResistant(),
        uvResistant(),
        hybrid(),
        cashcow()
    ]

    cropDict = {}

    for crop in crops:
        cropDict.update({crop.name: crop})

    def doTickUpdate(self):
        gainedFood = 0
        for crop in self.crops:

            gainedFood += crop.getFoodPerTick(self.get_temp(), self.get_uv())

        self.food += gainedFood




    def _handle_click_event(self, event, mouse):

        for region in self.click_regions:

            if region['x'] <= mouse[0] <= region['x'] + region['width'] and region['y'] <= mouse[1] <= region['y'] + region['height']:

                command = region['desc'].split('-')

                if command[0] == "sell":
                    crop = self.cropDict[command[1]]
                    if crop.sellPlant():
                        self.food += crop.sellValue

                elif command[0] == "buy":
                    crop = self.cropDict[command[1]]
                    if self.food >= crop.buyValue:
                        crop.addPlant(self.win_x1, self.win_y1, self.win_x2, self.win_y2, self.dead_x1, self.dead_y1, self.dead_x2, self.dead_y2)
                        self.food -= crop.buyValue

                elif command[0]  == "click":
                    self.food += 1

                elif command[0] == "switch":
                    if command[1] == "portfolio":
                        self.portfolioMode = True
                    else:
                        self.portfolioMode = False

    def init_click_regions(self):
        self.click_regions = []

    def append_click_region(self, x, y, width, height, str):


        self.click_regions.append({'x':x, 'y':y, 'width':width, 'height':height, 'desc': str})
    
    def increment_sol(self):
        
        self.solNum += 1
        if self.solNum >= Context.solPerYear:
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

        self.current_env = soldata.getRandomizedSolData(self.solNum - 1, self.sol_data)
    



    def get_time_string(self):
        return f"Year {self.yearNum}, Sol {self.solNum}        {str(self.hourNum).zfill(2)}:{str(self.minNum - self.minNum % Context.minuteIncrement).zfill(2)}"


